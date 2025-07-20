import React from 'react';

const Category = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Book Categories</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-2">Fiction</h2>
          <p className="text-gray-600">Explore the world of imagination</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-2">Non-Fiction</h2>
          <p className="text-gray-600">Learn from real experiences</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-2">Mystery</h2>
          <p className="text-gray-600">Solve puzzles and uncover secrets</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-2">Romance</h2>
          <p className="text-gray-600">Stories of love and relationships</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-2">Science Fiction</h2>
          <p className="text-gray-600">Journey to the future and beyond</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-2">Fantasy</h2>
          <p className="text-gray-600">Enter magical worlds</p>
        </div>
      </div>
    </div>
  );
};

export default Category;
