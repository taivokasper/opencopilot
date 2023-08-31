# OpenCopilot quickstart deployment

## Fly.io initial setup
1. Signup at [fly.io](https://fly.io)
2. Install flyctl locally (Macos):
```bash
brew install flyctl
```
3. Authenticate local cli by running:
```bash
flyctl auth login
```

## App deployment

[fly.io](https://fly.io) supports both Dockerized and bare deployment types. These instructions are for Dockerizes app only.

1. make sure your OpenCopilot is running or capable of running on 0.0.0.0 network interface. This can be achieved by:
```python
copilot = OpenCopilot(
    ...
    host=os.getenv("HOST", "127.0.0.1")
    ...
)
```

2. In your OpenCopilot root add the following `Dockerfile`:
```docker
FROM python:latest

WORKDIR /app
ADD requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 3000

CMD ["python", "copilot.py"]
```

3. Use `flyctl` to generate a fly.io deployment (`fly.toml` file)
```bash
flyctl launch
```
* flyctl prompts you for an app name
* answer _No_ to all the rest. We do not need a database and cannot deploy yet!

4. Set OPENAI_API_KEY secret
```bash
fly secrets set OPENAI_API_KEY=$YOUR_OPENAI_API_KEY_HERE
```

5. Open `fly.toml` file and add a top level section for environment variables somewhere to the file:
```toml
[env]
  HOST = "0.0.0.0"
```

6. Now you are ready to deploy the app by running:
```bash
flyctl deploy
```
Your app should now be ready!
