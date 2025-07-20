import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function BookDetail() {
  const { isbn } = useParams();
  const [book, setBook] = useState(null);
  const [similarBooks, setSimilarBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isbn) {
      fetch(`http://localhost:5000/api/books/${isbn}`)
        .then(res => {
          if (!res.ok) {
            throw new Error('Book not found');
          }
          return res.json();
        })
        .then(data => {
          setBook(data.book);
          setSimilarBooks(data.similar_books || []);
          setLoading(false);
        })
        .catch(err => {
          setError(err.message);
          setLoading(false);
        });
    }
  }, [isbn]);

  if (loading) {
    return <div className="flex justify-center items-center min-h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
    </div>;
  }

  if (error || !book) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold mb-4">Book Not Found</h1>
        <p className="text-gray-600 mb-6">{error || 'The requested book could not be found.'}</p>
        <Link 
          to="/"
          className="bg-orange-500 text-white px-6 py-3 rounded-lg hover:bg-orange-600 transition"
        >
          Back to Home
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Book Details */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div className="lg:col-span-1">
          <div className="sticky top-8">
            <div className="aspect-[2/3] overflow-hidden rounded-xl shadow-2xl bg-gray-100 max-w-sm mx-auto">
              <img 
                src={book.image_url || '/placeholder-book.jpg'} 
                alt={book.title}
                className="w-full h-full object-cover hover:scale-105 transition-transform duration-500"
                onError={(e) => {
                  e.target.src = '/placeholder-book.jpg';
                }}
              />
            </div>
          </div>
        </div>
        
        <div className="lg:col-span-3 space-y-6">
          <div>
            <h1 className="text-4xl font-bold mb-4 text-gray-900">{book.title}</h1>
            <p className="text-2xl text-orange-600 mb-4 font-semibold">by {book.author}</p>
            <div className="flex flex-wrap gap-4 mb-6">
              <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                📅 Published: {book.year}
              </span>
              <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                🏢 {book.publisher}
              </span>
              <span className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm font-medium">
                📚 ISBN: {book.isbn}
              </span>
            </div>
          </div>

          <div className="flex flex-wrap gap-4">
            <button className="bg-orange-500 text-white px-8 py-3 rounded-lg hover:bg-orange-600 transition font-semibold shadow-lg">
              📖 Add to Library
            </button>
            <button className="bg-gray-200 text-gray-800 px-8 py-3 rounded-lg hover:bg-gray-300 transition font-semibold shadow-lg">
              💾 Save for Later
            </button>
            <button className="bg-blue-500 text-white px-8 py-3 rounded-lg hover:bg-blue-600 transition font-semibold shadow-lg">
              🔗 Share Book
            </button>
          </div>
        </div>
      </div>

      {/* Similar Books */}
      {similarBooks.length > 0 && (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold">Similar Books You Might Like</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
            {similarBooks.map(similarBook => (
              <Link
                key={similarBook.isbn}
                to={`/book/${similarBook.isbn}`}
                className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 p-3 group transform hover:-translate-y-1"
              >
                <div className="aspect-[2/3] overflow-hidden rounded-lg mb-3 bg-gray-100 shadow-md">
                  <img 
                    src={similarBook.image_url || '/placeholder-book.jpg'} 
                    alt={similarBook.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    onError={(e) => {
                      e.target.src = '/placeholder-book.jpg';
                    }}
                  />
                </div>
                <div className="text-center">
                  <h3 className="font-bold text-sm md:text-base mb-1 line-clamp-2 text-gray-800">{similarBook.title}</h3>
                  <p className="text-gray-600 mb-1 text-xs md:text-sm font-medium line-clamp-1">by {similarBook.author}</p>
                  <p className="text-gray-500 text-xs bg-gray-100 px-2 py-1 rounded-full inline-block">{similarBook.year}</p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default BookDetail;
