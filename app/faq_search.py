# faq_search.py
"""
FAQ Search functionality for the Financial Literacy Chatbot
Provides semantic search across FAQs with "People Also Asked" features
"""

import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from collections import Counter
from config import Config
from rag_retriever import RAGRetriever


class FAQSearch:
    """Handles FAQ search and related functionality"""

    def __init__(self, rag_retriever: Optional[RAGRetriever] = None):
        self.rag_retriever = rag_retriever
        self.search_history_path = Config.PROJECT_ROOT / "data" / "search_history.json"
        self._ensure_search_history_exists()

    def _ensure_search_history_exists(self):
        """Ensure search history file exists"""
        if not self.search_history_path.exists():
            self.search_history_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.search_history_path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)

    def search_faqs(self, query: str, top_k: int = 5) -> Dict:
        """
        Search FAQs using semantic search

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            Dict with 'results' and 'people_also_asked'
        """
        if not self.rag_retriever or not self.rag_retriever.vector_index:
            return {
                'results': [],
                'people_also_asked': [],
                'error': 'Search system not available'
            }

        try:
            # Perform semantic search
            search_results = self.rag_retriever.retrieve(
                query=query,
                top_k=top_k,
                use_reranking=True,
                translate_query=True
            )

            # Format results for display
            formatted_results = []
            for result in search_results:
                metadata = result['metadata']

                # Extract question and answer
                question = self._extract_question(metadata, result['content'])
                answer = self._extract_answer(metadata, result['content'])

                formatted_result = {
                    'question': question,
                    'answer': answer,
                    'similarity_score': result['similarity_score'],
                    'language': metadata.get('language', 'English'),
                    'category': metadata.get('category', 'general'),
                    'source': metadata.get('source', 'Unknown'),
                    'confidence': self._calculate_confidence(result)
                }
                formatted_results.append(formatted_result)

            # Get "People Also Asked" suggestions
            people_also_asked = self._get_people_also_asked(query, formatted_results)

            # Track this search
            self._track_search(query)

            return {
                'results': formatted_results,
                'people_also_asked': people_also_asked,
                'total_results': len(formatted_results)
            }

        except Exception as e:
            return {
                'results': [],
                'people_also_asked': [],
                'error': f'Search failed: {str(e)}'
            }

    def _extract_question(self, metadata: Dict, content: str) -> str:
        """Extract question from metadata or content"""
        # Try metadata first
        if 'question' in metadata and metadata['question']:
            return str(metadata['question'])

        # Try to extract from content
        content_lower = content.lower()
        if 'question:' in content_lower:
            parts = content.split('Question:', 1)
            if len(parts) > 1:
                question_part = parts[1].split('\n', 1)[0].strip()
                return question_part

        # Fallback: use first line or truncate content
        lines = content.split('\n', 1)
        if len(lines) > 0:
            first_line = lines[0].strip()
            if len(first_line) < 100:  # Reasonable question length
                return first_line

        # Last resort: truncate content
        return content[:100] + "..." if len(content) > 100 else content

    def _extract_answer(self, metadata: Dict, content: str) -> str:
        """Extract answer from metadata or content"""
        # Try metadata first
        if 'answer' in metadata and metadata['answer']:
            return str(metadata['answer'])
        if 'content' in metadata and metadata['content']:
            return str(metadata['content'])
        if 'original_answer' in metadata and metadata['original_answer']:
            return str(metadata['original_answer'])

        # Try to extract from content
        content_lower = content.lower()
        if 'answer:' in content_lower:
            parts = content.split('Answer:', 1)
            if len(parts) > 1:
                return parts[1].strip()

        # Return full content as answer
        return content

    def _calculate_confidence(self, result: Dict) -> float:
        """Calculate display confidence from similarity score"""
        score = result.get('similarity_score', 0.0)
        # Convert FAISS similarity to percentage (assuming normalized vectors)
        return min(100.0, max(0.0, score * 100))

    def _get_people_also_asked(self, original_query: str, results: List[Dict]) -> List[str]:
        """Generate 'People Also Asked' suggestions"""
        suggestions = []

        # Get popular searches
        popular_searches = self._get_popular_searches(limit=10)

        # Filter out the current query and similar queries
        current_words = set(original_query.lower().split())
        filtered_searches = []

        for search in popular_searches:
            search_words = set(search.lower().split())
            # Only include if not too similar to current query
            if len(current_words.intersection(search_words)) / len(current_words) < 0.8:
                filtered_searches.append(search)

        # Add some suggestions from results
        for result in results[:3]:  # First 3 results
            question = result.get('question', '')
            if question and len(question) < 150:  # Reasonable length
                # Create variations
                variations = self._generate_question_variations(question)
                suggestions.extend(variations)

        # Combine and deduplicate
        all_suggestions = filtered_searches[:5] + suggestions[:5]
        unique_suggestions = list(dict.fromkeys(all_suggestions))  # Preserve order

        return unique_suggestions[:8]  # Limit to 8 suggestions

    def _generate_question_variations(self, question: str) -> List[str]:
        """Generate related question variations"""
        variations = []
        question_lower = question.lower()

        # Common financial question patterns
        patterns = [
            ("what is", "how does"),
            ("how to", "what are the steps to"),
            ("why", "what are the reasons for"),
            ("when", "in what situations should I"),
        ]

        for old_pattern, new_pattern in patterns:
            if old_pattern in question_lower:
                variation = question_lower.replace(old_pattern, new_pattern, 1)
                # Capitalize first letter
                variation = variation[0].upper() + variation[1:]
                if variation != question:
                    variations.append(variation)

        return variations

    def _track_search(self, query: str):
        """Track search queries for analytics"""
        try:
            # Load existing history
            with open(self.search_history_path, 'r', encoding='utf-8') as f:
                history = json.load(f)

            # Add new search
            history.append({
                'query': query,
                'timestamp': json.dumps(None),  # Will be set by datetime in future
                'count': 1
            })

            # Keep only recent searches (last 1000)
            history = history[-1000:]

            # Save back
            with open(self.search_history_path, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"Warning: Could not track search: {e}")

    def _get_popular_searches(self, limit: int = 10) -> List[str]:
        """Get most popular search queries"""
        try:
            with open(self.search_history_path, 'r', encoding='utf-8') as f:
                history = json.load(f)

            # Count query frequencies
            query_counts = Counter(item['query'] for item in history)
            popular = query_counts.most_common(limit)

            return [query for query, count in popular]

        except Exception:
            return []

    def get_search_stats(self) -> Dict:
        """Get search statistics"""
        try:
            with open(self.search_history_path, 'r', encoding='utf-8') as f:
                history = json.load(f)

            total_searches = len(history)
            unique_queries = len(set(item['query'] for item in history))

            return {
                'total_searches': total_searches,
                'unique_queries': unique_queries,
                'popular_searches': self._get_popular_searches(5)
            }

        except Exception:
            return {
                'total_searches': 0,
                'unique_queries': 0,
                'popular_searches': []
            }