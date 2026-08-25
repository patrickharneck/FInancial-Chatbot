# llm_client.py
"""
LLM API client for Groq integration
Handles all API calls and response processing
"""

import requests
from typing import Optional
from config import Config


class GroqClient:
    """Client for Groq API interactions"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.get_groq_api_key()
        self.base_url = Config.GROQ_API_URL
        self.available_models = Config.GROQ_MODELS
    
    def generate(
        self, 
        prompt: str,
        temperature: float = Config.DEFAULT_TEMPERATURE,
        max_tokens: int = Config.DEFAULT_MAX_TOKENS,
        timeout: int = Config.DEFAULT_TIMEOUT,
        system_instructions: Optional[str] = None
    ) -> str:
        """
        Generate response from Groq API
        
        Args:
            prompt: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            timeout: Request timeout in seconds
            system_instructions: Optional system message
            
        Returns:
            Generated text response
            
        Raises:
            ValueError: If API key is missing
            Exception: If no working models found
        """
        if not self.api_key:
            raise ValueError("No Groq API key provided")
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Try each model until one works
        for model in self.available_models:
            messages = []
            
            if system_instructions:
                messages.append({'role': 'system', 'content': system_instructions})
            
            messages.append({'role': 'user', 'content': prompt})
            
            payload = {
                'messages': messages,
                'model': model,
                'temperature': float(temperature),
                'top_p': 0.95,
                'max_tokens': max_tokens,
                'stream': False
            }
            
            try:
                response = requests.post(
                    self.base_url, 
                    headers=headers, 
                    json=payload, 
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and 'choices' in data:
                        return data['choices'][0]['message']['content']
                
                elif response.status_code == 404:
                    # Model not found, try next one
                    continue
                    
            except Exception:
                # Request failed, try next model
                continue
        
        raise Exception('No working Groq models found')
    
    def expand_response(
        self, 
        short_response: str, 
        min_words: int = Config.DEFAULT_RESPONSE_LENGTH
    ) -> str:
        """
        Expand a short response to meet minimum word count
        
        Args:
            short_response: Original short response
            min_words: Minimum required words
            
        Returns:
            Expanded response
        """
        expansion_prompt = (
            f"Expand this financial answer to be at least {min_words} words long, "
            f"with detailed explanation and Malawi-specific examples:\n\n{short_response}"
        )
        
        try:
            return self.generate(
                prompt=expansion_prompt,
                temperature=0.8,
                timeout=25
            )
        except Exception:
            # Return original if expansion fails
            return short_response