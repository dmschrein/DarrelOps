
# Clone the repository

```sh
git clone https://github.com/dmschrein/DarrelOps.git

cd DarrelOps

```

# Create virtual environment
```sh
python3 -m venv .venv
```

# Activate virtual environment on macOS/Linux
```sh
source .venv/bin/activate
```

# Activate virtual environment on Windows
```sh
.\myenv\Scripts\activate

```

# Install Dependencies from requirements.txt and Setup Program

```sh

pip install -r requirements.txt

pip install -e .

```

# Running the server

```sh
cd darrelops

python3 -m darrelops runserver

```

# Run artifactory and database cleanup 

```sh

python3 reset_program.py

```


# To run tests

```sh
python -m pytest tests/
```


# ROUTES
POST `/api/register`: Register a new C program with the build server.<br>
GET `/api/artifacts`: List all artifacts.<br>
GET `/api/artifacts/<program_id>`: List all artifacts for a specific program.<br>
GET `/api/artifact/download/<program_id>/<version>`: Download a specific artifact.<br>
GET `/status`: Displays status of builds for each registered C program.

# API USAGE

# Register a C Program

```sh
curl -X POST http://localhost:5000/api/register \
     -H "Content-Type: application/json" \
     -d '{
           "name": "hello",
           "repo_url": "https://github.com/dmschrein/hello.git",
           "repo_branch": "main",
           "build_cmd": "make",
           "build_dir": "./"
          }'
```

```sh
curl -X POST http://localhost:5000/api/register \
     -H "Content-Type: application/json" \
     -d '{
           "name": "hello",
           "repo_url": "https://github.com/dmschrein/hello.git",
           "repo_branch": "development",
           "build_cmd": "make",
           "build_dir": "./"
          }'
```


```sh
curl -X POST http://localhost:5000/api/register \
     -H "Content-Type: application/json" \
     -d '{
           "name": "hello",
           "repo_url": "https://github.com/dmschrein/hello-2.git",
           "repo_branch": "main",
           "build_cmd": "make",
           "build_dir": "./"
          }'
```

```sh

curl -X POST http://localhost:5000/api/register \
     -H "Content-Type: multipart/form-data" \
     -F "files=@hello-2-main.zip" \
     -F "name=hello-2-main" \
     -F "repo_url=https://github.com/dmschrein/hello-2.git" \
     -F "repo_branch=main" \
     -F "build_cmd=make" \
     -F "build_dir=./"
     
```

# List All Artifacts
```sh

curl -X GET http://localhost:5000/api/artifacts

```

# Retrieve Artifacts for a specific program
```sh

curl -X GET http://localhost:5000/api/artifacts/1

```

# Download an Artifact
```sh
curl -O -J http://localhost:5000/api/artifact/download/1/1.0.0

```


# Program clean up (run in root directory)
```sh
python3 reset_program
```

