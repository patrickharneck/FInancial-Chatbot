# audio_recording_ui.py
"""
Audio recording UI component for inline microphone input in chat interface
Provides seamless voice input similar to ChatGPT/Copilot interface
"""

import streamlit as st
import threading
from typing import Optional, Dict
from voice_processor import VoiceProcessor
from config import Config


class AudioRecordingUI:
    """Manages inline audio recording UI component"""
    
    @staticmethod
    def initialize_recording_state():
        """Initialize recording session state variables"""
        if 'recording' not in st.session_state:
            st.session_state.recording = False
        if 'recording_thread' not in st.session_state:
            st.session_state.recording_thread = None
        if 'recording_result' not in st.session_state:
            st.session_state.recording_result = None
    
    @staticmethod
    def render_inline_recording_button(
        enable_voice: bool,
        voice_language: str = 'en-US',
        button_size: str = "small"
    ) -> Optional[str]:
        """
        Render inline recording button for chat input area
        
        Args:
            enable_voice: Whether voice input is enabled
            voice_language: Language code for voice recognition
            button_size: Button size ('small', 'medium', 'large')
            
        Returns:
            Recognized text if recording completed, None otherwise
        """
        AudioRecordingUI.initialize_recording_state()
        
        if not enable_voice:
            return None
        
        # Recording status and button
        if st.session_state.recording:
            # Show recording state with stop button
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("🎤 **Recording...** (Click to stop)")
            
            with col2:
                if st.button("⏹️ Stop Recording", key="stop_recording_btn", use_container_width=True):
                    st.session_state.recording = False
                    st.rerun()
        else:
            # Show start recording button
            if st.button(
                "🎤 Record",
                key="start_recording_btn",
                use_container_width=True,
                help="Click to record your voice input"
            ):
                st.session_state.recording = True
                st.rerun()
        
        # Process recording result
        if st.session_state.recording_result:
            result = st.session_state.recording_result
            st.session_state.recording_result = None
            
            if result['success']:
                return result['text']
            else:
                st.error(f"❌ {result['error']}")
        
        return None
    
    @staticmethod
    def render_inline_microphone_icon(
        enable_voice: bool,
        voice_language: str = 'en-US',
        on_record_complete: Optional[callable] = None
    ) -> Optional[str]:
        """
        Render microphone icon that can be clicked for quick recording
        Designed to sit next to chat input for seamless UX
        
        Args:
            enable_voice: Whether voice input is enabled
            voice_language: Language code for voice recognition
            on_record_complete: Callback function when recording completes
            
        Returns:
            Recognized text if recording completed, None otherwise
        """
        AudioRecordingUI.initialize_recording_state()
        
        if not enable_voice:
            return None
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.session_state.recording:
                st.markdown("🎤 **REC**")
                if st.button("⏹️ Stop", key="stop_rec_icon", use_container_width=True):
                    st.session_state.recording = False
                    # Perform actual recording here
                    AudioRecordingUI._perform_recording(voice_language)
            else:
                if st.button("🎤", key="start_rec_icon", use_container_width=True, help="Click to record"):
                    st.session_state.recording = True
                    AudioRecordingUI._perform_recording(voice_language)
                    st.rerun()
        
        # Return result if available
        if st.session_state.recording_result:
            result = st.session_state.recording_result
            st.session_state.recording_result = None
            
            if result['success']:
                if on_record_complete:
                    on_record_complete(result['text'])
                return result['text']
            else:
                st.warning(f"❌ {result['error']}")
        
        return None
    
    @staticmethod
    def _perform_recording(voice_language: str):
        """
        Perform actual voice recording
        
        Args:
            voice_language: Language code for voice recognition
        """
        try:
            with st.spinner("🎤 Listening... Speak now!"):
                voice_processor = VoiceProcessor(enable_tts=False)
                voice_processor.set_language(voice_language)
                
                result = voice_processor.process_voice_input(
                    timeout=Config.SPEECH_RECOGNITION_TIMEOUT
                )
                
                st.session_state.recording_result = result
                st.session_state.recording = False
                
        except Exception as e:
            st.session_state.recording_result = {
                'success': False,
                'error': f"Recording error: {str(e)}",
                'text': ''
            }
            st.session_state.recording = False
    
    @staticmethod
    def render_chat_input_with_microphone(
        enable_voice: bool,
        voice_language: str = 'en-US',
        placeholder: str = "Ask about money..."
    ) -> Optional[str]:
        """
        Render chat input with inline microphone button
        Similar to ChatGPT/Copilot interface
        
        Args:
            enable_voice: Whether voice input is enabled
            voice_language: Language code for voice recognition
            placeholder: Placeholder text for input field
            
        Returns:
            User input (from text or voice)
        """
        AudioRecordingUI.initialize_recording_state()
        
        col1, col2 = st.columns([20, 1]) if enable_voice else (st.columns([1]), None)
        
        with col1:
            user_input = st.chat_input(placeholder)
        
        if col2 is not None:
            with col2:
                if st.session_state.recording:
                    if st.button("⏹️", key="stop_chat_rec", help="Stop recording"):
                        st.session_state.recording = False
                        AudioRecordingUI._perform_recording(voice_language)
                        st.rerun()
                else:
                    if st.button("🎤", key="start_chat_rec", help="Click to record your question"):
                        st.session_state.recording = True
                        AudioRecordingUI._perform_recording(voice_language)
                        st.rerun()
        
        # Check for voice input result
        if st.session_state.recording_result:
            result = st.session_state.recording_result
            st.session_state.recording_result = None
            
            if result['success']:
                return result['text']
            else:
                st.error(f"❌ {result['error']}")
                return None
        
        return user_input
