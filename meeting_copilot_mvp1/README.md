# meeting_copilot_mvp1

A local-first desktop meeting copilot MVP for Windows-first usage during Zoom, Teams, Google Meet, or any app that outputs local audio. MVP1 intentionally avoids official meeting APIs and instead uses local loopback capture, local transcription, and local summarization.

## Features

- Fully local AI pipeline (Ollama + faster-whisper).
- Windows-first system audio loopback capture, optional mic mixing.
- Incremental transcription with timestamps and estimated speaker labels.
- Rolling summaries every 60 seconds plus manual **Summarize Now**.
- Structured meeting state for decisions, action items, risks, and questions.
- SQLite persistence for sessions, chunks, summaries, and final report metadata.
- Export final outputs as Markdown, JSON, and polished PDF.
- Resilient runtime behavior with UI-level status and error visibility.

## Architecture

```mermaid
flowchart LR
    UI[Streamlit Dashboard] --> CORE[MeetingCopilotApp Orchestrator]
    CORE --> AUDIO[AudioCaptureService\n(soundcard loopback + optional mic)]
    CORE --> STT[TranscriptionService\n(faster-whisper)]
    CORE --> SUMM[SummarizationService\n(Ollama llama3.2)]
    CORE --> STATE[MeetingState Aggregator]
    CORE --> DB[(SQLite)]
    CORE --> REPORT[ReportGenerator\n(JSON/MD/PDF)]
    SUMM --> PROMPTS[Prompt Templates]
```

## Project Structure

```text
meeting_copilot_mvp1/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   ├── services/
│   │   ├── audio_capture.py
│   │   ├── transcription.py
│   │   ├── summarization.py
│   │   ├── state_manager.py
│   │   ├── report_generator.py
│   │   └── ollama_client.py
│   ├── prompts/
│   │   ├── live_summary.txt
│   │   └── final_report.txt
│   └── utils/
│       ├── logging_utils.py
│       └── time_utils.py
├── ui/
│   └── streamlit_app.py
├── data/
│   ├── meetings.db
│   └── exports/
├── tests/
├── requirements.txt
├── .env.example
├── README.md
└── run.ps1
```

## Prerequisites

- Python 3.11+
- Windows 10/11 recommended for loopback path
- [Ollama](https://ollama.com/) installed and running locally

## Setup

1. Clone and enter project directory.
2. Create a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Create environment file:
   ```powershell
   copy .env.example .env
   ```

## Install and prepare Ollama

1. Install Ollama from official site.
2. Start Ollama service.
3. Pull default model:
   ```powershell
   ollama pull llama3.2
   ```
4. Verify:
   ```powershell
   ollama list
   ```

## Run the app

### Option A: one-step PowerShell script

```powershell
./run.ps1 -InstallDeps
```

### Option B: manual

```powershell
$env:PYTHONPATH='.'
streamlit run ui/streamlit_app.py
```

## Using the UI

1. Click **Check Dependencies**.
2. Enter meeting title.
3. Click **Start Meeting Session**.
4. Watch live transcript and rolling summary panes.
5. Use **Summarize Now** for ad-hoc updates.
6. Click **Stop Meeting Session** when done.
7. Click **Export PDF / Markdown / JSON**.

## Troubleshooting

- **Ollama disconnected**: Ensure `ollama serve` is running and `OLLAMA_BASE_URL` is correct.
- **No loopback device**: Audio driver may not expose loopback; app shows warning and cannot capture system audio.
- **No microphone**: If optional mic is enabled and unavailable, app falls back to system audio only.
- **Transcription inactive**: `faster-whisper` may be missing or model failed to load.
- **PDF export failure**: Verify write access to `data/exports`.
- **Empty summaries**: Ensure transcript chunks are being produced and Ollama model exists.

## Known MVP1 limitations

- No official Zoom/Teams/Google Meet APIs.
- Speaker labels are estimated from mixed audio segments only (`Speaker 1`, `Speaker 2`, `Unknown Speaker`).
- True participant attribution is not guaranteed without richer channel separation.
- On some Windows setups, simultaneous loopback + mic can be unstable; app prioritizes loopback.

## MVP2 roadmap

- Official Zoom/Teams/Google Meet APIs for participant-level events.
- Better diarization and optional voice profile mapping.
- Real-time assistant drafting in-meeting chat responses.
- Cross-platform packaging (macOS/Linux) and native desktop wrapper.
- Multi-session analytics and search.

