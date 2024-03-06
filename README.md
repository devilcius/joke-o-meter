
# Joke-O-Meter

## Description

The Joke-O-Meter is a web application designed to entertain users by presenting them with a collection of jokes. Users can rate jokes based on their preferences, swiping right for jokes they like and left for those they do not. After evaluating a set of jokes, the application analyzes the user's preferences and assigns them a unique Jokometian character, each with its own set of traits reflecting the user's humor style. This project is split into two main components: a Django REST API backend for handling data and business logic, and a React frontend for interactive UI/UX.

## Features

- Browse through a curated list of jokes.
- Rate jokes as like or dislike.
- Receive a personalized Jokometian character based on joke preferences.
- Share your Jokometian character with others.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Node.js and npm (for the React frontend)

### Backend Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/joke-o-meter.git
   ```
2. Navigate to the project directory:
   ```sh
   cd joke-o-meter
   ```
3. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory of the project and populate it with necessary environment variables:
   ```plaintext
   DJANGO_SECRET_KEY=your_secret_key
   DJANGO_DEBUG=True
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   OPENAI_API_KEY=(optional)
   ```
5. Run migrations to set up the database:
   ```sh
   python manage.py migrate
   ```

### Frontend Setup

>Under development

1. Navigate to the `front` directory:
   ```sh
   cd front
   ```
2. Install the required npm packages:
   ```sh
   npm install
   ```

## Running the Application in Development Mode

### Backend

1. Start the Django development server:
   ```sh
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000`.

### Frontend

1. Ensure you are in the `front` directory:
   ```sh
   cd front  # If not already in the front directory
   ```
2. Start the React development server:
   ```sh
   npm start
   ```
   The frontend will be available at `http://localhost:3000`.

## API Documentation

Refer to `http://localhost:8000/swagge/` for detailed API documentation.