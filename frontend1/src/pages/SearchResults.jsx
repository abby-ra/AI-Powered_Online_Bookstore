import { useSearchParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { addToLibrary, addToSaveForLater } from '../services/library';

export default function SearchResults() {
  const [searchParams] = useSearchParams();
  const query = searchParams.get('q');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (query) {
      fetch(`http://localhost:5000/api/books/search?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
          setResults(data);
          setLoading(false);
        })
        .catch(err => {
          console.error(err);
          setLoading(false);
        });
    }
  }, [query]);

  if (loading) {
    return <div className="text-center py-12">Searching...</div>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Search Results for "{query}"</h1>
      
      {results.length === 0 ? (
        <p>No results found. Try a different search term.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.map((book) => (
            <div key={book.isbn} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition flex flex-col">
              <img 
                src={book.image_url} 
                alt={book.title} 
                className="w-full h-64 object-contain p-4"
                onError={(e) => {
                  e.target.src = 'https://via.placeholder.com/300x450?text=No+Cover';
                }}
              />
              <div className="p-4 flex-1 flex flex-col">
                <h3 className="font-bold text-lg mb-1">{book.title}</h3>
                <p className="text-gray-600 mb-2">{book.author}</p>
                <p className="text-sm text-gray-500">{book.year}  {book.publisher}</p>
                <div className="flex gap-2 mt-2">
                  <button
                    onClick={() => addToLibrary(book.isbn)}
                    className="flex items-center gap-1 bg-indigo-600 hover:bg-indigo-700 text-white px-2 py-1 rounded text-xs"
                    title="Add to Library"
                  >
                    <span role="img" aria-label="library">📚</span> Library
                  </button>
                  <button
                    onClick={() => addToSaveForLater(book.isbn)}
                    className="flex items-center gap-1 bg-orange-500 hover:bg-orange-600 text-white px-2 py-1 rounded text-xs"
                    title="Save for Later"
                  >
                    <span role="img" aria-label="save for later">💾</span> Save
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}