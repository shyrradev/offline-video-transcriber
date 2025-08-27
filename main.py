import os
import tempfile
import streamlit as st
from moviepy import VideoFileClip
import whisper
from pathlib import Path
import time

class VideoTranscriber:
    def __init__(self):
        self.whisper_model = None
    
    def load_whisper_model(self, model_size="base"):
        """Load Whisper model for transcription"""
        try:
            self.whisper_model = whisper.load_model(model_size)
            return True
        except Exception as e:
            st.error(f"Error loading Whisper model: {str(e)}")
            return False
    
    def extract_audio_from_video(self, video_path, audio_path):
        """Extract audio from video file"""
        try:
            video_clip = VideoFileClip(video_path)
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(audio_path, logger=None)
            video_clip.close()
            audio_clip.close()
            return True
        except Exception as e:
            st.error(f"Error extracting audio: {str(e)}")
            return False
    
    def transcribe_with_whisper(self, audio_path):
        """Transcribe audio using OpenAI Whisper"""
        try:
            if self.whisper_model is None:
                if not self.load_whisper_model():
                    return None
            
            result = self.whisper_model.transcribe(audio_path)
            return result["text"]
        except Exception as e:
            st.error(f"Error with Whisper transcription: {str(e)}")
            return None
    
    def transcribe_with_whisper_only(self, audio_path, model_size="base"):
        """Transcribe audio using OpenAI Whisper (simplified)"""
        try:
            if self.whisper_model is None:
                if not self.load_whisper_model(model_size):
                    return None
            
            result = self.whisper_model.transcribe(audio_path)
            return result["text"]
        except Exception as e:
            st.error(f"Error with Whisper transcription: {str(e)}")
            return None
    
    def process_video(self, video_file, model_size="base"):
        """Main method to process video and return transcription"""
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_video:
            tmp_video.write(video_file.read())
            video_path = tmp_video.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_audio:
            audio_path = tmp_audio.name
        
        try:
            # Extract audio from video
            st.info("Extracting audio from video...")
            if not self.extract_audio_from_video(video_path, audio_path):
                return None
            
            # Transcribe with Whisper
            st.info(f"Transcribing with Whisper ({model_size} model)...")
            if self.whisper_model is None:
                if not self.load_whisper_model(model_size):
                    return None
            transcription = self.transcribe_with_whisper_only(audio_path, model_size)
            
            return transcription
            
        finally:
            # Cleanup temporary files
            try:
                os.unlink(video_path)
                os.unlink(audio_path)
            except:
                pass

def main():
    st.set_page_config(
        page_title="Video Transcription App",
        page_icon="🎥",
        layout="wide"
    )
    
    st.title("🎥 Video Transcription App")
    st.markdown("Upload a video file and get its transcription using AI-powered speech recognition.")
    
    # Initialize transcriber
    if 'transcriber' not in st.session_state:
        st.session_state.transcriber = VideoTranscriber()
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        model_size = st.selectbox(
            "Whisper Model Size",
            ["tiny", "base", "small", "medium", "large"],
            index=1,
            help="Larger models are more accurate but slower and use more memory."
        )
        
        st.markdown("---")
        st.markdown("""
        ### 📝 Supported Formats
        - **Video**: MP4, AVI, MOV, MKV, WMV
        - **Max Size**: 200MB per file
        
        ### 🚀 Tips
        - **Whisper** works offline and is very accurate
        - Larger models are slower but more accurate
        - Clear audio gives better results
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Video")
        
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'avi', 'mov', 'mkv', 'wmv'],
            help="Upload a video file to transcribe its audio content"
        )
        
        if uploaded_file is not None:
            # Display video info
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.info(f"📊 File size: {uploaded_file.size / (1024*1024):.2f} MB")
            
            # Show video preview
            st.video(uploaded_file)
            
            # Transcribe button
            if st.button("🎯 Start Transcription", type="primary"):
                if uploaded_file.size > 200 * 1024 * 1024:  # 200MB limit
                    st.error("❌ File too large. Please upload a file smaller than 200MB.")
                else:
                    with st.spinner("Processing video... This may take a while."):
                        start_time = time.time()
                        
                        transcription = st.session_state.transcriber.process_video(
                            uploaded_file, 
                            model_size
                        )
                        
                        end_time = time.time()
                        processing_time = end_time - start_time
                        
                        if transcription:
                            st.session_state.transcription = transcription
                            st.session_state.processing_time = processing_time
                            st.success(f"✅ Transcription completed in {processing_time:.1f} seconds!")
                        else:
                            st.error("❌ Failed to transcribe the video. Please try again.")
    
    with col2:
        st.header("📄 Transcription Results")
        
        if 'transcription' in st.session_state and st.session_state.transcription:
            # Display transcription
            st.text_area(
                "Transcribed Text",
                value=st.session_state.transcription,
                height=400,
                help="The transcribed text from your video"
            )
            
            # Statistics
            word_count = len(st.session_state.transcription.split())
            char_count = len(st.session_state.transcription)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("⏱️ Processing Time", f"{st.session_state.processing_time:.1f}s")
            with col_b:
                st.metric("📝 Word Count", word_count)
            with col_c:
                st.metric("🔤 Character Count", char_count)
            
            # Download options
            st.markdown("---")
            st.subheader("💾 Download Options")
            
            col_d, col_e = st.columns(2)
            with col_d:
                st.download_button(
                    label="📄 Download as TXT",
                    data=st.session_state.transcription,
                    file_name="transcription.txt",
                    mime="text/plain"
                )
            
            with col_e:
                # Create formatted text with metadata
                formatted_text = f"""Video Transcription
==================
File: {uploaded_file.name if uploaded_file else 'Unknown'}
Method: Whisper ({model_size} model)
Processing Time: {st.session_state.processing_time:.1f} seconds
Word Count: {word_count}
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

Transcription:
--------------
{st.session_state.transcription}
"""
                st.download_button(
                    label="📋 Download with Info",
                    data=formatted_text,
                    file_name="transcription_detailed.txt",
                    mime="text/plain"
                )
        else:
            st.info("👆 Upload a video file and click 'Start Transcription' to see results here.")
            
            # Example placeholder
            st.markdown("""
            ### 🔍 What you'll see here:
            - **Transcribed text** from your video
            - **Processing statistics** (time, word count, etc.)
            - **Download options** for the transcription
            - **Text formatting** and editing capabilities
            """)

if __name__ == "__main__":
    main()