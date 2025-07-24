import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { addToLibrary, addToSaveForLater } from '../services/library';

export default function BookDetail() {
  const { isbn } = useParams();
  const [book, setBook] = useState(null);
  const [recommendations, setRecommendations] = useState({ ml: [], ai: '' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch book details
    fetch(`http://localhost:5000/api/books/search?q=${isbn}`)
      .then(res => res.json())
      .then(data => {
        if (data.length > 0) {
          setBook(data[0]);
          // Fetch recommendations
          return fetch(`http://localhost:5000/api/books/recommend?title=${encodeURIComponent(data[0].title)}`);
        }
        return Promise.reject('Book not found');
      })
      .then(res => res.json())
      .then(data => setRecommendations({
        ml: data.ml_recommendations || [],
        ai: data.ai_recommendations || ''
      }))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, [isbn]);

  if (loading) {
    return <div className="text-center py-12">Loading...</div>;
  }

  if (!book) {
    return <div className="text-center py-12">Book not found</div>;
  }

  // Add feedback state
  const [feedback, setFeedback] = useState('');

  const handleAddToLibrary = async () => {
    if (!book) return;
    await addToLibrary(book.isbn);
    setFeedback('Added to My Library!');
    setTimeout(() => setFeedback(''), 1500);
  };
  const handleAddToSaveForLater = async () => {
    if (!book) return;
    await addToSaveForLater(book.isbn);
    setFeedback('Saved for Later!');
    setTimeout(() => setFeedback(''), 1500);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex flex-col md:flex-row gap-8 mb-12">
        <div className="md:w-1/3">
          <img 
            src={book.image_url} 
            alt={book.title} 
            className="w-full rounded-lg shadow-md"
            onError={(e) => {
              e.target.src = 'https://via.placeholder.com/300x450?text=No+Cover';
            }}
          />
        </div>
        <div className="md:w-2/3">
          <h1 className="text-3xl font-bold mb-2">{book.title}</h1>
          <p className="text-xl text-gray-600 mb-4">by {book.author}</p>
          <div className="flex items-center mb-4">
            <div className="flex">
              {[1, 2, 3, 4, 5].map((i) => (
                <span key={i} className="text-yellow-400 text-lg">⭐</span>
              ))}
            </div>
            <span className="ml-2 text-gray-600">(4.5)</span>
          </div>
          <div className="bg-gray-100 p-4 rounded-lg mb-6">
            <h3 className="font-bold mb-2">Details</h3>
            <p><span className="font-semibold">Publisher:</span> {book.publisher}</p>
            <p><span className="font-semibold">Year:</span> {book.year}</p>
            <p><span className="font-semibold">ISBN:</span> {book.isbn}</p>
          </div>
          <div className="flex gap-4 mb-2">
            <button
              onClick={handleAddToLibrary}
              className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition shadow-md focus:outline-none focus:ring-2 focus:ring-indigo-400"
              title="Add this book to your personal library"
            >
              <span role="img" aria-label="library">📚</span>
              <span>Add to Library</span>
            </button>
            <button
              onClick={handleAddToSaveForLater}
              className="flex items-center gap-2 bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg transition shadow-md focus:outline-none focus:ring-2 focus:ring-orange-300"
              title="Save this book for later"
            >
              <span role="img" aria-label="save for later">💾</span>
              <span>Save for Later</span>
            </button>
          </div>
          {feedback && <div className="text-green-600 font-semibold mt-2">{feedback}</div>}
        </div>
      </div>
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">You Might Also Like</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
          {recommendations.ml.map((book) => (
            <div key={book.isbn} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
              <img 
                src={book.image_url} 
                alt={book.title} 
                className="w-full h-48 object-cover"
                onError={(e) => {
                  e.target.src = 'https://via.placeholder.com/300x450?text=No+Cover';
                }}
              />
              <div className="p-4">
                <h3 className="font-bold text-lg mb-1">{book.title}</h3>
                <p className="text-gray-600 text-sm">{book.author}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="bg-indigo-50 p-6 rounded-lg">
        <h2 className="text-2xl font-bold mb-4">AI Recommendations</h2>
        <div className="prose max-w-none">
          {recommendations.ai.split('\n').map((line, i) => (
            <p key={i}>{line}</p>
          ))}
        </div>
      </div>
    </div>
  );
}