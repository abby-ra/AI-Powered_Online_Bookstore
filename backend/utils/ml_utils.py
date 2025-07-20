import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from scipy.sparse import csr_matrix
import joblib
import os

from models.book import Book, BookRecommendation, BookCollection
from utils.text_processing import text_processor

class MLRecommendationEngine:
    """Machine Learning based recommendation engine"""
    
    def __init__(self):
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.book_features = None
        self.similarity_matrix = None
        self.svd_model = None
        self.book_clusters = None
        self.is_fitted = False
    
    def fit(self, book_collection: BookCollection) -> None:
        """Fit the recommendation engine on book data"""
        df = book_collection.to_dataframe()
        
        # Create text features by combining title, author, and other metadata
        df['combined_features'] = df.apply(
            lambda row: text_processor.create_search_terms(
                row['title'], row['author'], row.get('genre', '')
            ), axis=1
        )
        
        # Initialize and fit TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            stop_words='english'
        )
        
        # Create TF-IDF matrix
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(df['combined_features'])
        
        # Calculate similarity matrix
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix)
        
        # Apply SVD for dimensionality reduction
        self.svd_model = TruncatedSVD(n_components=50, random_state=42)
        self.book_features = self.svd_model.fit_transform(self.tfidf_matrix)
        
        # Perform clustering
        self._perform_clustering(df)
        
        self.books_df = df
        self.is_fitted = True
    
    def _perform_clustering(self, df: pd.DataFrame) -> None:
        """Perform clustering on book features"""
        n_clusters = min(10, len(df) // 5)  # Adjust cluster count based on data size
        if n_clusters < 2:
            n_clusters = 2
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.book_clusters = kmeans.fit_predict(self.book_features)
        df['cluster'] = self.book_clusters
    
    def get_content_based_recommendations(
        self, 
        book_title: str, 
        n_recommendations: int = 5
    ) -> List[BookRecommendation]:
        """Get content-based recommendations for a book"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making recommendations")
        
        # Find the book index
        book_idx = self._find_book_index(book_title)
        if book_idx is None:
            return []
        
        # Get similarity scores
        similarity_scores = self.similarity_matrix[book_idx]
        
        # Get top similar books (excluding the book itself)
        similar_indices = np.argsort(similarity_scores)[::-1][1:n_recommendations+1]
        
        recommendations = []
        for idx in similar_indices:
            book_data = self.books_df.iloc[idx]
            book = Book.from_pandas_row(book_data)
            
            recommendation = BookRecommendation(
                book=book,
                similarity_score=float(similarity_scores[idx]),
                recommendation_type='content_based',
                reason=f"Similar content and themes to '{book_title}'"
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def get_cluster_based_recommendations(
        self, 
        book_title: str, 
        n_recommendations: int = 5
    ) -> List[BookRecommendation]:
        """Get cluster-based recommendations"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making recommendations")
        
        book_idx = self._find_book_index(book_title)
        if book_idx is None:
            return []
        
        # Get the cluster of the input book
        book_cluster = self.book_clusters[book_idx]
        
        # Find other books in the same cluster
        cluster_books = self.books_df[self.books_df['cluster'] == book_cluster]
        
        # Exclude the input book itself
        cluster_books = cluster_books[cluster_books.index != book_idx]
        
        # Get random samples from the cluster
        if len(cluster_books) > n_recommendations:
            cluster_books = cluster_books.sample(n_recommendations)
        
        recommendations = []
        for _, book_data in cluster_books.iterrows():
            book = Book.from_pandas_row(book_data)
            
            recommendation = BookRecommendation(
                book=book,
                similarity_score=0.8,  # Approximate score for cluster-based
                recommendation_type='cluster_based',
                reason=f"Part of similar genre/category as '{book_title}'"
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def search_books(
        self, 
        query: str, 
        n_results: int = 10
    ) -> List[Tuple[Book, float]]:
        """Search for books using TF-IDF similarity"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before searching")
        
        # Preprocess the query
        processed_query = text_processor.preprocess_text(query)
        
        # Transform query using the fitted vectorizer
        query_vector = self.tfidf_vectorizer.transform([processed_query])
        
        # Calculate similarity with all books
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get top results
        top_indices = np.argsort(similarity_scores)[::-1][:n_results]
        
        results = []
        for idx in top_indices:
            if similarity_scores[idx] > 0:  # Only include relevant results
                book_data = self.books_df.iloc[idx]
                book = Book.from_pandas_row(book_data)
                results.append((book, float(similarity_scores[idx])))
        
        return results
    
    def _find_book_index(self, book_title: str) -> Optional[int]:
        """Find the index of a book by title"""
        matches = self.books_df[
            self.books_df['title'].str.contains(book_title, case=False, na=False)
        ]
        
        if len(matches) > 0:
            return matches.index[0]
        
        return None
    
    def get_book_features_vector(self, book_title: str) -> Optional[np.ndarray]:
        """Get feature vector for a specific book"""
        book_idx = self._find_book_index(book_title)
        if book_idx is not None:
            return self.book_features[book_idx]
        return None
    
    def save_model(self, filepath: str) -> None:
        """Save the trained model to disk"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        
        model_data = {
            'tfidf_vectorizer': self.tfidf_vectorizer,
            'tfidf_matrix': self.tfidf_matrix,
            'similarity_matrix': self.similarity_matrix,
            'svd_model': self.svd_model,
            'book_features': self.book_features,
            'book_clusters': self.book_clusters,
            'books_df': self.books_df,
            'is_fitted': self.is_fitted
        }
        
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath: str) -> None:
        """Load a trained model from disk"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model_data = joblib.load(filepath)
        
        self.tfidf_vectorizer = model_data['tfidf_vectorizer']
        self.tfidf_matrix = model_data['tfidf_matrix']
        self.similarity_matrix = model_data['similarity_matrix']
        self.svd_model = model_data['svd_model']
        self.book_features = model_data['book_features']
        self.book_clusters = model_data['book_clusters']
        self.books_df = model_data['books_df']
        self.is_fitted = model_data['is_fitted']

class CollaborativeFilteringEngine:
    """Collaborative filtering recommendation engine"""
    
    def __init__(self):
        self.user_item_matrix = None
        self.item_similarity = None
        self.is_fitted = False
    
    def fit(self, user_ratings: Dict[str, Dict[str, float]]) -> None:
        """Fit collaborative filtering model
        
        Args:
            user_ratings: Dict of {user_id: {book_isbn: rating}}
        """
        # Create user-item matrix
        users = list(user_ratings.keys())
        books = set()
        for user_books in user_ratings.values():
            books.update(user_books.keys())
        books = list(books)
        
        # Create the matrix
        matrix = np.zeros((len(users), len(books)))
        
        for i, user in enumerate(users):
            for j, book in enumerate(books):
                if book in user_ratings[user]:
                    matrix[i, j] = user_ratings[user][book]
        
        self.user_item_matrix = matrix
        self.users = users
        self.books = books
        
        # Calculate item-item similarity
        self.item_similarity = cosine_similarity(matrix.T)
        
        self.is_fitted = True
    
    def get_user_recommendations(
        self, 
        user_id: str, 
        n_recommendations: int = 5
    ) -> List[Tuple[str, float]]:
        """Get recommendations for a user based on collaborative filtering"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making recommendations")
        
        if user_id not in self.users:
            return []
        
        user_idx = self.users.index(user_id)
        user_ratings = self.user_item_matrix[user_idx]
        
        # Calculate predicted ratings for unrated items
        predictions = []
        for book_idx, current_rating in enumerate(user_ratings):
            if current_rating == 0:  # Unrated book
                # Predict rating based on similar items
                similar_items = self.item_similarity[book_idx]
                weighted_sum = np.dot(similar_items, user_ratings)
                similarity_sum = np.sum(np.abs(similar_items[user_ratings > 0]))
                
                if similarity_sum > 0:
                    predicted_rating = weighted_sum / similarity_sum
                    predictions.append((self.books[book_idx], predicted_rating))
        
        # Sort by predicted rating and return top recommendations
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:n_recommendations]

# Global instances
ml_engine = MLRecommendationEngine()
collaborative_engine = CollaborativeFilteringEngine()
