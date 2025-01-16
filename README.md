# Marriage Matchmaking App Backend

A FastAPI-based backend for a marriage matchmaking application with user management and matching functionality.

## Features
- User registration and management (CRUD operations)
- Email validation
- Interest-based matching
- Location-based matching
- Opposite gender matching

## Prerequisites
- Python 3.8+
- pip (Python package installer)
- virtualenv (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd marriage-matchmaking-app-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### User Management
- `POST /users/`: Create a new user
- `GET /users/`: List all users
- `GET /users/{user_id}`: Get a specific user
- `PUT /users/{user_id}`: Update a user
- `DELETE /users/{user_id}`: Delete a user
- `GET /users/{user_id}/matches`: Get matches for a user

### Example User Creation
```bash
curl -X POST "http://localhost:8000/users/" \
-H "Content-Type: application/json" \
-d '{
    "name": "John Smith",
    "age": 28,
    "gender": "male",
    "email": "john@example.com",
    "city": "New York",
    "interests": ["sports", "music", "travel"]
}'
```

## Data Validation

### User Fields
- `name`: 1-50 characters
- `age`: 18-100 years
- `gender`: "male" or "female"
- `email`: Valid email format (checked with email-validator)
- `city`: 1-50 characters
- `interests`: List of strings

## Testing

Sample test data is available in `dummy_data.txt`. You can use these curl commands to populate the database with test users.

## Database

The application uses SQLite as its database. The database file (`test.db`) is automatically created when the server starts. Note that the database is reset on each server restart for testing purposes.

## Development

### Project Structure
```
dating-app-backend/
├── main.py           # FastAPI application and endpoints
├── models.py         # SQLAlchemy models
├── schemas.py        # Pydantic models for validation
├── database.py       # Database configuration
├── requirements.txt  # Project dependencies
└── dummy_data.txt   # Sample test data
```

### Adding New Features
1. Update models in `models.py`
2. Add corresponding schemas in `schemas.py`
3. Implement endpoints in `main.py`
4. Update documentation

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[Add your license here]