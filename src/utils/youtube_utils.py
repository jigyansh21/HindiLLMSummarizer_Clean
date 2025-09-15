"""
YouTube Processing Utilities
Handles YouTube transcript extraction and summarization
"""

import asyncio
import re
from typing import Dict, Any, Literal, Optional
from urllib.parse import urlparse, parse_qs

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import TextFormatter
    YOUTUBE_API_AVAILABLE = True
except ImportError:
    print("youtube-transcript-api not installed. YouTube functionality will be limited.")
    YouTubeTranscriptApi = None
    TextFormatter = None
    YOUTUBE_API_AVAILABLE = False

class YouTubeProcessor:
    def __init__(self):
        self.formatter = TextFormatter() if TextFormatter else None
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID from URL"""
        try:
            # Handle various YouTube URL formats
            patterns = [
                r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
                r'youtube\.com\/v\/([^&\n?#]+)',
                r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
            
            return None
            
        except Exception:
            return None
    
    async def get_transcript(self, video_id: str, language: str = "en") -> str:
        """Get transcript for YouTube video"""
        if not YOUTUBE_API_AVAILABLE or not YouTubeTranscriptApi:
            raise Exception("YouTube transcript API not available. Please install youtube-transcript-api: pip install youtube-transcript-api")
        
        try:
            # Create an instance of YouTubeTranscriptApi
            api = YouTubeTranscriptApi()
            
            # Try to get transcript in specified language first
            try:
                transcript = api.fetch(video_id, languages=[language])
            except Exception as lang_error:
                print(f"Failed to get transcript in {language}: {lang_error}")
                # Fallback to any available language
                try:
                    transcript = api.fetch(video_id)
                except Exception as fallback_error:
                    print(f"Failed to get transcript in any language: {fallback_error}")
                    raise Exception(f"No transcript available for this video. Error: {str(fallback_error)}")
            
            if not transcript:
                raise Exception("No transcript available for this video")
            
            # Format transcript as plain text
            if self.formatter:
                formatted_text = self.formatter.format_transcript(transcript)
            else:
                # Manual formatting if formatter not available
                formatted_text = " ".join([entry['text'] for entry in transcript])
            
            return formatted_text
            
        except Exception as e:
            raise Exception(f"Failed to get transcript: {str(e)}")
    
    async def get_video_info(self, video_id: str) -> Dict[str, Any]:
        """Get basic video information"""
        try:
            # This is a simplified version - in production you might want to use
            # the YouTube Data API for more detailed information
            return {
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "title": "YouTube Video",  # Would need YouTube Data API for actual title
                "duration": "Unknown"  # Would need YouTube Data API for actual duration
            }
        except Exception as e:
            return {
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "title": "Unknown Video",
                "error": str(e)
            }
    
    async def summarize_video(
        self, 
        url: str, 
        language: Literal["hindi", "english"] = "hindi",
        summary_length: Literal["short", "medium", "long", "auto"] = "auto"
    ) -> Dict[str, Any]:
        """Extract transcript and summarize YouTube video"""
        try:
            # Extract video ID
            video_id = self.extract_video_id(url)
            if not video_id:
                raise Exception("Invalid YouTube URL")
            
            # Get video info
            video_info = await self.get_video_info(video_id)
            
            # Get transcript
            transcript_language = "hi" if language == "hindi" else "en"
            transcript = await self.get_transcript(video_id, transcript_language)
            
            if not transcript.strip():
                raise Exception("No transcript available for this video")
            
            # Import summarizer service
            from src.core.summarizer import SummarizerService
            summarizer = SummarizerService()
            
            # Summarize the transcript
            result = await summarizer.summarize_text(
                text=transcript,
                language=language,
                summary_length=summary_length
            )
            
            # Add video information to result
            result["title"] = video_info["title"]
            result["video_id"] = video_id
            result["video_url"] = video_info["url"]
            
            return result
            
        except Exception as e:
            raise Exception(f"Failed to process YouTube video: {str(e)}")
    
    def is_valid_youtube_url(self, url: str) -> bool:
        """Check if URL is a valid YouTube URL"""
        try:
            video_id = self.extract_video_id(url)
            return video_id is not None
        except:
            return False
