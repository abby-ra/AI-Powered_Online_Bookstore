from dataclasses import dataclass
from typing import Optional, List
import pandas as pd

@dataclass
class Book:
    """Data model for a book"""
    isbn: str
    title: str
    author: str
    year: int
    publisher: str
    image_url_s: str  # Small image
    image_url_m: str  # Medium image
    image_url_l: str  # Large image
    rating: Optional[float] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    
    @property
    def image_url(self) -> str:
        """Default image URL (large size)"""
        return self.image_url_l
    
    def to_dict(self) -> dict:
        """Convert book object to dictionary"""
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'publisher': self.publisher,
            'image_url': self.image_url_l,  # Use large image as default
            'image_url_s': self.image_url_s,
            'image_url_m': self.image_url_m,
            'image_url_l': self.image_url_l,
            'rating': self.rating,
            'genre': self.genre,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """Create book object from dictionary"""
        return cls(
            isbn=data.get('isbn', ''),
            title=data.get('title', ''),
            author=data.get('author', ''),
            year=int(data.get('year', 0)),
            publisher=data.get('publisher', ''),
            image_url_s=data.get('image_url_s', ''),
            image_url_m=data.get('image_url_m', ''),
            image_url_l=data.get('image_url_l', ''),
            rating=data.get('rating'),
            genre=data.get('genre'),
            description=data.get('description')
        )
    
    @classmethod
    def from_pandas_row(cls, row: pd.Series) -> 'Book':
        """Create book object from pandas Series"""
        return cls(
            isbn=str(row.get('ISBN', row.get('isbn', ''))),
            title=str(row.get('Book-Title', row.get('title', ''))),
            author=str(row.get('Book-Author', row.get('author', ''))),
            year=int(row.get('Year-Of-Publication', row.get('year', 0))) if pd.notna(row.get('Year-Of-Publication', row.get('year', 0))) else 0,
            publisher=str(row.get('Publisher', row.get('publisher', ''))),
            image_url_s=str(row.get('Image-URL-S', row.get('image_url_s', ''))),
            image_url_m=str(row.get('Image-URL-M', row.get('image_url_m', ''))),
            image_url_l=str(row.get('Image-URL-L', row.get('image_url_l', ''))),
            rating=float(row.get('rating')) if pd.notna(row.get('rating')) else None,
            genre=str(row.get('genre')) if pd.notna(row.get('genre')) else None,
            description=str(row.get('description')) if pd.notna(row.get('description')) else None
        )

@dataclass
class BookRecommendation:
    """Data model for book recommendations"""
    book: Book
    similarity_score: float
    recommendation_type: str  # 'ml', 'ai', 'collaborative'
    reason: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert recommendation object to dictionary"""
        return {
            'book': self.book.to_dict(),
            'similarity_score': self.similarity_score,
            'recommendation_type': self.recommendation_type,
            'reason': self.reason
        }

class BookCollection:
    """Collection class for managing books"""
    
    def __init__(self, books: List[Book]):
        self.books = books
        self._isbn_index = {book.isbn: book for book in books}
        self._title_index = {book.title.lower(): book for book in books}
    
    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        """Get book by ISBN"""
        return self._isbn_index.get(isbn)
    
    def get_by_title(self, title: str) -> Optional[Book]:
        """Get book by title (case insensitive)"""
        return self._title_index.get(title.lower())
    
    def search_by_title(self, query: str) -> List[Book]:
        """Search books by title substring"""
        query_lower = query.lower()
        return [book for book in self.books if query_lower in book.title.lower()]
    
    def search_by_author(self, query: str) -> List[Book]:
        """Search books by author substring"""
        query_lower = query.lower()
        return [book for book in self.books if query_lower in book.author.lower()]
    
    def filter_by_year_range(self, start_year: int, end_year: int) -> List[Book]:
        """Filter books by publication year range"""
        return [book for book in self.books if start_year <= book.year <= end_year]
    
    def get_random_books(self, n: int) -> List[Book]:
        """Get n random books"""
        import random
        return random.sample(self.books, min(n, len(self.books)))
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert collection to pandas DataFrame"""
        return pd.DataFrame([book.to_dict() for book in self.books])
