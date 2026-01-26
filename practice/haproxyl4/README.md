1. create 2 severs using python on different port
2. use haproxy to alternate incoming request between both
    - install it first
3. configure it #doubt how to make this
```tcp.cfg
global
    maxconn 4096 
defaults
    log global
    mode tcp 
    timeout connect 5000 
    timeout client 50000  # useful in l7
    timeout server 50000  # useful in l7
frontend localnodes
    bind *:8888
    default_backend nodes
backend nodes
    server serverl 127.0.0.1:4000 check
    server server2 127.0.0.1:3000 check
```
4. run hapraxy
haproxy -f tcp.cfg

5. check port 8888
http://localhost:8888
- meaning 8888 is the proxy load balancer and it will send incoming to either 4000 or 3000 

6. killing a server shows alert in haproxy and so does bringing them back