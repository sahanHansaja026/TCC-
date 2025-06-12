from youtube_transcript_api import YouTubeTranscriptApi

def get_youtube_transcript(video_id, language='en'):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        # Try to find the desired language, or fall back to any available transcript
        transcript = transcript_list.find_transcript([language])
        # If a specific language is not found, you might want to try other available languages
        # or simply use the first available one:
        # transcript = transcript_list.find_generated_transcript([language]) or transcript_list.find_manually_created_transcript([language]) or transcript_list.get_transcript()

        full_transcript = " ".join([entry['text'] for entry in transcript.fetch()])
        return full_transcript
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

video_id = "dQw4w9WgXcQ" # Replace with your YouTube video ID
transcript_text = get_youtube_transcript(video_id)

if transcript_text:
    print("Transcript:")
    print(transcript_text)
else:
    print("Could not retrieve transcript.")