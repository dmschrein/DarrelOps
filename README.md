
# Clone the repository

```sh
git clone https://github.com/dmschrein/DarrelOps.git

cd DarrelOps

```

# Install Dependencies from `requirements.txt

```sh

pip install -r requirements.txt

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

# API USAGE

# Register a C Program

```sh
curl -X POST http://localhost:5000/api/register \
     -H "Content-Type: application/json" \
     -d '{
           "name": "hello",
           "repo_url": "https://github.com/dmschrein/hello.git",
           "build_cmd": "make",
           "build_dir": "./"
          }'
```

```sh
curl -X POST http://localhost:5000/api/register \
     -H "Content-Type: application/json" \
     -d '{
           "name": "hello2",
           "repo_url": "https://github.com/dmschrein/hello-2.git",
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

# Routes
POST `/api/register`: Register a new C program with the build server.
GET `/api/artifacts`: List all artifacts.
GET `/api/artifacts/<program_id>`: List all artifacts for a specific program.
GET `/api/artifact/download/<program_id>/<version>`: Download a specific artifact.
