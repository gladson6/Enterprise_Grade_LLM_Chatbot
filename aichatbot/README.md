# Company IT Chatbot (Full Stack with Llama 3)

This project is an advanced, self-hosted chatbot for an IT company website. It uses a **Retrieval-Augmented Generation (RAG)** architecture powered by a local **Llama 3** instance to answer user queries based on internal company documents.

---

## 🚀 Features

- **Llama 3 Powered**: Utilizes the open-source Llama 3 model running locally via [Ollama](https://ollama.com) for state-of-the-art conversational AI.
- **RAG Architecture**: Provides answers based on your private documents, ensuring accuracy and reducing hallucinations.
- **Fully Self-Hosted**: Complete control over your data and models. No third-party API costs.
- **Clean Architecture**: Backend (FastAPI) and frontend (React) are separated for scalability.
- **Modern UI**: Responsive, user-friendly chat interface with Tailwind CSS and dark mode.
- **Lead Capture**: Integrated form to capture user details when the bot cannot answer. Option for email notifications.
- **Easy Document Updates**: Add new documents to the `docs/` folder and rebuild the knowledge base with a single command.

---

## 📋 System Prerequisites

Before starting, ensure you have installed:

- **Ollama** → Required to run the Llama 3 model locally. [Download here](https://ollama.com).
- **Node.js & npm** → Required for the React frontend. [Download here](https://nodejs.org).
- **Python & pip** → Required for the FastAPI backend. [Download here](https://python.org).

---

## ⚙️ Step 1: Set Up Llama 3 with Ollama

1. **Install Ollama**
   - Download and install Ollama for macOS, Windows, or Linux.

2. **Pull the Llama 3 Model**
   ```bash
   ollama pull llama3:8b-instruct
   ```

3. **Verify the Model**
   ```bash
   ollama list
   ```
   You should see `llama3:8b-instruct` listed. The model will be served at `http://localhost:11434`.

---

## ⚙️ Step 2: Backend Setup

1. **Navigate & Install Dependencies**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   ```
   The defaults should work with Ollama. Edit `.env` if needed.

3. **Add Documents**
   - Place `.pdf`, `.txt`, or `.md` files into the `docs/` directory.

4. **Build the Vector Store**
   ```bash
   python backend/app/db/vector_store.py
   ```
   Run this whenever you update your documents.

5. **Run Backend Server**
   ```bash
   uvicorn main:app --reload
   ```
   API will be available at `http://127.0.0.1:8000`.

---

## 🖥️ Step 3: Frontend Setup

1. **Navigate & Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure Tailwind CSS**
   ```bash
   npx tailwindcss init -p
   ```
   - Update `tailwind.config.js` to scan project files.
   - Add Tailwind directives to `src/index.css`.

3. **Run Development Server**
   ```bash
   npm start
   ```
   Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## ✅ You're All Set!

- Ollama is serving the Llama 3 model.
- Backend is running on **port 8000**.
- Frontend is running on **port 3000**.

Open [http://localhost:3000](http://localhost:3000) and start chatting with your **private, Llama 3-powered IT chatbot**!
