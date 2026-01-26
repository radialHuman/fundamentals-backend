## I. Core Understanding & Purpose

### 1.  What is it? 
- What problem does it solve? What is its core function?
    - to balace incoming request to multiple machines/services/processes
    - it is a reverse proxy : client sends request to a server but internally the server calls other server
    - the client doesn know where tis request is forwarded tohence reverse proxy
        - where unlike normal proxy, the server doesn know who the client is
    - its a s/w that dedices where to frwd requests based on criterias
        - if a backend server is down, it will stop sending to that one 

### 2.  Why is it used? 
- What are the key benefits and drawbacks of using it?
    - For fault tolerance
    - Instead of sending to one server the request is distributed to replicas of servers
        - in a manner that doesn hurt the performance or congest requests

### 3.  What was there before it? 
- Why was the previous solution inadequate? What drove the need for this component?


## II. Evolution & Future

### 4.  Advancements? 
- How has it evolved to meet changing needs?

### 5.  Future Trends & Emerging Technologies: 
- What emerging technologies will impact it?  How is it adapting?


## III. Practical Application 

### 6.  When to Use It
- What are the specific requirements that make it a good choice?

### 7.  When *Not* to Use It
- What are the limitations or drawbacks that would make an alternative better?

### 8.  Common Use Cases
- Can you provide specific examples of how it's being used successfully?

### 9.  Typical Configuration Options
- What are the most frequently used configurations? What are the trade-offs of different configurations?

### 10. How to Use It? 
- What are the essential steps to implement and use it effectively?

### 11. How does it integrate with other components? 
- What are the common integration patterns? What APIs or protocols are used?

### 12. Common Pitfalls or Mistakes
- What are the most frequent errors or misconfigurations?


## IV. Technical Deep Dive 

### 13. Internal Working
#### Underlying mechanisms:
- Round robin : 1/1, irrespective of the laod backend replicas are facing, each gets equal turn
- Weighted round robin : some servers get priority based on their capacity 
- Least connections : the one with least requests gets the next request
- Weighted least connections : some preference is given absed on the server capacity
- Random : just randomly send request without caring about the capacity or queue

#### Types
- Layer 4 (transport) : here we know only the ip and the port
    - so based pn that the traffic is routed
    - the data is not known at this stage
    - checks the ip of incoming client, and ip of itself, if matches
        - decides where to send the incoming request based on algorithms mentioned above
        - changes the target ip address to the decided server and routes the request
            - using network address translation #doubt
                - a table where it logs what cmae in and what was it changed to
    - The client doesn know where the request is going.
        - as it could be a different subnet etc, and its only poc is the load balancer ip
    - Pros
        - Simple implementation (only ip) : 
        - efficient : doesn look at the data inside the packets, no decryption involved so faster
        - more secure : if compromised, data is not leaked
        - one TCP connection : the routing acts as just one connection, like a router, only one circuit not breaker
        - uses NAT : staefulness
    - Cons
        - not smart enough : cant see data, cant look at cookies, cant modify or rewrite urls
        - not for microservices : based on the content, it cant reroute, cant see
        - sticky per segment : incoming packet if broken into multiple and gets rerouted to different servers it will not be helpful
            - there is no way that can be done in this
        - no caching : cant see data so cant caching, doesn know what to and what not to
- Layer 7 (application) : can see the data and make a smart routing
    - if allowed it can look at the data and decrypt it to decide how to route based on routing mechanism "/"
        - using tls and certification
    - it looks at the ip address for the target and reads where the api whats to get info from
        - then establishes connection between the client and itself
        - takes the data changes the ip address in tcp packet from it self to the other backend server
            - making it act as two different connections even while routing
            - in this process ehaders or the content might change based on the nature of the backend servers requirement
    - pros
        - smart loadbalancing
        - microservices compatible
        - routing based on data
        - caching : because data is visible
    - Cons
        - expensive : time as it looks at the data
        - decrypts data, terminates as tls : certificates are visible
        - two tcp connections : more persistence, time out issues
        - must share tls certificate #doubt
        - less secure, data visible
    #TODO implement it

### 14. Performance Characteristics
- How does it perform under different load conditions?

### 15. Scalability Limitations
- What are the bottlenecks that limit scalability?

### 16. Security Considerations
- What are the potential security risks? What security measures should be implemented?

### 17. Failure Modes
- What are the likely failure scenarios? How can they be prevented or mitigated?


## V. Ecosystem & Support

### 18. Famous Ones
- What are the leading products or services based on this component?
    - Paid
        - AWS NLB, AWS ALB
        - GC LB
        - Azure application gateway
        - Citrix ADC
        - Cloudflare Load Balancer is a global edge solution used by over 7.5 million domains, offering multi-region failover and performance optimization
    - F5 BIG-IP
    - Open
        - HAProxy excels in performance-critical systems. (example : haproxyl4)
        - NGINX is ideal for simple HTTP apps and reverse proxying. 
        - Traefik is a favorite in Kubernetes and Docker environments for dynamic service discovery. 
        - Envoy powers service meshes and gRPC-based microservices with strong observability. 
        - Seesaw
        - Neutrino

### 19. Licensing or Cost Considerations
- What are the long-term cost implications?

### 20. Licensing Models or Open-Source Options
- What are the pros and cons of each licensing option?

### 21. Community or Ecosystem Support
- How responsive is the community? Are there active forums or mailing lists?

### 22. Learning Resources or Documentation
- Is the documentation comprehensive and up-to-date?

### 23. Versioning and Upgrade Paths
- What are the potential challenges during upgrades?


## VI. Operational Aspects 

### 24. Deployment Patterns
- What are the recommended deployment practices?

### 25. Maintenance Requirements
- What are the typical maintenance procedures?

### 26. Monitoring and Observability Needs
- What key metrics should be monitored?

### 27. Testing Strategies
- What are the best practices for testing this component?


## VII. Broader Context 

### 28. Industry Standards or Best Practices
- What are the prevailing standards or guidelines?

### 29. Trade-offs Compared to Other Solutions
- What are the key differentiators?

### 30. Alternatives
- What are the relative strengths and weaknesses of the alternatives?

### 31. Real-world examples or case studies
- Can you provide detailed examples of successful implementations?

### 32. What best-practice patterns exist for its implementation? 
- What are the most common and effective patterns?

### 33. Are there regulatory or compliance considerations? 
- Does this component have any implications for data privacy or security?


## VIII. Commercial Support & Services

### 34. Vendors Offering Commercial Support or Services
- What are the different support tiers and pricing models?


## IX. Resources

### Links

### Books

### YT
1. [Load Balancing by Hussein Nasser](https://www.youtube.com/playlist?list=PLQnljOFTspQWdgYcGXCTkjda8vd2jWJYt)