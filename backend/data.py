import pandas as pd
import os
from typing import List, Optional, Dict, Any
from models.book import Book, BookCollection
from models.user import User, UserRepository
from models.rating import BookRating, RatingRepository
from utils.text_processing import text_processor
from utils.ml_utils import ml_engine
import json
import random
import numpy as np

class DataManager:
    """Centralized data management for the bookstore application"""
    
    def __init__(self, 
                 books_path: str = "data/books.csv",
                 ratings_path: str = "data/ratings.csv", 
                 users_path: str = "data/users.csv"):
        self.books_path = books_path
        self.ratings_path = ratings_path
        self.users_path = users_path
        self.book_collection: Optional[BookCollection] = None
        self.user_repository = UserRepository()
        self.rating_repository = RatingRepository()
        self._initialize_data()
    
    def _initialize_data(self):
        """Initialize the data by loading all CSV files and setting up ML models"""
        print("Loading dataset...")
        self._load_books()
        self._load_users()
        self._load_ratings()
        self._setup_ml_engine()
        print("Data initialization complete!")
    
    def _load_books(self):
        """Load books from CSV file"""
        try:
            if not os.path.exists(self.books_path):
                raise FileNotFoundError(f"Books data file not found: {self.books_path}")
            
            print(f"Loading books from {self.books_path}...")
            # Read CSV with proper encoding and error handling
            df = pd.read_csv(
                self.books_path, 
                sep=';', 
                encoding='latin-1', 
                on_bad_lines='skip',
                dtype=str  # Read all as strings initially
            )
            
            print(f"Loaded {len(df)} book records")
            
            # Clean and validate data
            df = self._clean_book_data(df)
            
            # Convert to Book objects (sample first 10000 for performance)
            sample_size = min(10000, len(df))
            df_sample = df.sample(n=sample_size, random_state=42) if len(df) > sample_size else df
            
            books = []
            failed_count = 0
            
            for _, row in df_sample.iterrows():
                try:
                    book = Book.from_pandas_row(row)
                    # Add genre and description
                    book.genre = self._assign_genre(book.title, book.author)
                    book.description = self._generate_description(book.title, book.author, book.genre)
                    books.append(book)
                except Exception as e:
                    failed_count += 1
                    continue
            
            self.book_collection = BookCollection(books)
            print(f"Successfully loaded {len(books)} books ({failed_count} failed)")
            
        except Exception as e:
            print(f"Error loading books: {e}")
            # Create a fallback with some sample books
            self._create_fallback_books()
    
    def _load_users(self):
        """Load users from CSV file"""
        try:
            if not os.path.exists(self.users_path):
                print(f"Users data file not found: {self.users_path}, skipping user loading")
                return
            
            print(f"Loading users from {self.users_path}...")
            df = pd.read_csv(
                self.users_path,
                sep=';',
                encoding='latin-1',
                on_bad_lines='skip',
                dtype={'User-ID': str, 'Location': str, 'Age': str}
            )
            
            print(f"Loaded {len(df)} user records")
            
            # Sample users for performance (take first 1000)
            sample_size = min(1000, len(df))
            df_sample = df.head(sample_size)
            
            users_loaded = 0
            for _, row in df_sample.iterrows():
                try:
                    user = User.from_pandas_row(row)
                    self.user_repository.users[user.user_id] = user
                    users_loaded += 1
                except Exception as e:
                    continue
            
            print(f"Successfully loaded {users_loaded} users")
            
        except Exception as e:
            print(f"Error loading users: {e}")
    
    def _load_ratings(self):
        """Load ratings from CSV file"""
        try:
            if not os.path.exists(self.ratings_path):
                print(f"Ratings data file not found: {self.ratings_path}, skipping ratings loading")
                return
            
            print(f"Loading ratings from {self.ratings_path}...")
            
            # Load ratings in chunks to manage memory
            chunk_size = 50000
            total_loaded = 0
            
            for chunk in pd.read_csv(
                self.ratings_path,
                sep=';',
                encoding='latin-1',
                on_bad_lines='skip',
                dtype={'User-ID': str, 'ISBN': str, 'Book-Rating': str},
                chunksize=chunk_size
            ):
                self.rating_repository.load_ratings_from_dataframe(chunk)
                total_loaded += len(chunk)
                
                # Limit total ratings for performance (100K ratings)
                if total_loaded >= 100000:
                    break
            
            # Update book ratings in book collection
            self._update_book_ratings()
            
            print(f"Ratings loading complete. Statistics:")
            stats = self.rating_repository.get_statistics()
            for key, value in stats.items():
                print(f"  {key}: {value}")
            
        except Exception as e:
            print(f"Error loading ratings: {e}")
    
    def _update_book_ratings(self):
        """Update book objects with rating information"""
        if not self.book_collection:
            return
        
        for book in self.book_collection.books:
            avg_rating = self.rating_repository.get_book_average_rating(book.isbn)
            if avg_rating is not None:
                book.rating = round(avg_rating, 1)
    
    def _clean_book_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate book data"""
        # Make a copy to avoid SettingWithCopyWarning
        df = df.copy()
        
        # Remove rows with missing essential data
        df = df.dropna(subset=['Book-Title', 'Book-Author'])
        
        # Clean year column
        df['Year-Of-Publication'] = pd.to_numeric(df['Year-Of-Publication'], errors='coerce')
        df['Year-Of-Publication'] = df['Year-Of-Publication'].fillna(2000).astype(int)
        
        # Ensure year is reasonable
        df['Year-Of-Publication'] = df['Year-Of-Publication'].apply(lambda x: max(1500, min(2024, x)))
        
        # Fill missing publishers
        df['Publisher'] = df['Publisher'].fillna('Unknown Publisher')
        
        # Clean ISBN
        df['ISBN'] = df['ISBN'].astype(str).str.replace('-', '').str.replace(' ', '')
        
        # Ensure image URLs are strings and not null
        for col in ['Image-URL-S', 'Image-URL-M', 'Image-URL-L']:
            df[col] = df[col].fillna('').astype(str)
        
        # Remove duplicates based on ISBN
        df = df.drop_duplicates(subset=['ISBN'], keep='first')
        
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
        if self.book_collection and len(self.book_collection.books) > 0:
            try:
                # Use the enhanced fitting method with ratings if available
                if len(self.rating_repository.ratings) > 0:
                    ml_engine.fit_with_ratings(self.book_collection, self.rating_repository)
                else:
                    # Fallback to original method if no ratings
                    ml_engine.fit(self.book_collection)
                print("ML recommendation engine initialized successfully")
            except Exception as e:
                print(f"Error setting up ML engine: {e}")
                import traceback
                traceback.print_exc()
    
    def _create_sample_users(self):
        """Create some sample users for testing (if no real users loaded)"""
        if len(self.user_repository.users) > 0:
            return  # Real users already loaded
        
        sample_users = [
            {"username": "bookworm_alice", "email": "alice@example.com"},
            {"username": "reader_bob", "email": "bob@example.com"},
            {"username": "literary_carol", "email": "carol@example.com"}
        ]
        
        for i, user_data in enumerate(sample_users):
            user = User(
                user_id=str(i + 1),
                username=user_data["username"],
                email=user_data["email"]
            )
            self.user_repository.users[user.user_id] = user
    
    def get_user_recommendations(self, user_id: str, num_recommendations: int = 10) -> List[Book]:
        """Get personalized recommendations for a user based on their ratings"""
        user_ratings = self.rating_repository.get_user_ratings(user_id)
        if not user_ratings:
            # Return popular books for new users
            return self.get_popular_books(num_recommendations)
        
        # Get similar users
        similar_users = self.rating_repository.get_similar_users(user_id)
        if not similar_users:
            return self.get_popular_books(num_recommendations)
        
        # Collect books rated highly by similar users
        recommended_books = {}
        user_read_books = {r.isbn for r in user_ratings}
        
        for similar_user_id, similarity_score in similar_users[:5]:  # Top 5 similar users
            similar_user_ratings = self.rating_repository.get_user_ratings(similar_user_id)
            
            for rating in similar_user_ratings:
                if (rating.isbn not in user_read_books and 
                    rating.normalized_rating >= 4.0):  # Only recommend highly rated books
                    
                    if rating.isbn not in recommended_books:
                        recommended_books[rating.isbn] = 0
                    
                    # Weight by similarity score
                    recommended_books[rating.isbn] += similarity_score * rating.normalized_rating
        
        # Sort by recommendation score
        sorted_recommendations = sorted(
            recommended_books.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:num_recommendations]
        
        # Get book objects
        recommended_book_objects = []
        for isbn, score in sorted_recommendations:
            book = self.get_book_by_isbn(isbn)
            if book:
                recommended_book_objects.append(book)
        
        return recommended_book_objects
    
    def get_popular_books(self, limit: int = 20) -> List[Book]:
        """Get popular books based on ratings"""
        popular_isbn_list = self.rating_repository.get_popular_books(limit=limit)
        
        popular_books = []
        for isbn, popularity_score, rating_count in popular_isbn_list:
            book = self.get_book_by_isbn(isbn)
            if book:
                popular_books.append(book)
        
        return popular_books
    
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
        rating_stats = self.rating_repository.get_statistics()
        
        stats = {
            'total_users': len(self.user_repository.users),
            'total_books': len(self.book_collection.books) if self.book_collection else 0,
            'total_genres': len(self.get_available_genres()),
            'total_ratings': rating_stats.get('total_ratings', 0),
            'explicit_ratings': rating_stats.get('explicit_ratings', 0),
            'average_book_rating': 0.0,
            'average_user_rating': rating_stats.get('average_rating', 0),
            'data_sparsity': rating_stats.get('sparsity', 0)
        }
        
        if self.book_collection:
            ratings = [book.rating for book in self.book_collection.books if book.rating]
            if ratings:
                stats['average_book_rating'] = round(sum(ratings) / len(ratings), 2)
        
        return stats
    
    def get_book_recommendations_by_rating(self, isbn: str, num_recommendations: int = 5) -> List[Book]:
        """Get recommendations based on users who rated this book highly"""
        # Get users who rated this book highly
        book_ratings = self.rating_repository.get_book_ratings(isbn)
        high_rating_users = [
            r.user_id for r in book_ratings 
            if r.normalized_rating >= 4.0
        ]
        
        if not high_rating_users:
            return []
        
        # Get books that these users also rated highly
        recommended_books = {}
        
        for user_id in high_rating_users[:20]:  # Limit to top 20 users
            user_ratings = self.rating_repository.get_user_ratings(user_id)
            
            for rating in user_ratings:
                if (rating.isbn != isbn and 
                    rating.normalized_rating >= 4.0):
                    
                    if rating.isbn not in recommended_books:
                        recommended_books[rating.isbn] = 0
                    recommended_books[rating.isbn] += 1
        
        # Sort by frequency
        sorted_recommendations = sorted(
            recommended_books.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:num_recommendations]
        
        # Get book objects
        recommended_book_objects = []
        for isbn, count in sorted_recommendations:
            book = self.get_book_by_isbn(isbn)
            if book:
                recommended_book_objects.append(book)
        
        return recommended_book_objects

# Global data manager instance
data_manager = DataManager()
