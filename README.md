
# Joke-O-Meter

## Description

The Joke-O-Meter is a web application designed to entertain users by presenting them with a collection of jokes. Users can rate jokes based on their preferences, swiping right for jokes they like and left for those they do not. After evaluating a set of jokes, the application analyzes the user's preferences and assigns them a unique Jokometian character, each with its own set of traits reflecting the user's humor style. This project is split into two main components: a Django REST API backend for handling data and business logic, and a React frontend for interactive UI/UX.

## Features

- Browse through a curated list of jokes.
- Rate jokes as like or dislike.
- Receive a personalized Jokometian character based on joke preferences.
- Share your Jokometian character with others.
- Jokometians ranking

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
6. Run and compile translations
   ```sh   
   django-admin compilemessages
   ```

### Frontend Setup

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

## Localization

The application currently supports English and Spanish. To add additional languages, follow the steps below. This example demonstrates adding French.

### Back-End

1. **Generate Message Files**: Run the following command to generate the `.po` file for the new language (French, in this example):

   ```sh
   django-admin makemessages -l fr
   ```

2. **Translate Messages**: Open the generated file located at `/locale/fr/LC_MESSAGES/django.po`. Translate the message strings from English to French, filling in the corresponding 'msgstr' for each 'msgid'.

3. **Compile Messages**: After translating, compile the messages to apply the translations using:

   ```sh
   django-admin compilemessages
   ```

### Front-End

For front-end localization:

1. **Add Language File**: Create a new language file for your translations,  `translation.json`, in the translations folder (e.g., `/locales/fr/translation.json`).

2. **Translate Content**: Fill `fr.json` with the translations. Use the existing English (or Spanish) translations as a reference. The file structure typically follows a key-value format, where keys match those used in your React components:

   ```json
   {
     "welcome": "Bienvenue",
     "description": "Ceci est une application localisée"
   }
   ```

3. **Configure i18n**: Ensure your i18n configuration includes the new language. This typically involves adding the new language to the list of available languages and possibly setting a detection order if you're using language detection:

   ```javascript
   i18n.use(initReactI18next).init({
     resources,
     lng: "en", // Default language
     fallbackLng: "en",
     whitelist: ["en", "es", "fr"], // Available languages
     interpolation: {
       escapeValue: false
     }
   });
   ```

Certainly, adding a **TODO** section to your README.md can help track future enhancements and important tasks that need attention. Here's how you could structure this section to highlight the areas for improvement mentioned:

## TODO

### UI Improvements

- **Responsive Design**: Ensure the application is fully responsive and provides an optimal viewing experience across a range of devices, including tablets and smartphones.
- **User Interface Polish**: Review and refine the UI elements for better visual appeal and usability. This includes button styles, form inputs, and navigation components.

### Front-End Testing

- **Component Tests**: Expand the suite of React component tests to cover all user interactions and edge cases.
- **Integration Tests**: Develop front-end integration tests that simulate real user scenarios and interactions within the application. This will help ensure that the front-end components work seamlessly together.

### Accessibility

- **Keyboard Navigation**: Improve keyboard navigation within the application to ensure that all interactive elements are accessible without the use of a mouse.

Contributions to address these tasks are highly valued.