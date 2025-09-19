# Study Tracker

A Django web application to track and analyze your study sessions, providing insights to improve your productivity.

## Features

- **User Authentication**: Secure signup, login, and logout functionality
- **Study Session Management**: Add, edit, view, and delete study sessions
- **Dashboard Analytics**: Visual representation of your study data with charts
- **Data Insights**: Personalized insights based on your study patterns
- **Export Functionality**: Download your study data as CSV
- **Productivity Prediction**: Basic prediction of productivity based on past data

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd studytracker
```

2. Create and activate a virtual environment:
```
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run migrations:
```
python manage.py migrate
```

5. Create a superuser (optional):
```
python manage.py createsuperuser
```

6. Run the development server:
```
python manage.py runserver
```

7. Access the application at http://127.0.0.1:8000/

## Usage

1. Sign up for a new account or log in with existing credentials
2. Add study sessions from the dashboard or session list page
3. View your study statistics and insights on the dashboard
4. Export your data or make productivity predictions using the tools section

## Technologies Used

- Django
- Bootstrap 5
- Chart.js
- Plotly
- Pandas
- SQLite (default database)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Django documentation
- Bootstrap documentation
- Chart.js documentation
- Plotly documentation