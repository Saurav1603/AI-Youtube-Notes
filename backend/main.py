from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import notes

app = FastAPI(
    title="YouTube Notes Generator API",
    description="API for generating structured notes from YouTube videos using Gemini 2.5 Flash",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, restrict this to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(notes.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to YouTube Notes Generator API"}
