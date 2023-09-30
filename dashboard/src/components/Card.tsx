import React from 'react';

interface CardProps {
  message: string;
}

const Card: React.FC<CardProps> = ({ message }) => {
  return (
    <div className="w-full p-4 border-2">
      <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition duration-300 ease-in-out transform hover:-translate-y-1 relative">
        <div className="px-3 py-4 ">
          <p className="text-lg font-semibold">{message}</p>
        </div>
        <div className="px-3 py-3 hidden">
          <p className="text-lg font-semibold">{message}</p>
        </div>
      </div>
    </div>
  );
};

export default Card;
