# PDF Chatbot

A Streamlit app that lets you ask questions about an uploaded PDF. It retrieves
relevant text from the document and uses a local Ollama model to generate
answers.

## Requirements

- Python 3.11
- [Ollama](https://ollama.com/download)
- The Ollama model `llama3.2:3b`

No OpenAI API key is required. The first use of PDF indexing may download the
`all-MiniLM-L6-v2` embedding model.

## Setup on Windows

Open PowerShell in the project folder and run:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
ollama pull llama3.2:3b
```

Make sure Ollama is running, then launch the app:

```powershell
python -m streamlit run main.py
```

Open the local URL printed by Streamlit in your browser.

## Using the app

1. Upload a PDF.
2. Select **Index PDF** and wait for indexing to finish.
3. Ask a question in the chat box.

The app uses the PDF's retrieved text as context for answers. Ollama must be
running locally, and the `llama3.2:3b` model must be available.

## Dependencies

Python package dependencies are listed in [`requirements.txt`](requirements.txt).

## Chatbot

<img width="1747" height="883" alt="Screenshot 2026-11-26 224453" src="https://github.com/user-attachments/assets/0f5cfdea-0a1e-4d2a-8b77-210289d72761" />

