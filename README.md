# Flask and MongoDB Student Grades

This project contains a Flask frontend and a Flask backend API. The frontend
runs on port `8000`; the backend runs on port `9000`.

## Requirements

- Python 3.10 or newer
- pip
- MongoDB, for saving and viewing submitted grades

## Install dependencies

From the project directory, create and activate a virtual environment, then
install the packages listed in `requirements.txt`:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows Command Prompt, activate the environment with:

```bat
venv\Scripts\activate
```

## Configure MongoDB

The backend reads the MongoDB connection string from `backend/.env`. Create
that file with:

```dotenv
URI=your_mongodb_connection_string
```

Use a connection string for a MongoDB instance accessible to your machine.
Do not commit real credentials to source control. MongoDB is used by the
submission and database-view routes; `/api` returns the project's grade data.

## Start the applications

Run each application in a separate terminal from the project directory. If
using a virtual environment, activate it in both terminals.

Start the backend:

```bash
python backend/app.py
```

Start the frontend:

```bash
python frontend/app.py
```

Open the frontend at <http://localhost:8000/>. The backend API is available at
<http://localhost:9000/>.

## Backend API

### `GET /api`

Returns student grades as a JSON object whose keys are student names and whose
values are grades. The response combines the entries in
`backend/student_grade.json` with the additional entries defined in the
backend's `/api` route. If a name is present in both places, the route's
in-code grade takes precedence.

Example response:

```json
{
  "Anjali": 90,
  "Ravi": 80,
  "Ramesh": 70,
  "Suresh": 60,
  "Yoesh": 90,
  "Sameer": 80,
  "Ram": 70,
  "Kuldeep": 60
}
```

You can retrieve it in a browser or with:

```bash
curl http://localhost:9000/api
```

The frontend form at `http://localhost:8000/` submits student details through
the backend's `POST /submit` route. `GET /view` returns the grades stored in
MongoDB. Submitting an email already present in MongoDB returns HTTP `409`;
the frontend shows an error on the form and retains the submitted values.