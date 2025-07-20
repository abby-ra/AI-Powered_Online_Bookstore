import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-8 mt-16">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">AI Bookstore</h3>
            <p className="text-gray-300">
              Your intelligent companion for discovering and reading amazing books.
            </p>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li><a href="/" className="text-gray-300 hover:text-white">Home</a></li>
              <li><a href="/categories" className="text-gray-300 hover:text-white">Categories</a></li>
              <li><a href="/search" className="text-gray-300 hover:text-white">Search</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact</h3>
            <p className="text-gray-300">
              Email: info@aibookstore.com<br />
              Phone: (555) 123-4567
            </p>
          </div>
        </div>
        <div className="border-t border-gray-600 mt-8 pt-4 text-center">
          <p className="text-gray-300">
            © 2024 AI Bookstore. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
