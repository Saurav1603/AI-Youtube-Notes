import React, { useState } from 'react';
import { generateNotes } from './api';
import InputBox from './components/InputBox';
import NotesDisplay from './components/NotesDisplay';
import { BookOpen, AlertCircle, Sparkles } from 'lucide-react';

function App() {
  const [loading, setLoading] = useState(false);
  const [notes, setNotes] = useState(null);
  const [error, setError] = useState(null);

  const fetchNotes = async (url) => {
    setLoading(true);
    setError(null);
    setNotes(null);

    try {
      const response = await generateNotes(url);
      if (response.success && response.notes) {
        setNotes(response.notes);
      } else {
        setError(response.error || "Failed to generate notes based on the provided URL.");
      }
    } catch (err) {
      setError(err.message || 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-mesh flex flex-col font-sans animate-gradient-xy bg-[length:400%_400%] transition-all duration-700 relative overflow-hidden print:bg-white print:bg-none">
      {/* Decorative background elements */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none print:hidden">
        <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-blob"></div>
        <div className="absolute top-[20%] right-[-10%] w-96 h-96 bg-blue-300 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-[-20%] left-[20%] w-96 h-96 bg-pink-400 rounded-full mix-blend-multiply filter blur-3xl opacity-50 animate-blob animation-delay-4000"></div>
      </div>

      {/* Header */}
      <header className="sticky top-0 z-50 glassmorphism border-b border-white/40 print:hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3 group cursor-pointer">
            <div className="bg-gradient-to-br from-indigo-500 to-purple-600 p-2.5 rounded-xl shadow-lg ring-2 ring-white/50 group-hover:scale-105 transition-transform duration-300">
              <BookOpen className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-indigo-900">
              YouTube Notes AI
            </h1>
          </div>
          <div className="flex items-center space-x-2 text-sm font-semibold bg-white/50 px-4 py-2 rounded-full border border-white/60 shadow-sm text-indigo-700 backdrop-blur-md">
            <Sparkles className="w-4 h-4" />
            <span>Powered by Gemini 2.5</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24 flex flex-col items-center z-10 print:py-0">
        
        <div className="text-center mb-10 w-full max-w-3xl animate-in fade-in slide-in-from-bottom-4 duration-700 print:hidden">
          <div className="inline-flex items-center space-x-2 bg-indigo-50/80 backdrop-blur-sm border border-indigo-100 px-4 py-1.5 rounded-full text-indigo-600 font-medium text-sm mb-6 shadow-sm">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-indigo-500"></span>
            </span>
            <span>AI-Powered Summarization</span>
          </div>
          <h2 className="text-4xl md:text-6xl font-extrabold text-gray-900 mb-6 tracking-tight leading-tight">
            Turn Any <span className="bg-clip-text text-transparent bg-gradient-to-r from-red-500 to-pink-600">YouTube Video</span> into Study Notes
          </h2>
          <p className="text-lg md:text-xl text-gray-700 max-w-2xl mx-auto font-medium opacity-80 leading-relaxed">
            Instantly generate structured summaries, key points, and important concepts from lengthy lectures or tutorials with just one click.
          </p>
        </div>

        <div className="w-full animate-in fade-in slide-in-from-bottom-8 duration-700 delay-150 print:hidden">
          <InputBox onSubmit={fetchNotes} isLoading={loading} />
        </div>

        {/* Error State */}
        {error && (
          <div className="mt-8 p-5 glass-panel bg-red-50/80 border border-red-200 rounded-2xl max-w-2xl w-full flex items-start space-x-4 text-red-700 animate-in fade-in zoom-in duration-300 shadow-xl print:hidden">
            <div className="bg-red-100 p-2 rounded-full">
              <AlertCircle className="w-6 h-6 flex-shrink-0 text-red-600" />
            </div>
            <div>
              <h3 className="font-bold text-lg">Action Failed</h3>
              <p className="text-sm mt-1 text-red-600/90 font-medium">{error}</p>
            </div>
          </div>
        )}

        {/* Results */}
        {!loading && notes && (
          <div className="w-full mt-12 animate-in fade-in slide-in-from-bottom-12 duration-700 delay-300 print:mt-0">
            <NotesDisplay notes={notes} />
          </div>
        )}

      </main>
      
      <footer className="py-6 glassmorphism border-t border-white/40 mt-auto z-10 w-full print:hidden">
          <div className="max-w-7xl mx-auto px-4 text-center text-sm font-medium text-gray-600">
              Built using React, Tailwind & FastAPI.
          </div>
      </footer>
    </div>
  );
}

export default App;
