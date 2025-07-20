from dataclasses import dataclass
from typing import List, Optional, Dict
import json
from datetime import datetime

@dataclass
class UserPreferences:
    """User reading preferences"""
    favorite_genres: List[str]
    favorite_authors: List[str]
    reading_goals: Dict[str, int]  # e.g., {'books_per_month': 2, 'pages_per_day': 50}
    preferred_book_length: Optional[str] = None  # 'short', 'medium', 'long'
    preferred_publication_era: Optional[str] = None  # 'classic', 'modern', 'contemporary'
    
    def to_dict(self) -> dict:
        return {
            'favorite_genres': self.favorite_genres,
            'favorite_authors': self.favorite_authors,
            'reading_goals': self.reading_goals,
            'preferred_book_length': self.preferred_book_length,
            'preferred_publication_era': self.preferred_publication_era
        }

@dataclass
class ReadingHistory:
    """User's reading history entry"""
    isbn: str
    title: str
    author: str
    date_started: Optional[datetime] = None
    date_finished: Optional[datetime] = None
    rating: Optional[int] = None  # 1-5 scale
    review: Optional[str] = None
    status: str = 'to_read'  # 'to_read', 'reading', 'finished', 'abandoned'
    
    def to_dict(self) -> dict:
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'date_started': self.date_started.isoformat() if self.date_started else None,
            'date_finished': self.date_finished.isoformat() if self.date_finished else None,
            'rating': self.rating,
            'review': self.review,
            'status': self.status
        }

@dataclass
class User:
    """User data model"""
    user_id: str
    username: str
    email: str
    preferences: Optional[UserPreferences] = None
    reading_history: Optional[List[ReadingHistory]] = None
    created_at: Optional[datetime] = None
    last_active: Optional[datetime] = None
    
    def __post_init__(self):
        if self.reading_history is None:
            self.reading_history = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_active is None:
            self.last_active = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'preferences': self.preferences.to_dict() if self.preferences else None,
            'reading_history': [entry.to_dict() for entry in self.reading_history] if self.reading_history else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_active': self.last_active.isoformat() if self.last_active else None
        }
    
    def add_book_to_history(self, isbn: str, title: str, author: str, status: str = 'to_read') -> None:
        """Add a book to user's reading history"""
        new_entry = ReadingHistory(
            isbn=isbn,
            title=title,
            author=author,
            status=status
        )
        self.reading_history.append(new_entry)
        self.last_active = datetime.now()
    
    def update_reading_status(self, isbn: str, status: str, rating: Optional[int] = None, review: Optional[str] = None) -> bool:
        """Update reading status for a book"""
        for entry in self.reading_history:
            if entry.isbn == isbn:
                entry.status = status
                if rating is not None:
                    entry.rating = rating
                if review is not None:
                    entry.review = review
                if status == 'reading' and entry.date_started is None:
                    entry.date_started = datetime.now()
                elif status == 'finished' and entry.date_finished is None:
                    entry.date_finished = datetime.now()
                self.last_active = datetime.now()
                return True
        return False
    
    def get_finished_books(self) -> List[ReadingHistory]:
        """Get all finished books"""
        return [entry for entry in self.reading_history if entry.status == 'finished']
    
    def get_current_reading(self) -> List[ReadingHistory]:
        """Get currently reading books"""
        return [entry for entry in self.reading_history if entry.status == 'reading']
    
    def get_wishlist(self) -> List[ReadingHistory]:
        """Get books to read"""
        return [entry for entry in self.reading_history if entry.status == 'to_read']
    
    def get_favorite_authors(self) -> List[str]:
        """Get favorite authors based on reading history and preferences"""
        authors = []
        
        # From preferences
        if self.preferences and self.preferences.favorite_authors:
            authors.extend(self.preferences.favorite_authors)
        
        # From highly rated books
        for entry in self.reading_history:
            if entry.rating and entry.rating >= 4:
                authors.append(entry.author)
        
        # Remove duplicates and return
        return list(set(authors))
    
    def get_reading_stats(self) -> dict:
        """Get user's reading statistics"""
        finished_books = self.get_finished_books()
        current_books = self.get_current_reading()
        wishlist = self.get_wishlist()
        
        total_books = len(finished_books)
        average_rating = sum(entry.rating for entry in finished_books if entry.rating) / max(total_books, 1) if total_books > 0 else 0
        
        return {
            'total_books_read': total_books,
            'currently_reading': len(current_books),
            'books_to_read': len(wishlist),
            'average_rating': round(average_rating, 2),
            'favorite_authors': self.get_favorite_authors()
        }

class UserRepository:
    """In-memory user repository (would be replaced with database in production)"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
    
    def create_user(self, username: str, email: str) -> User:
        """Create a new user"""
        user_id = f"user_{len(self.users) + 1}"
        user = User(user_id=user_id, username=username, email=email)
        self.users[user_id] = user
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def update_user(self, user: User) -> bool:
        """Update user data"""
        if user.user_id in self.users:
            self.users[user.user_id] = user
            return True
        return False
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
