def chunk_text(text: str, chunk_size: int = 1500, chunk_overlap: int = 300) -> list[str]:
    """
    Splits long text into smaller chunks with overlap for LLM processing.
    """
    if not text:
        return []
        
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - chunk_overlap
    
    return chunks
