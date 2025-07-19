# backend/ai_models.py
import requests
import os
import random # For mock image search

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def get_similar_book_titles_from_llm(book_description):
    """
    Simulates getting similar book titles using the Gemini API.
    In a real scenario, this would involve more sophisticated NLP/ML.
    """
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY not set. Cannot call Gemini API.")
        return ["Mock Similar Book 1", "Mock Similar Book 2"]

    prompt = f"Given the book description: \"{book_description}\". Suggest 3-4 similar book titles. Provide only the titles, separated by commas."
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()

        if result.get('candidates') and len(result['candidates']) > 0 and \
           result['candidates'][0].get('content') and \
           result['candidates'][0]['content'].get('parts') and \
           len(result['candidates'][0]['content']['parts']) > 0:
            text = result['candidates'][0]['content']['parts'][0]['text']
            titles = [t.strip() for t in text.split(',') if t.strip()]
            return titles
        else:
            print("Gemini API returned an unexpected structure or no content.")
            return ["Generated Similar Book A", "Generated Similar Book B"] # Fallback

    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return ["Network Error Book 1", "Network Error Book 2"] # Fallback on error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ["Unexpected Error Book X", "Unexpected Error Book Y"] # Fallback on error

def identify_book_from_image(image_data):
    """
    Placeholder for actual image recognition.
    In a real system, this would use a trained CV model.
    For now, it returns a random book from the mock data.
    """
    from data import MOCK_BOOKS # Import here to avoid circular dependency
    print("Simulating image recognition...")
    # In a real scenario, image_data would be processed by a CV model
    # For demo, just return a random book
    return random.choice(MOCK_BOOKS)