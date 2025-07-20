import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function Home({ categories }) {
  const [featuredBooks, setFeaturedBooks] = useState([]);
  const [popularBooks, setPopularBooks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch featured/popular books
    Promise.all([
      fetch('http://localhost:5000/api/books/popular?per_page=6').then(res => res.json()),
      fetch('http://localhost:5000/api/books/random?count=6').then(res => res.json())
    ])
    .then(([popular, featured]) => {
      setPopularBooks(popular);
      setFeaturedBooks(featured);
      setLoading(false);
    })
    .catch(err => {
      console.error('Error fetching books:', err);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return <div className="flex justify-center items-center min-h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
    </div>;
  }

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-orange-500 to-pink-500 text-white p-8 rounded-lg">
        <h1 className="text-4xl font-bold mb-4">Discover Your Next Great Read</h1>
        <p className="text-xl mb-6">AI-powered recommendations from our vast collection of books</p>
        <Link 
          to="/search" 
          className="bg-white text-orange-500 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
        >
          Start Exploring
        </Link>
      </section>

      {/* Categories Grid */}
      <section>
        <h2 className="text-3xl font-bold mb-6">Browse by Genre</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {categories.map(category => (
            <Link
              key={category}
              to={`/category/${encodeURIComponent(category)}`}
              className="bg-gray-100 hover:bg-orange-100 p-4 rounded-lg text-center font-medium transition-colors"
            >
              {category}
            </Link>
          ))}
        </div>
      </section>

      {/* Featured Books */}
      <section>
        <h2 className="text-3xl font-bold mb-6">Featured Books</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
          {featuredBooks.map(book => (
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
                <h3 className="font-bold text-lg mb-2 line-clamp-2 text-gray-800">{book.title}</h3>
                <p className="text-gray-600 mb-1 font-medium">by {book.author}</p>
                <p className="text-gray-500 text-sm bg-gray-100 px-2 py-1 rounded-full inline-block">{book.year}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Popular Books */}
      <section>
        <h2 className="text-3xl font-bold mb-6">Popular This Week</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
          {popularBooks.map(book => (
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
                <h3 className="font-bold text-lg mb-2 line-clamp-2 text-gray-800">{book.title}</h3>
                <p className="text-gray-600 mb-1 font-medium">by {book.author}</p>
                <p className="text-gray-500 text-sm bg-gray-100 px-2 py-1 rounded-full inline-block">{book.year}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}

export default Home;
