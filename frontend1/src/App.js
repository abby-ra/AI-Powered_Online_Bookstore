import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Home from './pages/Home';
import Category from './pages/Category';
import SearchResults from './pages/SearchResults';
import BookDetail from './pages/BookDetail';
import MyLibrary from './pages/MyLibrary';
import SaveForLater from './pages/SaveForLater';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

function App() {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/books/categories')
      .then(res => res.json())
      .then(data => setCategories(data));
  }, []);

  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <Navbar categories={categories} />
        <main className="flex-grow container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home categories={categories} />} />
            <Route path="/category/:categoryName" element={<Category />} />
            <Route path="/search" element={<SearchResults />} />
            <Route path="/book/:isbn" element={<BookDetail />} />
            <Route path="/library" element={<MyLibrary />} />
            <Route path="/save-for-later" element={<SaveForLater />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;