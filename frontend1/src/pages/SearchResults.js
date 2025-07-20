import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';

function SearchResults() {
  const [searchParams] = useSearchParams();
  const query = searchParams.get('q') || '';
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (query) {
      setLoading(true);
      fetch(`http://localhost:5000/api/books/search?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
          setBooks(data);
          setLoading(false);
        })
        .catch(err => {
          console.error('Error searching books:', err);
          setLoading(false);
        });
    }
  }, [query]);

  if (!query) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold mb-4">Search Books</h1>
        <p className="text-gray-600">Enter a search term to find books</p>
      </div>
    );
  }

  if (loading) {
    return <div className="flex justify-center items-center min-h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
    </div>;
  }

  return (
    <div className="space-y-6">
      {/* Search Header */}
      <div className="bg-gray-100 p-6 rounded-lg">
        <h1 className="text-2xl font-bold mb-2">Search Results</h1>
        <p className="text-gray-600">Found {books.length} results for "{query}"</p>
      </div>

      {/* Results */}
      {books.length > 0 ? (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4 md:gap-6">
          {books.map(book => (
            <Link
              key={book.isbn}
              to={`/book/${book.isbn}`}
              className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 p-3 group transform hover:-translate-y-1"
            >
              <div className="aspect-[2/3] overflow-hidden rounded-lg mb-3 bg-gray-100 shadow-md">
                <img 
                  src={book.image_url || '/placeholder-book.jpg'} 
                  alt={book.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  onError={(e) => {
                    e.target.src = '/placeholder-book.jpg';
                  }}
                />
              </div>
              <div className="text-center">
                <h3 className="font-bold text-sm md:text-base mb-1 line-clamp-2 text-gray-800">{book.title}</h3>
                <p className="text-gray-600 mb-1 text-xs md:text-sm font-medium line-clamp-1">by {book.author}</p>
                <p className="text-gray-500 text-xs bg-gray-100 px-2 py-1 rounded-full inline-block">{book.year}</p>
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <h2 className="text-xl font-semibold mb-4">No results found</h2>
          <p className="text-gray-600 mb-6">Try different keywords or browse by category</p>
          <Link 
            to="/"
            className="bg-orange-500 text-white px-6 py-3 rounded-lg hover:bg-orange-600 transition"
          >
            Back to Home
          </Link>
        </div>
      )}
    </div>
  );
}

export default SearchResults;
