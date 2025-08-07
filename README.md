# LinkedIn AI Agent

This project is a full-stack application designed to automate LinkedIn content creation and scheduling. It uses AI to analyze user profiles, generate engaging posts, and post them to LinkedIn at scheduled times.

## Features

*   **LinkedIn Authentication:** Securely authenticates users with their LinkedIn accounts using OAuth 2.0.
*   **Profile Analysis:** Analyzes user profiles, including skills, experience, and interests, to generate a professional summary.
*   **AI-Powered Content Generation:** Leverages OpenAI's GPT-4o with LangChain to create relevant and engaging LinkedIn posts based on user profiles and industry trends.
*   **Post Scheduling:** Allows users to schedule posts to be published on their LinkedIn profiles at specific times.
*   **Performance Analytics:** Tracks the performance of posted content, providing insights into engagement and reach.

## Technologies Used

### Backend

*   **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
*   **Uvicorn:** An ASGI server for running FastAPI applications.
*   **LangChain:** A framework for developing applications powered by language models.
*   **OpenAI:** Used for generating AI-powered content.
*   **PostgreSQL:** An open-source object-relational database system.
*   **Redis:** An in-memory data structure store, used for caching.
*   **Docker:** For containerizing the application.

### Frontend

*   **React:** A JavaScript library for building user interfaces.
*   **Tailwind CSS:** A utility-first CSS framework for rapid UI development.

## Getting Started

### Prerequisites

*   Python 3.7+
*   Node.js and npm
*   PostgreSQL
*   Redis
*   Docker (optional)

### Installation

**Backend**

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/linkedin-ai-agent.git
    cd linkedin-ai-agent/backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Set up the environment variables in a `.env` file:
    ```
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=localhost
    DB_PORT=5432
    REDIS_HOST=localhost
    REDIS_PORT=6379
    LINKEDIN_CLIENT_ID=your_linkedin_client_id
    LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
    OPENAI_API_KEY=your_openai_api_key
    ```
5.  Run the application:
    ```bash
    uvicorn main:app --reload
    ```

**Frontend**

1.  Navigate to the frontend directory:
    ```bash
    cd ../frontend
    ```
2.  Install the dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm start
    ```

## API Endpoints

*   `GET /auth/linkedin`: Initiates the LinkedIn OAuth 2.0 authentication process.
*   `GET /callback`: Handles the callback from LinkedIn after authentication.
*   `POST /analyze_profile`: Analyzes a user's profile.
*   `POST /generate_post`: Generates a LinkedIn post based on a user's profile.
*   `POST /schedule_post`: Schedules a post to be published on LinkedIn.
*   `GET /analytics/{user_id}`: Retrieves analytics for a user's posts.

## Project Structure

```
.
├── backend
│   ├── main.py
│   ├── analytics.py
│   ├── content_generator.py
│   ├── linkedin_api.py
│   └── models.py
├── frontend
│   ├── src
│   │   ├── components
│   │   │   ├── Auth.js
│   │   │   ├── PostGenerator.js
│   │   │   └── ProfileForm.js
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```
