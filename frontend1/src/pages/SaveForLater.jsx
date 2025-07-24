import { useEffect, useState } from 'react';
import { getSaveForLater } from '../services/library';

export default function SaveForLater() {
  const [books, setBooks] = useState([]);
  useEffect(() => {
    getSaveForLater().then(setBooks);
  }, []);
  return (
    <div className="max-w-6xl mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Saved For Later</h1>
      {books.length === 0 ? (
        <p>No books saved for later.</p>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {books.map(book => (
            <div key={book.isbn} className="bg-white rounded-lg shadow-md p-4">
              <img src={book.image_url} alt={book.title} className="w-full h-40 object-cover mb-2 rounded" />
              <h3 className="font-bold text-lg">{book.title}</h3>
              <p className="text-gray-600 text-sm">{book.author}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
