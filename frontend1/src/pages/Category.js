import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function Category() {
  const { categoryName } = useParams();
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalBooks, setTotalBooks] = useState(0);
  const [hasMore, setHasMore] = useState(false);

  useEffect(() => {
    setLoading(true);
    setPage(1);
    fetchBooks(1);
  }, [categoryName]);

  const fetchBooks = async (pageNum) => {
    try {
      const response = await fetch(`http://localhost:5000/api/books/category/${encodeURIComponent(categoryName)}?page=${pageNum}&per_page=20`);
      const data = await response.json();
      
      if (pageNum === 1) {
        setBooks(data.books);
      } else {
        setBooks(prev => [...prev, ...data.books]);
      }
      
      setTotalBooks(data.total);
      setHasMore(data.books.length === 20);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching books:', error);
      setLoading(false);
    }
  };

  const loadMore = () => {
    const nextPage = page + 1;
    setPage(nextPage);
    fetchBooks(nextPage);
  };

  if (loading && page === 1) {
    return <div className="flex justify-center items-center min-h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
    </div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-500 to-pink-500 text-white p-6 rounded-lg">
        <h1 className="text-3xl font-bold">{decodeURIComponent(categoryName)}</h1>
        <p className="text-lg opacity-90">Discover amazing books in this category</p>
        {totalBooks > 0 && (
          <p className="text-sm opacity-75">{totalBooks} books available</p>
        )}
      </div>

      {/* Books Grid */}
      {books.length > 0 ? (
        <div className="space-y-6">
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

          {/* Load More Button */}
          {hasMore && (
            <div className="flex justify-center">
              <button
                onClick={loadMore}
                disabled={loading}
                className="bg-orange-500 text-white px-6 py-3 rounded-lg hover:bg-orange-600 transition disabled:opacity-50"
              >
                {loading ? 'Loading...' : 'Load More Books'}
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-12">
          <h2 className="text-xl font-semibold mb-4">No books found in this category</h2>
          <p className="text-gray-600 mb-6">Try browsing other categories or use the search function</p>
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

export default Category;
