import { Link } from 'react-router-dom';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Navbar({ categories }) {
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
      setSearchQuery('');
    }
  };

  return (
    <header className="bg-indigo-900 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between">
          <div className="flex items-center space-x-6">
            <Link to="/" className="text-2xl font-bold hover:text-indigo-200 transition">
              AI Bookstore
            </Link>
            <span
              onClick={() => navigate('/library')}
              className="cursor-pointer text-base font-bold px-2 py-1 rounded hover:bg-indigo-700 transition"
              style={{letterSpacing: '0.5px'}}
            >
              📚 My Library
            </span>
            <span
              onClick={() => navigate('/save-for-later')}
              className="cursor-pointer text-base font-bold px-2 py-1 rounded hover:bg-orange-500 transition"
              style={{letterSpacing: '0.5px'}}
            >
              💾 Save for Later
            </span>
          </div>
          <form onSubmit={handleSearch} className="mt-4 md:mt-0 md:ml-4 flex">
            <input
              type="text"
              placeholder="Search books..."
              className="px-4 py-2 rounded-l-lg text-gray-800 w-full md:w-64 focus:outline-none"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button
              type="submit"
              className="bg-indigo-700 hover:bg-indigo-600 px-4 py-2 rounded-r-lg transition"
            >
              🔍
            </button>
          </form>
        </div>
        <nav className="mt-4 overflow-x-auto">
          <ul className="flex space-x-6 whitespace-nowrap">
            {categories.map((category) => (
              <li key={category}>
                <Link
                  to={`/category/${category.toLowerCase().replace(/\s+/g, '-')}`}
                  className="hover:text-indigo-200 transition text-sm md:text-base"
                >
                  {category}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </header>
  );
}