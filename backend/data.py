import pandas as pd
import os
from typing import List, Optional, Dict, Any
from models.book import Book, BookCollection
from models.user import User, UserRepository
from utils.text_processing import text_processor
from utils.ml_utils import ml_engine
import json
import random

class DataManager:
    """Centralized data management for the bookstore application"""
    
    def __init__(self, data_path: str = "data/books.csv"):
        self.data_path = data_path
        self.book_collection: Optional[BookCollection] = None
        self.user_repository = UserRepository()
        self._initialize_data()
    
    def _initialize_data(self):
        """Initialize the data by loading books and setting up ML models"""
        self._load_books()
        self._setup_ml_engine()
        self._create_sample_users()
    
    def _load_books(self):
        """Load books from CSV file"""
        try:
            if not os.path.exists(self.data_path):
                raise FileNotFoundError(f"Data file not found: {self.data_path}")
            
            # Read CSV with proper encoding and error handling
            df = pd.read_csv(
                self.data_path, 
                sep=';', 
                encoding='latin-1', 
                on_bad_lines='skip'
            )
            
            # Rename columns to match our model
            df.columns = ['isbn', 'title', 'author', 'year', 'publisher', 'image_url']
            
            # Clean and validate data
            df = self._clean_book_data(df)
            
            # Convert to Book objects
            books = []
            for _, row in df.iterrows():
                try:
                    book = Book.from_pandas_row(row)
                    # Add some mock genres and ratings for demonstration
                    book.genre = self._assign_genre(book.title, book.author)
                    book.rating = round(random.uniform(3.0, 5.0), 1)
                    book.description = self._generate_description(book.title, book.author, book.genre)
                    books.append(book)
                except Exception as e:
                    print(f"Error creating book from row {row.get('title', 'Unknown')}: {e}")
                    continue
            
            self.book_collection = BookCollection(books)
            print(f"Loaded {len(books)} books successfully")
            
        except Exception as e:
            print(f"Error loading books: {e}")
            # Create a fallback with some sample books
            self._create_fallback_books()
    
    def _clean_book_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate book data"""
        # Remove rows with missing essential data
        df = df.dropna(subset=['title', 'author'])
        
        # Clean year column
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df['year'] = df['year'].fillna(2000).astype(int)
        
        # Ensure year is reasonable
        df['year'] = df['year'].apply(lambda x: max(1800, min(2024, x)))
        
        # Fill missing publishers
        df['publisher'] = df['publisher'].fillna('Unknown Publisher')
        
        # Clean ISBN
        df['isbn'] = df['isbn'].astype(str).str.replace('-', '').str.replace(' ', '')
        
        # Ensure image URLs are strings
        df['image_url'] = df['image_url'].fillna('').astype(str)
        
        return df
    
    def _assign_genre(self, title: str, author: str) -> str:
        """Assign a genre based on title and author (simplified logic)"""
        title_lower = title.lower()
        author_lower = author.lower()
        
        # Simple genre assignment based on keywords
        if any(word in title_lower for word in ['love', 'romance', 'heart', 'wedding']):
            return 'Romance'
        elif any(word in title_lower for word in ['mystery', 'murder', 'detective', 'crime']):
            return 'Mystery'
        elif any(word in title_lower for word in ['magic', 'dragon', 'wizard', 'fantasy', 'elf']):
            return 'Fantasy'
        elif any(word in title_lower for word in ['space', 'future', 'robot', 'science', 'alien']):
            return 'Science Fiction'
        elif any(word in title_lower for word in ['horror', 'ghost', 'scary', 'fear', 'dark']):
            return 'Horror'
        elif any(word in title_lower for word in ['history', 'war', 'historical', 'past']):
            return 'Historical Fiction'
        elif any(author in author_lower for author in ['stephen king', 'edgar allan poe']):
            return 'Horror'
        elif any(author in author_lower for author in ['j.k. rowling', 'j.r.r. tolkien']):
            return 'Fantasy'
        elif any(author in author_lower for author in ['george orwell', 'aldous huxley']):
            return 'Dystopian'
        else:
            # Random genre assignment for variety
            genres = ['Fiction', 'Drama', 'Adventure', 'Contemporary', 'Literary Fiction', 'Thriller']
            return random.choice(genres)
    
    def _generate_description(self, title: str, author: str, genre: str) -> str:
        """Generate a simple book description"""
        templates = [
            f"A captivating {genre.lower()} novel by {author} that explores themes of human nature and society.",
            f"An engaging {genre.lower()} story from {author} that will keep you turning pages.",
            f"{author}'s masterful {genre.lower()} work that delves deep into character development.",
            f"A thought-provoking {genre.lower()} tale by {author} with rich storytelling.",
            f"An acclaimed {genre.lower()} novel by {author} that has touched millions of readers."
        ]
        return random.choice(templates)
    
    def _setup_ml_engine(self):
        """Set up and train the ML recommendation engine"""
        if self.book_collection:
            try:
                ml_engine.fit(self.book_collection)
                print("ML recommendation engine initialized successfully")
            except Exception as e:
                print(f"Error setting up ML engine: {e}")
    
    def _create_sample_users(self):
        """Create some sample users for testing"""
        sample_users = [
            {"username": "bookworm_alice", "email": "alice@example.com"},
            {"username": "reader_bob", "email": "bob@example.com"},
            {"username": "literary_carol", "email": "carol@example.com"}
        ]
        
        for user_data in sample_users:
            user = self.user_repository.create_user(
                user_data["username"], 
                user_data["email"]
            )
            # Add some sample reading history
            self._add_sample_reading_history(user)
    
    def _add_sample_reading_history(self, user: User):
        """Add sample reading history to a user"""
        if self.book_collection and len(self.book_collection.books) > 0:
            # Add 3-5 random books to reading history
            num_books = random.randint(3, 5)
            sample_books = self.book_collection.get_random_books(num_books)
            
            for book in sample_books:
                status = random.choice(['finished', 'reading', 'to_read'])
                rating = random.randint(3, 5) if status == 'finished' else None
                user.add_book_to_history(book.isbn, book.title, book.author, status)
                if rating:
                    user.update_reading_status(book.isbn, status, rating)
    
    def _create_fallback_books(self):
        """Create fallback books if CSV loading fails"""
        fallback_books = [
            Book(
                isbn="0000000001",
                title="The Great Adventure",
                author="John Doe",
                year=2020,
                publisher="Sample Publisher",
                image_url="https://via.placeholder.com/150",
                genre="Adventure",
                rating=4.2,
                description="An exciting adventure novel that takes you on a journey."
            ),
            Book(
                isbn="0000000002",
                title="Mystery of the Old House",
                author="Jane Smith",
                year=2019,
                publisher="Mystery Press",
                image_url="https://via.placeholder.com/150",
                genre="Mystery",
                rating=4.5,
                description="A thrilling mystery that will keep you guessing."
            )
        ]
        
        self.book_collection = BookCollection(fallback_books)
        print("Created fallback book collection")
    
    def get_books(self, limit: Optional[int] = None) -> List[Book]:
        """Get all books or a limited number"""
        if not self.book_collection:
            return []
        
        books = self.book_collection.books
        if limit:
            return books[:limit]
        return books
    
    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """Get a book by ISBN"""
        if self.book_collection:
            return self.book_collection.get_by_isbn(isbn)
        return None
    
    def search_books(self, query: str, limit: int = 10) -> List[Book]:
        """Search for books using the ML engine"""
        if not self.book_collection or not ml_engine.is_fitted:
            # Fallback to simple text search
            return self._simple_search(query, limit)
        
        try:
            results = ml_engine.search_books(query, limit)
            return [book for book, score in results]
        except Exception as e:
            print(f"Error in ML search, falling back to simple search: {e}")
            return self._simple_search(query, limit)
    
    def _simple_search(self, query: str, limit: int) -> List[Book]:
        """Simple fallback search"""
        if not self.book_collection:
            return []
        
        results = []
        query_lower = query.lower()
        
        for book in self.book_collection.books:
            if (query_lower in book.title.lower() or 
                query_lower in book.author.lower() or
                (book.genre and query_lower in book.genre.lower())):
                results.append(book)
                if len(results) >= limit:
                    break
        
        return results
    
    def get_books_by_genre(self, genre: str, limit: int = 10) -> List[Book]:
        """Get books by genre"""
        if not self.book_collection:
            return []
        
        matching_books = [
            book for book in self.book_collection.books
            if book.genre and book.genre.lower() == genre.lower()
        ]
        
        return matching_books[:limit]
    
    def get_recommendations(self, book_title: str, num_recommendations: int = 5) -> Dict[str, Any]:
        """Get both ML and AI recommendations for a book"""
        recommendations = {
            'ml_recommendations': [],
            'ai_recommendations': []
        }
        
        # Get ML recommendations
        if ml_engine.is_fitted:
            try:
                content_recs = ml_engine.get_content_based_recommendations(
                    book_title, num_recommendations
                )
                recommendations['ml_recommendations'] = [
                    rec.to_dict() for rec in content_recs
                ]
            except Exception as e:
                print(f"Error getting ML recommendations: {e}")
        
        # Get AI recommendations would be handled by the main app.py
        # This is just the data structure
        
        return recommendations
    
    def get_available_genres(self) -> List[str]:
        """Get all available genres"""
        if not self.book_collection:
            return []
        
        genres = set()
        for book in self.book_collection.books:
            if book.genre:
                genres.add(book.genre)
        
        return sorted(list(genres))
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get overall user statistics"""
        stats = {
            'total_users': len(self.user_repository.users),
            'total_books': len(self.book_collection.books) if self.book_collection else 0,
            'total_genres': len(self.get_available_genres()),
            'average_book_rating': 0.0
        }
        
        if self.book_collection:
            ratings = [book.rating for book in self.book_collection.books if book.rating]
            if ratings:
                stats['average_book_rating'] = round(sum(ratings) / len(ratings), 2)
        
        return stats

# Global data manager instance
data_manager = DataManager()
