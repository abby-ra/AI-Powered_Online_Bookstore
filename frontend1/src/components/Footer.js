import { Link } from 'react-router-dom';

function Footer() {
  return (
    <footer className="bg-gray-800 text-white mt-12">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About Section */}
          <div>
            <h3 className="text-lg font-semibold mb-4">BookStore AI</h3>
            <p className="text-gray-300 text-sm leading-relaxed">
              Your intelligent companion for discovering amazing books. 
              Powered by AI to help you find your next great read from our vast collection.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li><Link to="/" className="text-gray-300 hover:text-white transition">Home</Link></li>
              <li><Link to="/category/Romance" className="text-gray-300 hover:text-white transition">Romance</Link></li>
              <li><Link to="/category/Fantasy" className="text-gray-300 hover:text-white transition">Fantasy</Link></li>
              <li><Link to="/category/Mystery" className="text-gray-300 hover:text-white transition">Mystery</Link></li>
              <li><Link to="/category/Science Fiction" className="text-gray-300 hover:text-white transition">Science Fiction</Link></li>
            </ul>
          </div>

          {/* Categories */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Popular Genres</h3>
            <ul className="space-y-2 text-sm">
              <li><Link to="/category/Thriller" className="text-gray-300 hover:text-white transition">Thriller</Link></li>
              <li><Link to="/category/Historical Fiction" className="text-gray-300 hover:text-white transition">Historical Fiction</Link></li>
              <li><Link to="/category/Horror" className="text-gray-300 hover:text-white transition">Horror</Link></li>
              <li><Link to="/category/Non-Fiction" className="text-gray-300 hover:text-white transition">Non-Fiction</Link></li>
              <li><Link to="/category/Poetry" className="text-gray-300 hover:text-white transition">Poetry</Link></li>
            </ul>
          </div>

          {/* Features */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Features</h3>
            <ul className="space-y-2 text-sm text-gray-300">
              <li>🤖 AI-Powered Recommendations</li>
              <li>🔍 Smart Search</li>
              <li>📚 Vast Book Collection</li>
              <li>🎯 Personalized Suggestions</li>
              <li>📱 Mobile Friendly</li>
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-sm text-gray-400">
          <p>&copy; 2025 BookStore AI. All rights reserved. Built with React & Flask.</p>
          <p className="mt-2">
            <span className="inline-block mx-2">📊 {(271353).toLocaleString()} Books</span>
            <span className="inline-block mx-2">🧠 AI-Powered</span>
            <span className="inline-block mx-2">⚡ Fast Search</span>
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
