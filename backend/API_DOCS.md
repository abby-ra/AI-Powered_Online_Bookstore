# API Documentation - AI-Powered Online Bookstore

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Get All Categories
- **URL:** `/api/books/categories`
- **Method:** `GET`
- **Description:** Get all available book categories/genres
- **Response:**
```json
[
  "Romance",
  "Fantasy", 
  "Science Fiction",
  "Mystery",
  "Horror",
  "Historical Fiction",
  "Fiction",
  "Drama"
]
```

### 2. Get Books by Category
- **URL:** `/api/books/category/<category>`
- **Method:** `GET`
- **Description:** Get books filtered by category
- **Parameters:**
  - `category` (string): The category/genre name
- **Response:**
```json
[
  {
    "isbn": "0439708184",
    "title": "Harry Potter and the Sorcerer's Stone",
    "author": "J.K. Rowling",
    "year": 1997,
    "publisher": "Scholastic Inc.",
    "image_url": "https://images.amazon.com/images/P/0439708184.01.L.jpg",
    "rating": 4.5,
    "genre": "Fantasy",
    "description": "A magical story about a young wizard..."
  }
]
```

### 3. Search Books
- **URL:** `/api/books/search`
- **Method:** `GET`
- **Description:** Search books by title, author, or content
- **Parameters:**
  - `q` (string): Search query
- **Response:** Array of book objects (same format as category endpoint)

### 4. Get Book Recommendations
- **URL:** `/api/books/recommend`
- **Method:** `GET`
- **Description:** Get AI and ML-based book recommendations
- **Parameters:**
  - `title` (string): Title of the book to base recommendations on
- **Response:**
```json
{
  "ml_recommendations": [
    {
      "book": {
        "isbn": "...",
        "title": "...",
        "author": "...",
        // ... other book fields
      },
      "similarity_score": 0.85,
      "recommendation_type": "content_based",
      "reason": "Similar content and themes to 'Harry Potter'"
    }
  ],
  "ai_recommendations": "AI-generated text recommendations..."
}
```

### 5. Get All Books (New)
- **URL:** `/api/books`
- **Method:** `GET`
- **Description:** Get all books with optional pagination
- **Parameters:**
  - `limit` (optional, integer): Number of books to return
  - `offset` (optional, integer): Number of books to skip
- **Response:** Array of book objects

### 6. Get Book by ISBN (New)
- **URL:** `/api/books/<isbn>`
- **Method:** `GET`
- **Description:** Get a specific book by its ISBN
- **Parameters:**
  - `isbn` (string): The book's ISBN
- **Response:** Single book object or 404 if not found

### 7. Get Available Genres (New)
- **URL:** `/api/genres`
- **Method:** `GET`
- **Description:** Get all available genres in the database
- **Response:** Array of genre strings

## New Enhanced Endpoints (Real Dataset)

### 9. Get User Recommendations (New)
- **URL:** `/api/users/<user_id>/recommendations`
- **Method:** `GET`
- **Description:** Get personalized recommendations for a specific user based on collaborative filtering
- **Parameters:**
  - `user_id` (string): The user's ID
  - `limit` (optional, integer): Number of recommendations (default: 10)
- **Response:** Array of book objects

### 10. Get Popular Books (New)
- **URL:** `/api/books/popular`
- **Method:** `GET`
- **Description:** Get most popular books based on ratings and user interactions
- **Parameters:**
  - `limit` (optional, integer): Number of books to return (default: 20)
- **Response:** Array of book objects sorted by popularity

### 11. Get Book by ISBN (Enhanced)
- **URL:** `/api/books/<isbn>`
- **Method:** `GET`
- **Description:** Get a specific book by its ISBN with rating information
- **Response:**
```json
{
  "isbn": "0195153448",
  "title": "Classical Mythology", 
  "author": "Mark P. O. Morford",
  "year": 2002,
  "publisher": "Oxford University Press",
  "image_url": "http://images.amazon.com/images/P/0195153448.01.LZZZZZZZ.jpg",
  "image_url_s": "http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg",
  "image_url_m": "http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg",
  "image_url_l": "http://images.amazon.com/images/P/0195153448.01.LZZZZZZZ.jpg",
  "rating": 4.2,
  "genre": "Mythology",
  "description": "A comprehensive guide to classical mythology..."
}
```

### 12. Get Rating-Based Recommendations (New)
- **URL:** `/api/books/<isbn>/recommendations`
- **Method:** `GET`
- **Description:** Get recommendations based on collaborative filtering for users who liked this book
- **Parameters:**
  - `isbn` (string): The book's ISBN
  - `limit` (optional, integer): Number of recommendations (default: 5)
- **Response:** Array of recommendation objects with similarity scores

### 13. Get Dataset Statistics (Enhanced)
- **URL:** `/api/stats`
- **Method:** `GET`
- **Description:** Get comprehensive statistics about the dataset
- **Response:**
```json
{
  "total_users": 1000,
  "total_books": 10000,
  "total_genres": 25,
  "total_ratings": 50000,
  "explicit_ratings": 21517,
  "average_book_rating": 4.1,
  "average_user_rating": 3.71,
  "data_sparsity": 0.999
}
```

## Dataset Information

This API now uses a real book recommendation dataset with:

### Books Dataset
- **Size**: ~271K books
- **Fields**: ISBN, Title, Author, Year, Publisher, Image URLs (Small, Medium, Large)
- **Sample Size**: 10K books loaded for performance
- **Coverage**: Wide variety of genres and publication years

### Ratings Dataset  
- **Size**: ~1.1M ratings
- **Sample Size**: 50K ratings loaded for performance
- **Rating Scale**: 0-10 (0 = implicit feedback, 1-10 = explicit ratings)
- **Normalized Scale**: Converted to 0-5 for consistency
- **Users**: ~4.3K active users in sample

### Users Dataset
- **Size**: ~278K users  
- **Sample Size**: 1K users loaded for performance
- **Fields**: User ID, Location, Age
- **Demographics**: Global user base with age information

## Enhanced Features

### 1. Collaborative Filtering
- Real user-item interactions
- User similarity calculations
- Rating-based recommendations
- Popular book identification

### 2. Content-Based Filtering (Enhanced)
- TF-IDF vectorization with rating features
- SVD dimensionality reduction
- Clustering with rating information
- Multi-modal feature combination

### 3. Hybrid Recommendations
- Combines content and collaborative approaches
- Rating-weighted similarity scores
- Popularity-boosted recommendations
- Cold-start handling for new users

### 4. Real-Time Statistics
- Data sparsity metrics
- Rating distribution analysis
- User engagement metrics
- Book popularity tracking

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad Request (missing required parameters)
- `404`: Not Found
- `500`: Internal Server Error

Error responses include a message:
```json
{
  "error": "Book title is required"
}
```

## Data Models

### Book Object
```json
{
  "isbn": "string",
  "title": "string", 
  "author": "string",
  "year": "integer",
  "publisher": "string",
  "image_url": "string",
  "rating": "float (optional)",
  "genre": "string (optional)",
  "description": "string (optional)"
}
```

### Recommendation Object
```json
{
  "book": "Book Object",
  "similarity_score": "float",
  "recommendation_type": "string",
  "reason": "string (optional)"
}
```

## Environment Variables

Create a `.env` file based on `.env.example`:
- `OPENAI_API_KEY`: Your OpenAI API key for AI recommendations
- `FLASK_ENV`: development/production
- `SECRET_KEY`: Flask secret key
- Other optional configuration variables

## Running the API

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run the server:
```bash
python run.py
# or
python app.py
```

The API will be available at `http://localhost:5000`
