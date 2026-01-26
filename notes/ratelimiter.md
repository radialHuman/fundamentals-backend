## I. Core Understanding & Purpose

### 1.  What is it? (A concise definition of the component)
- What problem does it solve? What is its core function?

### 2.  Why is it used? (The value it provides in a backend system)
- What are the key benefits and drawbacks of using it?

### 3.  What was there before it? (Historical context, predecessor technologies)
- Why was the previous solution inadequate? What drove the need for this component?


## II. Evolution & Future

### 4.  Advancements? (Significant milestones, key features added over time)
- How has it evolved to meet changing needs?

### 5.  Future Trends & Emerging Technologies: (How does it fit into the future?)
- What emerging technologies (AI, serverless, etc.) will impact it?  How is it adapting?


## III. Practical Application 

### 6.  When to Use It: (Ideal scenarios, use cases)
- What are the specific requirements that make it a good choice?

### 7.  When *Not* to Use It: (Situations where it's unsuitable)
- What are the limitations or drawbacks that would make an alternative better?

### 8.  Common Use Cases: (Real-world examples, industry applications)
- Can you provide specific examples of how it's being used successfully?

### 9.  Typical Configuration Options: (Common settings, customization)
- What are the most frequently used configurations? What are the trade-offs of different  configurations?
- Which one to choose?
    - depends on system scale, traffic pattern and need for precision

### 10. How to Use It? (Basic usage, getting started)
- What are the essential steps to implement and use it effectively?

### 11. How does it integrate with other components? (System interactions)
- What are the common integration patterns? What APIs or protocols are used?

### 12. Common Pitfalls or Mistakes: (Things to avoid during implementation)
- What are the most frequent errors or misconfigurations?


## IV. Technical Deep Dive 

### 13. Internal Working: (Architecture, algorithms, data structures)

#### Leaky bucket algorithm
- the requests handelling is in fixed rate
    - if large amount of req comes in it still processess it at the same rate
- If the capacity is exceeded, it rejects the last excesses, FIFO
- Pros : stable traffic control, simple and easy to implement
- Cons : not flexible, cant handle traffic spikes
- Use case : where stable req handelling is required
    - n/w bandwidth mgmt : to limit data transfer rate
    - video streaming : smooth transmission
    - server req handeling : steady rate, no overload

#### Token bucket algorithm
- better than leaky while handelling bursts of traffic
- a bucket is filled with tokens are a steady per sec rate
- the bucket has a fixed capacity
- if there is token in the bucket the request is processed
    - else discarded
- Pros : better than leaky, easy to understand and implement, 
- Cons : memory usage is high, need to maintain buckets for each user, not smooth req rate, tuning parameters of bucket capacity and token generation rate as epr system needs, trail and error
- Use case :
    - public api rate limiting : control individual user req, pereventing overload, can handel peaks while being stable
    - used in stripe and ec2

#### Fixed window counters
- its time based
- each time slot is given max capacity and a counter
- as loong as the counter is >= max capacity it processes request
- once its not, then rejects teh request and
- when the time slot ends, it resets the counter for that time slot
- Pros : simple and easy to implement
    - allows short term busrts
- Cons :
    - Though it controls in time slot but in an overlapping time slot it can go beyond the limit, example  :
        - @1.9 sec : 4, @2.2 sec : 4
        - if the max cap is 5 then both the time slots are within limits
            - but if the time slot is looked at from 1.5-2.5 instea dof 1-2 and 2-3
                - it processes 8 in 1 sec which is beyond 5 that was the limit
- Different from token bucket:
    - reset in the next time slot is to 0
        - while in token bukcet unsused can be sued in the next time slot
    - state mgmt is simpler in fixed window

- Use case : simple requirement with a little bit of unstability
    - api rate limiting, time period based
    - preventing logining attempts

#### Sliding window log
- addresses boundary spikes of fixed window
- Dynamic window, that shfts as time moved
- timestamp of each req is logged
- new req, is checked against logs of the latest window and if is mroe then rejects else logged and processed
- more smoother traffic control
- the time window is from the time of new req till the predecided time limit and if anything is more than hte capacity allocated, it rejectes
- Pros :
    - fine grained traffic control
    - no window boundary issue
- Cons : complex, log update, read adds on resources
- USe case : 

#### Sliding window counters
- balance between fixed window and sliding windo log
- no logs here
- uses weighted of previous window
- formula : #doubt
- Pros : simple cal, no storing logs
- Cons : not as precise as sliding window log, and can still have boundary issues
- Use case : 

#### Best practice
- include rate limiting info in http response headers, so that users can plan accordingly

### 14. Performance Characteristics: (Speed, latency, resource usage)
- How does it perform under different load conditions?

### 15. Scalability Limitations: (Horizontal vs. vertical scaling)
- What are the bottlenecks that limit scalability?

### 16. Security Considerations: (Vulnerabilities, best practices)
- What are the potential security risks? What security measures should be implemented?

### 17. Failure Modes: (Common errors, recovery strategies)
- What are the likely failure scenarios? How can they be prevented or mitigated?


## V. Ecosystem & Support

### 18. Famous Ones: (Popular implementations, key players)
- What are the leading products or services based on this component?

### 19. Licensing or Cost Considerations: (Pricing models, TCO)
- What are the long-term cost implications?

### 20. Licensing Models or Open-Source Options: (Availability and implications)
- What are the pros and cons of each licensing option?

### 21. Community or Ecosystem Support: (Activity, resources)
- How responsive is the community? Are there active forums or mailing lists?

### 22. Learning Resources or Documentation: (Quality, accessibility)
- Is the documentation comprehensive and up-to-date?

### 23. Versioning and Upgrade Paths: (Compatibility, migration)
- What are the potential challenges during upgrades?


## VI. Operational Aspects 

### 24. Deployment Patterns: (Common architectures, environments)
- What are the recommended deployment practices?

### 25. Maintenance Requirements: (Ongoing tasks, updates)
- What are the typical maintenance procedures?

### 26. Monitoring and Observability Needs: (Metrics, logging, alerting)
- What key metrics should be monitored?

### 27. Testing Strategies: (Types of tests, automation)
- What are the best practices for testing this component?


## VII. Broader Context 

### 28. Industry Standards or Best Practices: (Adoption rates, guidelines)
- What are the prevailing standards or guidelines?

### 29. Trade-offs Compared to Other Solutions: (Strengths, weaknesses)
- What are the key differentiators?

### 30. Alternatives: (Competing technologies)
- What are the relative strengths and weaknesses of the alternatives?

### 31. Real-world examples or case studies: (Demonstrating effectiveness)
- Can you provide detailed examples of successful implementations?

### 32. What best-practice patterns exist for its implementation? (Proven approaches)
- What are the most common and effective patterns?

### 33. Are there regulatory or compliance considerations? (Legal, ethical)
- Does this component have any implications for data privacy or security?


## VIII. Commercial Support & Services

### 34. Vendors Offering Commercial Support or Services: (Available options)
- What are the different support tiers and pricing models?


## IX. Resources

### Links

### Books

### YT
- [link](https://youtu.be/mQCJJqUfn9Y)