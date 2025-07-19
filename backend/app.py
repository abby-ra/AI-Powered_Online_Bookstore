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
    df = pd.read_csv('data/books.csv', sep=';', encoding='latin-1', on_bad_lines='skip')
    df = df[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]
    df.columns = ['isbn', 'title', 'author', 'year', 'publisher', 'image_url']
    df.dropna(inplace=True)
    return df

books_df = load_data()

# Preprocess text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# Initialize TF-IDF Vectorizer
tfidf = TfidfVectorizer(preprocessor=preprocess_text)
tfidf_matrix = tfidf.fit_transform(books_df['title'] + ' ' + books_df['author'])

# Generate book embeddings
book_embeddings = tfidf_matrix.toarray()

# Get similar books using cosine similarity
def get_similar_books(book_title, n=5):
    try:
        book_idx = books_df[books_df['title'].str.contains(book_title, case=False)].index[0]
    except:
        return []
    
    similarity_scores = cosine_similarity([book_embeddings[book_idx]], book_embeddings)
    similar_indices = similarity_scores.argsort()[0][-n-1:-1][::-1]
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
    # This is a simplified version - in production you'd want actual category mapping
    sample_books = books_df.sample(10).to_dict('records')
    return jsonify(sample_books)

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
    
    # Get AI-generated recommendations
    ai_recommendations = generate_ai_recommendations(book_title)
    
    return jsonify({
        "ml_recommendations": ml_recommendations,
        "ai_recommendations": ai_recommendations
    })

if __name__ == '__main__':
    app.run(debug=True)