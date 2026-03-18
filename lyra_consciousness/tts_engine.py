"""
TTS Engine: High-fidelity neural text-to-speech using Piper
Streams audio chunks alongside text for seamless voice integration
"""

import subprocess
import os
import json
import tempfile
from pathlib import Path
import base64

class TTSEngine:
    def __init__(self, voice_model="en_US-lessac-medium", enable_cache=True):
        """
        Initialize Piper TTS engine.
        
        voice_model: One of Piper's high-quality voices
            - en_US-lessac-medium (female, clear)
            - en_US-libritts-high (mix of speakers)
            - en_US-ryan-medium (male, natural)
            - en_US-glow-tts (high-quality)
        """
        self.voice_model = voice_model
        self.enable_cache = enable_cache
        self.cache_dir = Path(".tts_cache")
        self.piper_available = self._check_piper_available()
        
        if self.cache_dir and self.enable_cache:
            self.cache_dir.mkdir(exist_ok=True)
        
        if not self.piper_available:
            print("⚠️ Piper TTS not installed. Install with: pip install piper-tts")
            print("   Or download from: https://github.com/rhasspy/piper")
    
    def _check_piper_available(self):
        """Check if piper is available on system"""
        try:
            result = subprocess.run(
                ["which", "piper"],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False
    
    def synthesize_to_bytes(self, text: str) -> bytes:
        """
        Synthesize text to audio bytes (WAV format).
        Returns audio data or empty bytes if TTS unavailable.
        """
        if not text or len(text.strip()) == 0:
            return b""
        
        # Check cache first
        if self.enable_cache:
            cached = self._get_cached_audio(text)
            if cached:
                return cached
        
        try:
            if self.piper_available:
                return self._synthesize_piper(text)
            else:
                # Fallback: return empty if piper unavailable
                return b""
        except Exception as e:
            print(f"TTS Error: {e}")
            return b""
    
    def _synthesize_piper(self, text: str) -> bytes:
        """Use system piper to synthesize speech"""
        try:
            # Use Piper via command line
            # Piper outputs WAV format to stdout
            result = subprocess.run(
                [
                    "piper",
                    "--model", self.voice_model,
                    "--output-file", "-"  # stdout
                ],
                input=text.encode('utf-8'),
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0:
                audio_bytes = result.stdout
                # Cache it
                if self.enable_cache:
                    self._cache_audio(text, audio_bytes)
                return audio_bytes
            else:
                print(f"Piper error: {result.stderr.decode()}")
                return b""
        except subprocess.TimeoutExpired:
            print("Piper TTS timeout")
            return b""
        except Exception as e:
            print(f"Piper synthesis failed: {e}")
            return b""
    
    def _get_cached_audio(self, text: str) -> bytes:
        """Retrieve cached audio for text if available"""
        if not self.cache_dir:
            return None
        
        cache_file = self.cache_dir / f"{hash(text)}.wav"
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    return f.read()
            except:
                pass
        return None
    
    def _cache_audio(self, text: str, audio_bytes: bytes):
        """Cache audio bytes for future use"""
        if not self.cache_dir:
            return
        
        try:
            cache_file = self.cache_dir / f"{hash(text)}.wav"
            with open(cache_file, 'wb') as f:
                f.write(audio_bytes)
        except:
            pass
    
    def stream_synthesis(self, text: str, chunk_size=1024):
        """
        Stream audio synthesis in chunks.
        Yields: tuples of (chunk_type, data)
            - ("audio", audio_bytes)
        """
        # For streaming, we synthesize the whole text but yield in chunks
        audio_bytes = self.synthesize_to_bytes(text)
        
        if audio_bytes:
            # Yield in chunks for streaming
            for i in range(0, len(audio_bytes), chunk_size):
                chunk = audio_bytes[i:i+chunk_size]
                yield ("audio", chunk)
    
    def get_voice_info(self):
        """Return info about current voice model"""
        return {
            "model": self.voice_model,
            "type": "piper-tts",
            "quality": "high-fidelity neural",
            "available": self.piper_available,
            "cached_entries": len(list(self.cache_dir.glob("*.wav"))) if self.cache_dir else 0
        }
