import { Link } from 'react-router-dom';

export default function Home({ categories }) {
  const featuredCategories = categories.slice(0, 6);

  return (
    <div>
      <section className="mb-12">
        <div className="bg-indigo-800 text-white py-16 px-4 rounded-lg">
          <div className="container mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">Discover Your Next Favorite Book</h1>
            <p className="text-xl mb-8">AI-powered recommendations tailored just for you</p>
          </div>
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Browse Categories</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {featuredCategories.map((category) => (
            <Link
              key={category}
              to={`/category/${category.toLowerCase().replace(/\s+/g, '-')}`}
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition text-center"
            >
              <div className="text-indigo-600 font-medium">{category}</div>
            </Link>
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-bold mb-6">Editor's Picks</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
          {/* These would be populated with actual books from an API */}
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
              <div className="bg-gray-200 h-48"></div>
              <div className="p-4">
                <h3 className="font-bold text-lg mb-1">Book Title {i}</h3>
                <p className="text-gray-600 text-sm">Author Name</p>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}