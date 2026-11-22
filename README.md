# EventHub

EventHub is a college event management system designed to help students discover college events and access information about upcoming activities.

The project is being developed using Python and Flask, with SQLite for database management and HTML/CSS for the frontend.

## Technology Stack

- Python
- Flask
- SQLite
- HTML and CSS
- Git and GitHub
- Pytest
- GitHub Actions

## Implemented Features

- Display college events on the homepage.
- Retrieve event information from an SQLite database.
- Display event details such as name, description, date, venue, organizer and category.
- Automated homepage testing using Pytest.
- Continuous Integration workflow using GitHub Actions.

## Planned Features

- Browse events by category.
- Search for events.
- Manage event information.
- Improve event details and user experience.

## Project Structure

```text
EventHub/
├── .github/
│   └── workflows/
│       └── tests.yml
├── tests/
│   └── test_app.py
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── app.py
├── database.py
├── eventhub.db
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup and Installation

1. Clone the repository:

   `git clone https://github.com/hemangsrivastava/EventHub.git`

2. Navigate to the project directory:

   `cd EventHub`

3. Create a virtual environment:

   `python -m venv .venv`

4. Activate the virtual environment on Windows:

   `.venv\Scripts\activate`

5. Install dependencies:

   `pip install -r requirements.txt`

6. Initialize the database:

   `python database.py`

7. Run the application:

   `python app.py`

8. Open the application at:

   `http://127.0.0.1:5000`

## Testing

Run the automated tests using:

`python -m pytest -v`

The project uses GitHub Actions to automatically execute tests when changes are pushed to the main or develop branches, or when pull requests target these branches.

## Project Status

EventHub is currently under development. New features are being added and tested incrementally.

## Team

- **Hemang Srivastava:** Project Development, Source Code Management (SCM), GitHub Management and Integration.
- **Dhruv Singh Solanki:** Testing, Test Case Development and Bug Identification.

Both team members contribute to maintaining the project workflow and quality.
