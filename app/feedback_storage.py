# feedback_storage.py
"""
Feedback storage system for the Financial Literacy Chatbot
Handles storing and retrieving user feedback on responses
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from config import Config


class FeedbackStorage:
    """Manages feedback data storage and retrieval"""
    
    def __init__(self, storage_path: Path = None):
        self.storage_path = storage_path or Config.FEEDBACK_STORAGE_PATH
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Ensure the feedback storage file exists"""
        if not self.storage_path.exists():
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)
    
    def save_feedback(self, query: str, response: str, feedback: str, 
                     confidence: float = None, timestamp: str = None) -> bool:
        """
        Save user feedback for a response
        
        Args:
            query: The user's question
            response: The chatbot's response
            feedback: 'positive' or 'negative'
            confidence: RAG confidence score (optional)
            timestamp: ISO timestamp (optional, defaults to now)
        
        Returns:
            bool: Success status
        """
        try:
            if timestamp is None:
                timestamp = datetime.now().isoformat()
            
            feedback_entry = {
                'timestamp': timestamp,
                'query': query,
                'response': response,
                'feedback': feedback,
                'confidence': confidence
            }
            
            # Load existing feedback
            feedback_data = self.load_all_feedback()
            feedback_data.append(feedback_entry)
            
            # Save back to file
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(feedback_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving feedback: {e}")
            return False
    
    def load_all_feedback(self) -> List[Dict]:
        """Load all feedback entries"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def get_feedback_stats(self) -> Dict:
        """Get feedback statistics"""
        feedback_data = self.load_all_feedback()
        
        if not feedback_data:
            return {
                'total_responses': 0,
                'positive': 0,
                'negative': 0,
                'helpfulness_rate': 0.0
            }
        
        positive = sum(1 for f in feedback_data if f.get('feedback') == 'positive')
        negative = sum(1 for f in feedback_data if f.get('feedback') == 'negative')
        total = len(feedback_data)
        
        return {
            'total_responses': total,
            'positive': positive,
            'negative': negative,
            'helpfulness_rate': (positive / total * 100) if total > 0 else 0.0
        }
    
    def get_recent_feedback(self, limit: int = 10) -> List[Dict]:
        """Get most recent feedback entries"""
        feedback_data = self.load_all_feedback()
        return sorted(feedback_data, key=lambda x: x.get('timestamp', ''), reverse=True)[:limit]