# Aim
- Load Balancing: Nginx distributes traffic between servers
- Reverse Proxy: Nginx acts as a single entry point
- Basic Server Management: Starting/stopping services
- Configuration: Editing Nginx config files

## Step 1: Create Two Simple Web Servers

### Create two simple HTTP servers
echo 'Hello from Server 1' > server1.html
echo 'Hello from Server 2' > server2.html

### Start servers in background
python3 -m http.server 8000 --directory . &
python3 -m http.server 8001 --directory . &

## Step 2 configure nginx load balancer
sudo code /etc/nginx/sites-available/default

upstream backend_servers {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
}

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

## Step 3 test
### Restart Nginx
sudo systemctl restart nginx

### Test with curl
curl http://localhost

## Step 4 check
### Check Nginx logs
sudo tail -f /var/log/nginx/access.log

### Test from browser
# Open http://localhost in your web browser