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

### 8. Get Statistics (New)
- **URL:** `/api/stats`
- **Method:** `GET`
- **Description:** Get general statistics about the bookstore
- **Response:**
```json
{
  "total_users": 3,
  "total_books": 50,
  "total_genres": 8,
  "average_book_rating": 4.2
}
```

## Error Responses

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
