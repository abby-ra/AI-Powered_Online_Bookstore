# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import time # For simulating delays

from data import MOCK_BOOKS
from ai_models import get_similar_book_titles_from_llm, identify_book_from_image

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route('/')
def home():
    return "AI Bookstore Backend is running!"

@app.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Simulate database search delay
    time.sleep(1)

    found_book = None
    for book in MOCK_BOOKS:
        if query in book['title'].lower() or query in book['author'].lower():
            found_book = book
            break

    if found_book:
        return jsonify(found_book)
    else:
        return jsonify({"message": "Book not found"}), 404

@app.route('/search_image', methods=['POST'])
def search_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "No selected image file"}), 400

    # In a real application, you'd save the image or pass its bytes
    # to your image recognition model.
    # For this demo, we'll just pass a placeholder.
    # image_data = image_file.read() # If you need actual image bytes

    # Simulate image processing delay
    time.sleep(2)

    # Call the AI model for image identification
    identified_book = identify_book_from_image(None) # Pass None as image_data for mock

    if identified_book:
        return jsonify(identified_book)
    else:
        return jsonify({"message": "Could not identify book from image"}), 404


@app.route('/similar_books', methods=['POST'])
def get_similar_books():
    data = request.get_json()
    book_description = data.get('description')

    if not book_description:
        return jsonify({"error": "Book description is required"}), 400

    # Simulate AI model inference delay
    time.sleep(1.5)

    # Call the AI model to get similar book titles
    similar_titles = get_similar_book_titles_from_llm(book_description)

    # Filter mock books to find those matching the generated titles
    # Or create new mock entries for titles not in MOCK_BOOKS
    similar_books_data = []
    for title in similar_titles:
        found = False
        for book in MOCK_BOOKS:
            if book['title'].lower() == title.lower():
                similar_books_data.append(book)
                found = True
                break
        if not found:
            # Create a new mock entry for a generated title not in our mock data
            similar_books_data.append({
                'id': f'gen-{len(similar_books_data)}-{title.replace(" ", "-").lower()}',
                'title': title,
                'author': 'AI Generated Author',
                'description': f'A book suggested by AI based on similarity to your search.',
                'imageUrl': f'https://placehold.co/150x200/F0F0F0/000000?text={title.replace(" ", "+")[:10]}',
                'ecommerceLinks': {
                    'amazon': f'https://www.amazon.com/s?k={title.replace(" ", "+")}',
                    'flipkart': f'https://www.flipkart.com/search?q={title.replace(" ", "+")}',
                },
            })

    return jsonify(similar_books_data)

if __name__ == '__main__':
    # Ensure the virtual environment is active before running
    # Flask will run on http://127.0.0.1:5000/ by default
    app.run(debug=True)