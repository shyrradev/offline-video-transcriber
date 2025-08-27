
# 🎥 Offline Video Transcriber

An **offline video transcription app** built with [OpenAI Whisper](https://github.com/openai/whisper), [MoviePy](https://zulko.github.io/moviepy/), and [Streamlit](https://streamlit.io/).  
Easily convert **video to text** locally on your own machine — **no APIs, no cloud costs, 100% offline**.

---

## ✨ Features
- 🖥️ **Runs locally** using your own system resources  
- 🎙️ Extracts **audio from video files** (MP4, AVI, MOV, MKV, WMV)  
- 🤖 Transcribes audio using **OpenAI Whisper** models (tiny → large)  
- 📊 Provides **processing stats**: time, word count, character count  
- 💾 Download transcription results in **TXT** or **detailed format**  
- 🖼️ Simple, interactive **Streamlit web app** interface  

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/offline-video-transcriber.git
cd offline-video-transcriber

2. Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows

3. Install dependencies
pip install -r requirements.txt


Make sure ffmpeg is installed on your system (required by MoviePy & Whisper).

On Ubuntu/Debian: sudo apt install ffmpeg

On macOS (Homebrew): brew install ffmpeg

On Windows: Download from ffmpeg.org

▶️ Usage

Run the Streamlit app:

streamlit run app.py


Then open the local URL (usually http://localhost:8501) in your browser.

⚙️ Settings

Choose Whisper model size (tiny, base, small, medium, large)

Larger models are more accurate but slower and need more RAM/VRAM

Maximum video file size: 200 MB

📄 Example Output

Transcribed text from your video

Processing statistics (time, word count, character count)

Download options:

transcription.txt (plain text)

transcription_detailed.txt (with metadata)

🛠️ Tech Stack

Python 3.8+

Streamlit
 (UI)

MoviePy
 (audio extraction)

Whisper
 (speech-to-text engine)

📦 Requirements

Create a requirements.txt with:

streamlit
moviepy
openai-whisper

🔒 Privacy & Security

100% offline: nothing leaves your machine

No API keys, no internet required once installed

Your files and transcriptions remain local and private

🤝 Contributing

Contributions are welcome!

Report issues

Suggest improvements

Submit pull requests

📜 License

MIT License – free to use and modify.

🌟 Acknowledgments

OpenAI Whisper

Streamlit

MoviePy


---

👉 This README covers **everything recruiters/users expect**: setup, usage, features, security (offline emphasis), and SEO-friendly terms like *offline video transcription*, *local Whisper app*, *no API required*.  

Do you want me to also generate a **ready-to-use `requirements.txt`** for your repo so people can `pip install -r requirements.txt` without issues?

