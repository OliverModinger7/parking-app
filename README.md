# Flask App for Consulting and Registering Data

This project is a Flask web application that allows users to consult data about a specific number and register new data through an API. The application is connected to a MongoDB database for data storage and retrieval.

## Project Structure

```
flask-app
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   └── js
│   │       └── scripts.js
│   └── templates
│       └── index.html
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/flask-app.git
   cd flask-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Update the `config.py` file with your MongoDB connection details and any other necessary environment variables.

## Running the Application

To start the Flask application, run:
```
python run.py
```

The application will be accessible at `http://127.0.0.1:5000`.

## Usage

- Navigate to the main page to consult data about the specified number.
- Use the provided API endpoints to register new data.

## License

This project is licensed under the MIT License. See the LICENSE file for details.