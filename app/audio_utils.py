# audio_utils.py
"""
Audio utility functions for handling audio files, format conversion, and playback
Provides helper functions for managing audio in Streamlit context
"""

import io
import wave
import struct
from pathlib import Path
from typing import Optional, Tuple
import numpy as np


class AudioHandler:
    """Utility class for audio file operations"""
    
    # Supported audio formats
    SUPPORTED_FORMATS = ['.wav', '.mp3', '.m4a', '.ogg', '.flac']
    
    # Audio quality settings
    AUDIO_QUALITY = {
        'sample_rate': 16000,
        'channels': 1,
        'sample_width': 2,  # 16-bit
        'bit_rate': '128k'
    }
    
    @staticmethod
    def validate_audio_file(filepath: str) -> Tuple[bool, str]:
        """
        Validate if file is a supported audio format
        
        Args:
            filepath: Path to audio file
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        path = Path(filepath)
        
        if not path.exists():
            return False, f"File not found: {filepath}"
        
        if path.suffix.lower() not in AudioHandler.SUPPORTED_FORMATS:
            return False, f"Unsupported format: {path.suffix}. Supported: {', '.join(AudioHandler.SUPPORTED_FORMATS)}"
        
        file_size_mb = path.stat().st_size / (1024 * 1024)
        if file_size_mb > 100:  # 100 MB limit
            return False, f"File too large: {file_size_mb:.1f}MB (max: 100MB)"
        
        return True, "File is valid"
    
    @staticmethod
    def get_audio_duration(filepath: str) -> Optional[float]:
        """
        Get audio file duration in seconds
        
        Args:
            filepath: Path to audio file
            
        Returns:
            Duration in seconds or None if error
        """
        try:
            if filepath.endswith('.wav'):
                with wave.open(filepath, 'rb') as wav_file:
                    frames = wav_file.getnframes()
                    rate = wav_file.getframerate()
                    duration = frames / float(rate)
                    return duration
            else:
                # For other formats, would need additional libraries like pydub
                return None
        except Exception as e:
            print(f"Error getting audio duration: {e}")
            return None
    
    @staticmethod
    def convert_to_wav(input_path: str, output_path: str) -> Tuple[bool, str]:
        """
        Convert audio file to WAV format
        
        Args:
            input_path: Path to input audio file
            output_path: Path to save converted WAV file
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # This would require ffmpeg or pydub
            # For now, return a message about dependency
            import subprocess
            
            # Check if ffmpeg is available
            try:
                subprocess.run(['ffmpeg', '-version'], 
                             capture_output=True, 
                             check=True)
            except (FileNotFoundError, subprocess.CalledProcessError):
                return False, "ffmpeg not installed. Install with: pip install pydub"
            
            # Convert using ffmpeg
            cmd = [
                'ffmpeg', '-i', input_path,
                '-acodec', 'pcm_s16le',
                '-ar', str(AudioHandler.AUDIO_QUALITY['sample_rate']),
                '-ac', str(AudioHandler.AUDIO_QUALITY['channels']),
                '-y',  # Overwrite output file
                output_path
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            return True, f"Converted to {output_path}"
            
        except Exception as e:
            return False, f"Conversion error: {str(e)}"
    
    @staticmethod
    def trim_audio_silence(audio_data: np.ndarray, 
                          sample_rate: int,
                          threshold: float = 0.02) -> np.ndarray:
        """
        Trim silence from beginning and end of audio
        
        Args:
            audio_data: Audio as numpy array
            sample_rate: Sample rate in Hz
            threshold: Silence threshold (0.0 to 1.0)
            
        Returns:
            Trimmed audio array
        """
        try:
            # Normalize audio
            max_val = np.max(np.abs(audio_data))
            if max_val > 0:
                normalized = audio_data / max_val
            else:
                normalized = audio_data
            
            # Find non-silent regions
            silent_mask = np.abs(normalized) > threshold
            
            if not np.any(silent_mask):
                return audio_data
            
            # Find indices of first and last non-silent samples
            indices = np.where(silent_mask)[0]
            return audio_data[indices[0]:indices[-1]]
            
        except Exception as e:
            print(f"Error trimming silence: {e}")
            return audio_data
    
    @staticmethod
    def normalize_audio(audio_data: np.ndarray) -> np.ndarray:
        """
        Normalize audio to -1.0 to 1.0 range
        
        Args:
            audio_data: Audio as numpy array
            
        Returns:
            Normalized audio array
        """
        try:
            max_val = np.max(np.abs(audio_data))
            if max_val > 0:
                return audio_data / max_val
            return audio_data
        except Exception as e:
            print(f"Error normalizing audio: {e}")
            return audio_data
    
    @staticmethod
    def estimate_speech_quality(audio_data: np.ndarray, 
                               sample_rate: int) -> dict:
        """
        Estimate audio quality metrics for speech
        
        Args:
            audio_data: Audio as numpy array
            sample_rate: Sample rate in Hz
            
        Returns:
            Dictionary with quality metrics
        """
        try:
            # Calculate various quality metrics
            rms = np.sqrt(np.mean(audio_data**2))
            peak = np.max(np.abs(audio_data))
            
            # Signal-to-noise ratio estimation
            # (simplified: assumes first 0.5s might contain noise)
            noise_duration = int(0.5 * sample_rate)
            if len(audio_data) > noise_duration:
                noise_level = np.std(audio_data[:noise_duration])
                signal_level = np.std(audio_data[noise_duration:])
                snr = 20 * np.log10(signal_level / (noise_level + 1e-10))
            else:
                snr = 0
            
            # Clipping detection
            clip_threshold = 0.95
            clipping_samples = np.sum(np.abs(audio_data) > clip_threshold)
            clip_percentage = (clipping_samples / len(audio_data)) * 100 if len(audio_data) > 0 else 0
            
            return {
                'rms_level': float(rms),
                'peak_level': float(peak),
                'snr_db': float(snr),
                'clipping_percentage': float(clip_percentage),
                'quality_score': _calculate_quality_score(rms, snr, clip_percentage)
            }
        except Exception as e:
            print(f"Error estimating quality: {e}")
            return {
                'rms_level': 0.0,
                'peak_level': 0.0,
                'snr_db': 0.0,
                'clipping_percentage': 0.0,
                'quality_score': 0.0
            }


def _calculate_quality_score(rms: float, snr: float, clipping: float) -> float:
    """
    Calculate overall audio quality score (0.0 to 1.0)
    
    Args:
        rms: RMS level
        snr: Signal-to-noise ratio in dB
        clipping: Clipping percentage
        
    Returns:
        Quality score between 0.0 and 1.0
    """
    # Component scores
    rms_score = min(max(rms / 0.3, 0.0), 1.0)  # Target RMS is 0.3
    snr_score = min(max(snr / 20.0, 0.0), 1.0)  # Target SNR is 20dB
    clip_score = 1.0 - (clipping / 100.0)  # No clipping is ideal
    
    # Weighted average
    score = (rms_score * 0.3 + snr_score * 0.4 + clip_score * 0.3)
    return float(min(max(score, 0.0), 1.0))


class StreamlitAudioHelper:
    """Helper class for Streamlit-specific audio operations"""
    
    @staticmethod
    def save_uploaded_audio(uploaded_file, save_dir: str = "temp_audio") -> Optional[str]:
        """
        Save Streamlit uploaded file to temporary location
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            save_dir: Directory to save files
            
        Returns:
            Path to saved file or None if error
        """
        try:
            from pathlib import Path
            
            # Create temp directory if needed
            temp_path = Path(save_dir)
            temp_path.mkdir(exist_ok=True)
            
            # Save file
            file_path = temp_path / uploaded_file.name
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            return str(file_path)
        except Exception as e:
            print(f"Error saving uploaded file: {e}")
            return None
    
    @staticmethod
    def create_audio_player_html(file_path: str, controls: bool = True) -> str:
        """
        Create HTML audio player element
        
        Args:
            file_path: Path to audio file
            controls: Whether to show player controls
            
        Returns:
            HTML string for audio player
        """
        controls_attr = "controls" if controls else ""
        return f"""
        <audio {controls_attr} style="width: 100%;">
            <source src="file://{file_path}" type="audio/wav">
            Your browser does not support the audio element.
        </audio>
        """
    
    @staticmethod
    def format_audio_info(filepath: str, duration: Optional[float] = None) -> str:
        """
        Format audio file information for display
        
        Args:
            filepath: Path to audio file
            duration: Audio duration in seconds
            
        Returns:
            Formatted info string
        """
        path = Path(filepath)
        size_kb = path.stat().st_size / 1024
        
        info = f"📁 {path.name} | 📊 {size_kb:.1f}KB"
        
        if duration:
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            info += f" | ⏱️ {minutes}:{seconds:02d}"
        
        return info
