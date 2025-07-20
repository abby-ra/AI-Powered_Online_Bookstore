from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
import pandas as pd
from datetime import datetime

@dataclass
class BookRating:
    """Data model for book ratings"""
    user_id: str
    isbn: str
    rating: int  # 0-10 scale in the dataset
    timestamp: Optional[datetime] = None
    
    @property
    def normalized_rating(self) -> float:
        """Convert 0-10 scale to 0-5 scale for consistency"""
        return self.rating / 2.0 if self.rating > 0 else 0.0
    
    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'isbn': self.isbn,
            'rating': self.rating,
            'normalized_rating': self.normalized_rating,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    @classmethod
    def from_pandas_row(cls, row: pd.Series) -> 'BookRating':
        """Create rating object from pandas Series"""
        rating = 0
        try:
            rating = int(row.get('Book-Rating', 0))
        except (ValueError, TypeError):
            rating = 0
            
        return cls(
            user_id=str(row.get('User-ID', '')),
            isbn=str(row.get('ISBN', '')),
            rating=rating
        )

class RatingRepository:
    """Repository for managing ratings data"""
    
    def __init__(self):
        self.ratings: List[BookRating] = []
        self.user_ratings: Dict[str, List[BookRating]] = {}  # user_id -> ratings
        self.book_ratings: Dict[str, List[BookRating]] = {}  # isbn -> ratings
        self.rating_matrix: Optional[pd.DataFrame] = None
    
    def add_rating(self, rating: BookRating):
        """Add a rating to the repository"""
        self.ratings.append(rating)
        
        # Update user ratings index
        if rating.user_id not in self.user_ratings:
            self.user_ratings[rating.user_id] = []
        self.user_ratings[rating.user_id].append(rating)
        
        # Update book ratings index
        if rating.isbn not in self.book_ratings:
            self.book_ratings[rating.isbn] = []
        self.book_ratings[rating.isbn].append(rating)
    
    def load_ratings_from_dataframe(self, df: pd.DataFrame):
        """Load ratings from a pandas DataFrame"""
        self.ratings.clear()
        self.user_ratings.clear()
        self.book_ratings.clear()
        
        for _, row in df.iterrows():
            try:
                rating = BookRating.from_pandas_row(row)
                self.add_rating(rating)
            except Exception as e:
                continue  # Skip invalid ratings
        
        print(f"Loaded {len(self.ratings)} ratings for {len(self.user_ratings)} users and {len(self.book_ratings)} books")
    
    def get_user_ratings(self, user_id: str) -> List[BookRating]:
        """Get all ratings for a specific user"""
        return self.user_ratings.get(user_id, [])
    
    def get_book_ratings(self, isbn: str) -> List[BookRating]:
        """Get all ratings for a specific book"""
        return self.book_ratings.get(isbn, [])
    
    def get_book_average_rating(self, isbn: str) -> Optional[float]:
        """Get average rating for a book"""
        ratings = self.get_book_ratings(isbn)
        if not ratings:
            return None
        
        # Only consider non-zero ratings for average
        valid_ratings = [r.normalized_rating for r in ratings if r.rating > 0]
        if not valid_ratings:
            return None
        
        return sum(valid_ratings) / len(valid_ratings)
    
    def get_book_rating_count(self, isbn: str) -> int:
        """Get number of ratings for a book"""
        ratings = self.get_book_ratings(isbn)
        return len([r for r in ratings if r.rating > 0])
    
    def get_user_average_rating(self, user_id: str) -> Optional[float]:
        """Get average rating given by a user"""
        ratings = self.get_user_ratings(user_id)
        if not ratings:
            return None
        
        # Only consider non-zero ratings for average
        valid_ratings = [r.normalized_rating for r in ratings if r.rating > 0]
        if not valid_ratings:
            return None
        
        return sum(valid_ratings) / len(valid_ratings)
    
    def get_similar_users(self, user_id: str, min_common_books: int = 5) -> List[Tuple[str, float]]:
        """Find users with similar rating patterns"""
        user_ratings = self.get_user_ratings(user_id)
        if not user_ratings:
            return []
        
        user_books = {r.isbn: r.normalized_rating for r in user_ratings if r.rating > 0}
        similar_users = []
        
        for other_user_id, other_ratings in self.user_ratings.items():
            if other_user_id == user_id:
                continue
            
            other_books = {r.isbn: r.normalized_rating for r in other_ratings if r.rating > 0}
            
            # Find common books
            common_books = set(user_books.keys()) & set(other_books.keys())
            
            if len(common_books) >= min_common_books:
                # Calculate similarity (simple correlation)
                user_values = [user_books[isbn] for isbn in common_books]
                other_values = [other_books[isbn] for isbn in common_books]
                
                try:
                    import numpy as np
                    correlation = np.corrcoef(user_values, other_values)[0, 1]
                    if not pd.isna(correlation):
                        similar_users.append((other_user_id, correlation))
                except:
                    continue
        
        # Sort by similarity (highest first)
        similar_users.sort(key=lambda x: x[1], reverse=True)
        return similar_users[:20]  # Return top 20 similar users
    
    def get_popular_books(self, min_ratings: int = 10, limit: int = 50) -> List[Tuple[str, float, int]]:
        """Get popular books based on ratings"""
        book_stats = []
        
        for isbn, ratings in self.book_ratings.items():
            valid_ratings = [r.normalized_rating for r in ratings if r.rating > 0]
            if len(valid_ratings) >= min_ratings:
                avg_rating = sum(valid_ratings) / len(valid_ratings)
                rating_count = len(valid_ratings)
                
                # Calculate popularity score (weighted average)
                # Books with more ratings get slight preference
                popularity_score = avg_rating * (1 + min(rating_count / 100, 0.5))
                
                book_stats.append((isbn, popularity_score, rating_count))
        
        # Sort by popularity score
        book_stats.sort(key=lambda x: x[1], reverse=True)
        return book_stats[:limit]
    
    def create_user_item_matrix(self, sample_size: Optional[int] = None) -> pd.DataFrame:
        """Create user-item rating matrix for collaborative filtering"""
        if sample_size:
            # Sample users and books to make matrix manageable
            sampled_users = list(self.user_ratings.keys())[:sample_size]
            sampled_ratings = []
            
            for user_id in sampled_users:
                sampled_ratings.extend(self.user_ratings[user_id])
        else:
            sampled_ratings = self.ratings
        
        # Create DataFrame
        data = []
        for rating in sampled_ratings:
            if rating.rating > 0:  # Only include explicit ratings
                data.append({
                    'user_id': rating.user_id,
                    'isbn': rating.isbn,
                    'rating': rating.normalized_rating
                })
        
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        
        # Pivot to create user-item matrix
        matrix = df.pivot_table(
            index='user_id', 
            columns='isbn', 
            values='rating',
            fill_value=0
        )
        
        return matrix
    
    def get_statistics(self) -> Dict:
        """Get rating statistics"""
        total_ratings = len(self.ratings)
        explicit_ratings = len([r for r in self.ratings if r.rating > 0])
        
        if explicit_ratings > 0:
            avg_rating = sum(r.normalized_rating for r in self.ratings if r.rating > 0) / explicit_ratings
        else:
            avg_rating = 0
        
        return {
            'total_ratings': total_ratings,
            'explicit_ratings': explicit_ratings,
            'implicit_ratings': total_ratings - explicit_ratings,
            'unique_users': len(self.user_ratings),
            'unique_books': len(self.book_ratings),
            'average_rating': round(avg_rating, 2),
            'sparsity': 1 - (explicit_ratings / (len(self.user_ratings) * len(self.book_ratings))) if self.user_ratings and self.book_ratings else 0
        }
