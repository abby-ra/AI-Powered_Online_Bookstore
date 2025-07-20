import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Navbar({ categories }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
      setSearchQuery('');
    }
  };

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="text-2xl">📚</div>
            <span className="text-xl font-bold text-orange-500">BookStore AI</span>
          </Link>

          {/* Search Bar - Desktop */}
          <form onSubmit={handleSearch} className="hidden md:flex flex-1 max-w-md mx-8">
            <div className="relative w-full">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search books, authors, genres..."
                className="w-full px-4 py-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              />
              <button
                type="submit"
                className="absolute right-0 top-0 h-full px-4 bg-orange-500 text-white rounded-r-lg hover:bg-orange-600 transition"
              >
                🔍
              </button>
            </div>
          </form>

          {/* Navigation Links - Desktop */}
          <div className="hidden md:flex items-center space-x-6">
            <Link to="/" className="text-gray-700 hover:text-orange-500 transition">
              Home
            </Link>
            <div className="relative group">
              <button className="text-gray-700 hover:text-orange-500 transition">
                Browse ▼
              </button>
              <div className="absolute top-full left-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-[100] min-w-56 max-w-xs">
                <div className="py-2 max-h-80 overflow-y-auto">
                  {categories.slice(0, 15).map(category => (
                    <Link
                      key={category}
                      to={`/category/${encodeURIComponent(category)}`}
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-orange-50 hover:text-orange-500 transition whitespace-nowrap"
                    >
                      {category}
                    </Link>
                  ))}
                  {categories.length > 15 && (
                    <div className="border-t border-gray-200 mt-2 pt-2">
                      <Link to="/categories" className="block px-4 py-2 text-sm text-orange-500 font-medium hover:bg-orange-50 transition">
                        View All Categories
                      </Link>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden text-gray-700 hover:text-orange-500 transition"
          >
            {isMobileMenuOpen ? '✕' : '☰'}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t border-gray-200 py-4">
            {/* Mobile Search */}
            <form onSubmit={handleSearch} className="mb-4">
              <div className="relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search books..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
                <button
                  type="submit"
                  className="absolute right-0 top-0 h-full px-4 bg-orange-500 text-white rounded-r-lg hover:bg-orange-600 transition"
                >
                  🔍
                </button>
              </div>
            </form>

            {/* Mobile Links */}
            <div className="space-y-2">
              <Link 
                to="/" 
                className="block py-2 text-gray-700 hover:text-orange-500 transition"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Home
              </Link>
              <div className="border-t border-gray-200 pt-2">
                <p className="text-sm font-medium text-gray-500 mb-2">Categories</p>
                <div className="grid grid-cols-2 gap-1">
                  {categories.slice(0, 8).map(category => (
                    <Link
                      key={category}
                      to={`/category/${encodeURIComponent(category)}`}
                      className="block py-1 px-2 text-sm text-gray-700 hover:text-orange-500 transition"
                      onClick={() => setIsMobileMenuOpen(false)}
                    >
                      {category}
                    </Link>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
