import { useSearchParams } from 'react-router-dom';
import { useEffect, useState } from 'react';

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
            <div key={book.isbn} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
              <img 
                src={book.image_url} 
                alt={book.title} 
                className="w-full h-64 object-contain p-4"
                onError={(e) => {
                  e.target.src = 'https://via.placeholder.com/300x450?text=No+Cover';
                }}
              />
              <div className="p-4">
                <h3 className="font-bold text-lg mb-1">{book.title}</h3>
                <p className="text-gray-600 mb-2">{book.author}</p>
                <p className="text-sm text-gray-500">{book.year} • {book.publisher}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}