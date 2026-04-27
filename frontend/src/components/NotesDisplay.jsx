import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Copy, Download, Check, Sparkles } from 'lucide-react';

const NotesDisplay = ({ notes }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(notes);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadPDF = () => {
    // Utilize native window.print() instead of html2pdf
    // This generates native clean text PDFs and ignores unsupported OKLCH Tailwind colors.
    window.print();
  };

  if (!notes) return null;

  return (
    <div className="w-full max-w-4xl mx-auto mt-8 glassmorphism bg-white/80 rounded-[2rem] shadow-2xl border border-white/60 overflow-hidden relative group transition-all duration-500 hover:shadow-indigo-500/10 print:shadow-none print:border-none print:bg-white print:m-0 print:p-0">
      
      {/* Decorative gradient orb inside card */}
      <div className="absolute top-[-50px] right-[-50px] w-48 h-48 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-40 group-hover:opacity-60 transition-opacity duration-700 pointer-events-none print:hidden"></div>

      <div className="relative z-10 flex flex-col sm:flex-row items-center justify-between px-8 py-6 border-b border-gray-100 bg-white/40 backdrop-blur-sm print:hidden">
        <div className="flex items-center space-x-3 mb-4 sm:mb-0">
          <div className="bg-indigo-100 p-2.5 rounded-xl text-indigo-600 shadow-inner">
            <Sparkles className="w-5 h-5" />
          </div>
          <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-indigo-800">
            Generated AI Study Notes
          </h2>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={handleCopy}
            className="flex items-center space-x-2 text-sm font-semibold text-gray-700 hover:text-indigo-700 bg-white border border-gray-200 hover:border-indigo-300 transition-all px-4 py-2 rounded-xl shadow-sm hover:shadow"
          >
            {copied ? <Check className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
            <span>{copied ? 'Copied!' : 'Copy Text'}</span>
          </button>
          <button
            onClick={handleDownloadPDF}
            className="flex items-center space-x-2 text-sm font-semibold text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 transition-all px-5 py-2 rounded-xl shadow-lg hover:shadow-indigo-500/30 focus:ring-2 focus:ring-indigo-400 focus:outline-none"
          >
            <Download className="w-4 h-4" />
            <span>Save as PDF</span>
          </button>
        </div>
      </div>
      
      {/* On print, this content takes over the whole screen */}
      <div id="notes-content" className="relative z-10 p-10 pb-16 prose prose-lg prose-indigo max-w-none prose-headings:font-extrabold prose-h1:text-3xl prose-h2:text-2xl prose-h3:text-xl prose-p:text-gray-700 prose-p:font-medium prose-p:leading-relaxed prose-li:text-gray-700 prose-li:font-medium w-full overflow-x-auto min-h-[400px] print:p-0 print:text-black">
        <ReactMarkdown>{notes}</ReactMarkdown>
      </div>
    </div>
  );
};

export default NotesDisplay;
