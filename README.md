# simple-task-list-API

# My FastAPI App

This is a simple FastAPI application with SQLAlchemy and SQLite.

## Installation

Install the dependencies:

```bash
pip install -r requirements.txt
```

## RUN 

In order to run the simple fastapi server simply run the command : uvicorn main:app --reload

In the output, there's a line with something like:

``` INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)```
That line shows the URL where your app is being served, in your local machine.

## Check it

Open your browser at http://127.0.0.1:8000.

You will see the JSON response as:

```{"message": "Hello World"}```

# Interactive API docs

Now go to http://127.0.0.1:8000/docs.

You will see the automatic interactive API documentation (provided by Swagger UI)

# Alternative API docs

And now, go to http://127.0.0.1:8000/redoc.

You will see the alternative automatic documentation (provided by ReDoc)