# Aim
- Docker Compose: Define multi-container applications
- Network Isolation: Containers communicate only within the network
- Environment Variables: Pass configuration to containers
- Service Discovery: Containers can find each other by name

1. docker network create backend-network

2. Python app
```python
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return f"Hello from {os.getenv('SERVER_ID', 'unknown')}"

if __name__ == '__main__':
    app.run(host='localhost', port=80)
```

3. Docker file
```docker
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python", "app.py"]
```

4. requirements.txt
flask

5. Build docker
- docker build -t web-app .

- Run two instances with different environment variables
    - docker run -d --name server3 --network backend-network -e SERVER_ID=1 -p 8000:80 web-app
    - docker run -d --name server4 --network backend-network -e SERVER_ID=2 -p 8001:80 web-app

6. compose
```docker
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - server1
      - server2
    networks:
      - backend-network

  server1:
    image: web-app
    environment:
      - SERVER_ID=1
    networks:
      - backend-network

  server2:
    image: web-app
    environment:
      - SERVER_ID=2
    networks:
      - backend-network

networks:
  backend-network:
    driver: bridge
```

6. nginx config
```confg
events {
    worker_connections 1024;
}

http {
    upstream backend_servers {
        server server1:80;
        server server2:80;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://backend_servers;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

7. run
docker-compose up -d

8. test
curl http://localhost

9. restart
docker-compose down
docker-compose rm -f
docker rm $(docker ps -q) -f