from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Download NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize NLP tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Load dataset
def load_data():
    import os
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'data', 'books.csv')
    
    # Use low_memory=False to handle mixed types and chunksize for memory efficiency
    df = pd.read_csv(csv_path, sep=';', encoding='latin-1', on_bad_lines='skip', low_memory=False)
    df = df[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]
    df.columns = ['isbn', 'title', 'author', 'year', 'publisher', 'image_url']
    df.dropna(inplace=True)
    
    # Clean the data
    df['title'] = df['title'].astype(str)
    df['author'] = df['author'].astype(str)
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df[df['year'].notna()]
    
    print(f"Loaded {len(df)} books from dataset")
    return df

books_df = load_data()

# Preprocess text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# Initialize TF-IDF Vectorizer with memory-efficient settings
tfidf = TfidfVectorizer(
    preprocessor=preprocess_text, 
    max_features=50000,  # Limit features to prevent memory issues
    stop_words='english',
    max_df=0.95,  # Ignore terms that appear in more than 95% of documents
    min_df=2      # Ignore terms that appear in less than 2 documents
)
tfidf_matrix = tfidf.fit_transform(books_df['title'] + ' ' + books_df['author'])

# Keep matrix sparse to save memory
print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")
print(f"Memory usage: {tfidf_matrix.nnz} non-zero elements")

# Get similar books using cosine similarity
def get_similar_books(book_title, n=5):
    try:
        book_idx = books_df[books_df['title'].str.contains(book_title, case=False, na=False)].index[0]
    except:
        return []
    
    # Use sparse matrix directly for memory efficiency
    book_vector = tfidf_matrix[book_idx:book_idx+1]  # Get single row as sparse matrix
    similarity_scores = cosine_similarity(book_vector, tfidf_matrix).flatten()
    
    # Get top similar indices (excluding the book itself)
    similar_indices = similarity_scores.argsort()[-n-1:-1][::-1]
    similar_indices = similar_indices[similar_indices != book_idx][:n]
    
    return books_df.iloc[similar_indices].to_dict('records')

# Generate AI recommendations using OpenAI
def generate_ai_recommendations(book_title, n=3):
    prompt = f"""
    Based on the book "{book_title}", suggest {n} similar books that readers might enjoy.
    Provide the recommendations in the following format:
    1. Book Title by Author - Brief reason for recommendation
    2. Book Title by Author - Brief reason for recommendation
    3. Book Title by Author - Brief reason for recommendation
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    
    return response.choices[0].message.content

# API Routes
@app.route('/api/books/categories', methods=['GET'])
def get_categories():
    categories = [
        "Romance", "Fanfiction", "LGBTQ+", "Wattpad Originals", "Werewolf", 
        "New Adult", "Fantasy", "Short Story", "Teen Fiction", "Historical Fiction",
        "Paranormal", "Editor's Picks", "Humor", "Horror", "Contemporary Lit",
        "Diverse Lit", "Mystery", "Thriller", "Science Fiction", "The Wattys",
        "Adventure", "Non-Fiction", "Poetry"
    ]
    return jsonify(categories)

@app.route('/api/books/category/<category>', methods=['GET'])
def get_books_by_category(category):
    # Get page parameter for pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Filter books by category using keywords in title/author
    category_keywords = {
        'Romance': ['love', 'romance', 'heart', 'passion', 'wedding', 'bride'],
        'Fantasy': ['magic', 'dragon', 'wizard', 'fantasy', 'kingdom', 'sword', 'quest'],
        'Mystery': ['mystery', 'detective', 'murder', 'crime', 'investigation', 'secret'],
        'Horror': ['horror', 'ghost', 'vampire', 'zombie', 'dark', 'fear', 'nightmare'],
        'Science Fiction': ['space', 'future', 'robot', 'alien', 'technology', 'time'],
        'Historical Fiction': ['history', 'war', 'century', 'historical', 'ancient', 'medieval'],
        'Thriller': ['thriller', 'suspense', 'action', 'chase', 'danger', 'spy'],
        'Contemporary Lit': ['life', 'family', 'relationship', 'modern', 'society'],
        'Teen Fiction': ['teen', 'young', 'school', 'adolescent', 'youth'],
        'Non-Fiction': ['guide', 'how to', 'biography', 'history', 'science', 'politics']
    }
    
    keywords = category_keywords.get(category, [category.lower()])
    
    # Filter books containing category keywords
    mask = books_df['title'].str.lower().str.contains('|'.join(keywords), na=False) | \
           books_df['author'].str.lower().str.contains('|'.join(keywords), na=False)
    
    filtered_books = books_df[mask]
    
    if filtered_books.empty:
        # If no matches, return random books
        filtered_books = books_df.sample(min(per_page * 5, len(books_df)))
    
    # Pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    result_books = filtered_books.iloc[start_idx:end_idx].to_dict('records')
    
    return jsonify({
        'books': result_books,
        'total': len(filtered_books),
        'page': page,
        'per_page': per_page,
        'category': category
    })

@app.route('/api/books/search', methods=['GET'])
def search_books():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    processed_query = preprocess_text(query)
    query_vec = tfidf.transform([processed_query])
    similarity_scores = cosine_similarity(query_vec, tfidf_matrix)
    similar_indices = similarity_scores.argsort()[0][-5:][::-1]
    results = books_df.iloc[similar_indices].to_dict('records')
    return jsonify(results)

@app.route('/api/books/recommend', methods=['GET'])
def recommend_books():
    book_title = request.args.get('title', '')
    if not book_title:
        return jsonify({"error": "Book title is required"}), 400
    
    # Get ML-based recommendations
    ml_recommendations = get_similar_books(book_title)
    
    # Get AI-generated recommendations (optional, requires OpenAI API)
    ai_recommendations = None
    try:
        if openai.api_key:
            ai_recommendations = generate_ai_recommendations(book_title)
    except:
        pass
    
    return jsonify({
        "ml_recommendations": ml_recommendations,
        "ai_recommendations": ai_recommendations
    })

@app.route('/api/books/popular', methods=['GET'])
def get_popular_books():
    """Get popular books (most recent publications)"""
    per_page = request.args.get('per_page', 20, type=int)
    
    # Sort by year descending and get recent books
    popular_books = books_df.sort_values('year', ascending=False).head(per_page)
    return jsonify(popular_books.to_dict('records'))

@app.route('/api/books/random', methods=['GET'])
def get_random_books():
    """Get random books for discovery"""
    count = request.args.get('count', 10, type=int)
    random_books = books_df.sample(min(count, len(books_df)))
    return jsonify(random_books.to_dict('records'))

@app.route('/api/books/<isbn>', methods=['GET'])
def get_book_details(isbn):
    """Get details for a specific book by ISBN"""
    book = books_df[books_df['isbn'] == isbn]
    if book.empty:
        return jsonify({"error": "Book not found"}), 404
    
    book_data = book.iloc[0].to_dict()
    
    # Get similar books
    similar_books = get_similar_books(book_data['title'], n=5)
    
    return jsonify({
        "book": book_data,
        "similar_books": similar_books
    })

if __name__ == '__main__':
    app.run(debug=True)