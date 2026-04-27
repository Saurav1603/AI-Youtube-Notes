from youtube_transcript_api import YouTubeTranscriptApi
import traceback

print("Methods in YouTubeTranscriptApi:", dir(YouTubeTranscriptApi))

try:
    print("Testing get_transcript...")
    print(YouTubeTranscriptApi.get_transcript('w28D1WIlluU'))
except Exception:
    traceback.print_exc()

try:
    print("Testing list()...")
    res = YouTubeTranscriptApi.list('w28D1WIlluU')
    print([vars(t) if hasattr(t, '__dict__') else t for t in res])
except Exception:
    traceback.print_exc()
