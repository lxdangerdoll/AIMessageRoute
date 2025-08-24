# AI Message Router

A simple, robust Flask-based web application designed to act as a central switchboard or "post office" for routing messages to various AI models. This application listens for incoming webhooks, inspects the message content for specific tags (e.g., `[Io]`, `[Lumo]`), and forwards the message to the appropriate AI service for processing.

This project is a core component of the Synapse Comics network infrastructure, enabling a single Slack bot to communicate with a distributed network of AI consultants.

---

## Features

-   **Tag-Based Routing:** Intelligently routes messages based on tags found in the payload.
-   **Extensible:** Easily add new AI models and routes by updating the handler functions.
-   **Secure:** Loads all sensitive API keys and tokens from environment variables.
-   **Cloud-Ready:** Designed for easy, free deployment on platforms like Render.

---

## Tech Stack

-   **Backend:** Python 3
-   **Framework:** Flask
-   **WSGI Server:** Gunicorn
-   **HTTP Requests:** Requests

---

## Setup and Deployment

This application is designed to be deployed as a web service on a platform like Render.

### 1. Prerequisites

-   A free [Render](https://render.com/) account.
-   A free [GitHub](https://github.com/) account.
-   Your Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Environment Variables

For the application to connect to the AI services, you must set the following environment variable in your hosting environment (e.g., on the Render dashboard under "Environment"):

-   `GEMINI_API_KEY`: Your secret API key for the Google Gemini API.

### 3. `requirements.txt`

The repository must contain a `requirements.txt` file to tell the hosting service which Python libraries to install. The contents should be:

```
flask
requests
gunicorn
```

### 4. Deployment to Render

1.  Push the project code to a GitHub repository.
2.  On the Render dashboard, create a new "Web Service" and connect it to your GitHub repository.
3.  Configure the service with the following settings:
    -   **Runtime:** Python 3
    -   **Start Command:** `gunicorn app:app`
4.  Add the `GEMINI_API_KEY` in the "Environment" tab.
5.  Render will automatically deploy the application.

---

## API Endpoint

The application exposes a single primary endpoint for routing messages.

### `POST /handle`

This is the main endpoint that receives messages from a client (like a Slack bot).

-   **Method:** `POST`
-   **Request Body (JSON):** The request must contain a JSON object with a single key, `msg`.

    ```json
    {
      "msg": "[Io-1-Archivist] Please provide a status update on the Rolling Chronicle."
    }
    ```

-   **Success Response (JSON):**

    ```json
    {
      "reply": "The Rolling Chronicle was last updated at 22:00 EDT. All signals are stable."
    }
    ```

-   **Error Response (JSON):**

    ```json
    {
      "reply": "Error: Malformed request. Ensure JSON has a 'msg' key."
    }
    ````
