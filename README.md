# AI Employee for Therapists

This project is a mobile application that serves as an AI-powered assistant for therapists and their patients. The application provides a chatbot interface for various tasks, including appointment scheduling, session note-taking, session summaries, billing/payments, and AI-assisted journaling.

## Project Structure

- `frontend/`: Contains the source code for the React Native mobile application.
- `backend/`: Contains the source code for the Python-based backend server.

## Features

- **Appointment Scheduling:** Allows patients to schedule appointments with their therapists.
- **Session Note-Taking:** Enables therapists to take notes during sessions.
- **Session Summaries:** Provides AI-generated summaries of therapy sessions.
- **Billing and Payments:** Handles billing and payment processing.
- **AI-Assisted Journaling:** Offers a journaling feature with AI-powered assistance and feedback.

## Technology Stack

- **Frontend:** React Native
- **Backend:** Python (with Flask/Django), and a natural language processing library (e.g., spaCy, NLTK, or a transformer-based model).
- **Database:** TBD

## Logging & Health Checks

### Development

- Start the backend with `python backend.py`.
- Logs are emitted as JSON to the console and saved to `backend.log`. View them with `tail -f backend.log`.
- Check service health with `curl http://localhost:5000/health`.

### Production

- Run the server with `gunicorn backend:app`.
- Logs continue to stream in JSON format to stdout and `backend.log`.
- Health checks are available at `GET /health` on the deployed host.
