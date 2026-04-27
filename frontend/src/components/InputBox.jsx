import React, { useState } from 'react';
import { Video, Search, Loader2 } from 'lucide-react';

const InputBox = ({ onSubmit, isLoading }) => {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim()) {
      onSubmit(url.trim());
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto mt-4 px-2">
      <form onSubmit={handleSubmit} className="relative flex items-center glassmorphism bg-white/60 p-2 rounded-2xl md:rounded-full overflow-hidden transition-all duration-300 focus-within:ring-4 focus-within:ring-indigo-300/50 shadow-xl hover:shadow-2xl">
        <div className="pl-6 pr-3 text-gray-500 transition-transform duration-300 hover:scale-110">
          <div className="bg-red-100 p-2.5 rounded-full">
             <Video className="w-5 h-5 text-red-600" />
          </div>
        </div>
        <input
          type="url"
          placeholder="Paste YouTube Video URL here..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="w-full py-4 px-2 text-lg font-medium text-gray-800 outline-none bg-transparent placeholder-gray-500"
          required
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !url.trim()}
          className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold py-4 px-8 md:px-10 mr-1 rounded-xl md:rounded-full hover:from-indigo-500 hover:to-purple-500 transition-all duration-300 shadow-md hover:shadow-lg disabled:from-indigo-300 disabled:to-purple-300 disabled:shadow-none disabled:cursor-not-allowed flex items-center justify-center space-x-2 min-w-[180px]"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-6 h-6 animate-spin" />
              <span className="text-sm md:text-base hidden sm:inline">Generating...</span>
            </>
          ) : (
            <>
              <Search className="w-5 h-5" />
              <span className="text-sm md:text-base hidden sm:inline">Generate Notes</span>
            </>
          )}
        </button>
      </form>
      <div className="mt-6 flex items-center justify-center space-x-2 text-sm font-semibold text-gray-600">
        <span className="block w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
        <p>Works best with videos that have closed captions available</p>
      </div>
    </div>
  );
};

export default InputBox;
