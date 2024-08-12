

# Install Dependencies from `requirements.txt
```sh
pip install -r requirements.txt
```

# To run tests

```sh
python -m pytest tests/
```


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
curl -X GET http://localhost:5000/api/artifact/download/1/1.0.0 \
     -o hello.zip
```