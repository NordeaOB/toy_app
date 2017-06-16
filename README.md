# Toy Application Using the OBI API

## Running the App

### Using Docker

`docker build . -t toy_app`

`docker run -d -p 5000:5000 --name toy_app toy_app`

### Without docker

`pip install -f requirements.txt`

`python toy_app.py`

