# 🎥 YouTube Notes Generator AI

![UI Mockup or Banner placeholder](https://via.placeholder.com/1000x400.png?text=YouTube+Notes+Generator+AI)

A full-stack GenAI web application that allows users to instantly generate structured, high-quality study notes from any YouTube video. The application leverages Google's Gemini 2.5 Flash model's native multimodal capabilities to parse video URLs and automatically structure the information into clean, readable study notes.

🔗 **Live Demo:** [https://ai-youtube-notes.vercel.app/](https://ai-youtube-notes.vercel.app/)

## ✨ Features

- **Instant AI Summarization:** Paste a YouTube URL and receive comprehensive notes in seconds.
- **Structured Output:** Automatically organizes content into:
  - 📌 **Summary:** A quick overview of the video's core topic.
  - 🧠 **Key Points:** Bullet points of the most critical information.
  - 📚 **Important Concepts:** Deep dive into specific vocabulary or theories.
  - 💡 **Examples:** Practical examples extracted from the content.
- **PDF Export:** Download the generated notes beautifully formatted as a PDF directly to your device.
- **Copy to Clipboard:** One-click copy for easy pasting into Notion, Docs, or Obsidian.
- **Fully Responsive UI:** A clean, modern interface built with React 19 and Tailwind CSS v4.

## 🚀 Technology Stack

### Frontend (Client)
- **Framework:** React 19 powered by Vite
- **Styling:** Tailwind CSS v4 (Glassmorphism & Gradients)
- **Markdown:** `react-markdown` for rendering structured AI outputs
- **Exporting:** `html2pdf.js` for native PDF generation
- **Icons:** Lucide React

### Backend (Server)
- **Framework:** Python + FastAPI (ASGI via Uvicorn)
- **AI Integration:** Google Gemini 2.5 Flash (`google-generativeai`)
- **Environment:** `python-dotenv` for secure credential management

## 🛠️ Local Development

### Prerequisites
- Node.js (v18+)
- Python (3.9+)
- A Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

### 1. Clone the repository
```bash
git clone https://github.com/Saurav1603/AI-Youtube-Notes.git
cd AI-Youtube-Notes
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file inside the `backend` folder and add your Gemini API key:
```env
GEMINI_API_KEY="your_api_key_here"
```

Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
The application will be running locally at `http://localhost:5173`.

## 🌐 Deployment

This application uses a modular architecture optimized for separate cloud hosting platforms.

- **Frontend:** Deployed globally via [Vercel](https://vercel.com/) (pointing to the `frontend` directory). The `VITE_API_BASE_URL` environment variable is configured to target the production backend.
- **Backend:** Deployed via [Render](https://render.com/) utilizing the `render.yaml` configuration and `Procfile`.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Saurav1603/AI-Youtube-Notes/issues).

---

*Built with ❤️ utilizing the power of Gemini AI.*
