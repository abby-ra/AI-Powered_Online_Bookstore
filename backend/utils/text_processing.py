import re
import string
from typing import List, Set
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk

class TextProcessor:
    """Advanced text processing utilities for book data"""
    
    def __init__(self):
        # Download required NLTK data
        self._download_nltk_data()
        
        # Initialize NLTK tools
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Add common book-specific stop words
        book_stop_words = {
            'book', 'novel', 'story', 'tale', 'chapter', 'page', 'read', 'reading',
            'author', 'writer', 'written', 'publish', 'published', 'publication',
            'edition', 'volume', 'series', 'part', 'first', 'second', 'third'
        }
        self.stop_words.update(book_stop_words)
    
    def _download_nltk_data(self):
        """Download required NLTK data if not already present"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            nltk.download('punkt_tab')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove HTML tags if any
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep spaces and letters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        if not text:
            return []
        
        # Use NLTK's word tokenizer
        tokens = word_tokenize(text)
        
        # Filter out punctuation and empty tokens
        tokens = [token for token in tokens if token and token not in string.punctuation]
        
        return tokens
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove stop words from token list"""
        return [token for token in tokens if token.lower() not in self.stop_words]
    
    def lemmatize_tokens(self, tokens: List[str]) -> List[str]:
        """Lemmatize tokens to their root form"""
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def preprocess_text(self, text: str) -> str:
        """Complete text preprocessing pipeline"""
        # Clean text
        text = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(text)
        
        # Remove stop words
        tokens = self.remove_stopwords(tokens)
        
        # Lemmatize
        tokens = self.lemmatize_tokens(tokens)
        
        # Join back to string
        return ' '.join(tokens)
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract important keywords from text"""
        processed_text = self.preprocess_text(text)
        tokens = processed_text.split()
        
        # Count word frequencies
        word_freq = {}
        for token in tokens:
            if len(token) > 2:  # Only consider words longer than 2 characters
                word_freq[token] = word_freq.get(token, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:max_keywords]]
    
    def create_search_terms(self, title: str, author: str, genre: str = None) -> str:
        """Create searchable terms from book metadata"""
        terms = []
        
        # Process title
        if title:
            title_processed = self.preprocess_text(title)
            terms.append(title_processed)
        
        # Process author
        if author:
            author_processed = self.preprocess_text(author)
            terms.append(author_processed)
        
        # Process genre
        if genre:
            genre_processed = self.preprocess_text(genre)
            terms.append(genre_processed)
        
        return ' '.join(terms)
    
    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts using Jaccard similarity"""
        if not text1 or not text2:
            return 0.0
        
        # Preprocess both texts
        tokens1 = set(self.preprocess_text(text1).split())
        tokens2 = set(self.preprocess_text(text2).split())
        
        if not tokens1 or not tokens2:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def fuzzy_match(self, query: str, text: str, threshold: float = 0.6) -> bool:
        """Check if query fuzzy matches text"""
        similarity = self.calculate_text_similarity(query, text)
        return similarity >= threshold

# Global instance for easy importing
text_processor = TextProcessor()
