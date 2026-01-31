# Comprehensive AWS Learning Plan for Linux (No AWS Account Required)

## Phase 1: Local Development Environment Setup (Week 1)

### Core Installation (Linux)

#### 1. **Docker & Docker Compose** (Essential Foundation)
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group (avoid sudo)
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

#### 2. **LocalStack** (Complete AWS Emulator)
```bash
# Install Python and pip (if not already installed)
sudo apt install python3 python3-pip -y

# Install LocalStack
pip3 install localstack

# Install LocalStack CLI wrapper
pip3 install awscli-local

# Verify
localstack --version
```

#### 3. **AWS CLI v2**
```bash
# Download and install
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify
aws --version

# Configure for LocalStack (dummy credentials)
aws configure
# AWS Access Key ID: test
# AWS Secret Access Key: test
# Default region: us-east-1
# Default output format: json
```

#### 4. **Terraform**
```bash
# Add HashiCorp GPG key
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

# Add repository
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

# Install
sudo apt update && sudo apt install terraform -y

# Verify
terraform --version
```

#### 5. **AWS SAM CLI**
```bash
# Download installer
wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
sudo ./sam-installation/install

# Verify
sam --version
```

#### 6. **Additional Development Tools**
```bash
# Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Python development tools
sudo apt install python3-dev python3-venv -y

# Git
sudo apt install git -y

# jq (JSON processor for CLI)
sudo apt install jq -y

# httpie (better curl)
sudo apt install httpie -y

# Verify all
node --version
npm --version
python3 --version
git --version
jq --version
http --version
```

#### 7. **VS Code with Extensions**
```bash
# Download and install VS Code
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code -y

# Install extensions via CLI
code --install-extension amazonwebservices.aws-toolkit-vscode
code --install-extension hashicorp.terraform
code --install-extension ms-python.python
code --install-extension ms-azuretools.vscode-docker
```

---

## Phase 2: LocalStack Complete Setup (Week 1-2)

### LocalStack Docker Compose Configuration

Create project directory:
```bash
mkdir -p ~/aws-learning-lab
cd ~/aws-learning-lab
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  localstack:
    container_name: localstack-main
    image: localstack/localstack:latest
    ports:
      - "4566:4566"            # LocalStack Gateway
      - "4510-4559:4510-4559"  # External services port range
    environment:
      # Core services
      - SERVICES=s3,dynamodb,lambda,apigateway,ec2,ecs,rds,sqs,sns,cloudformation,cloudwatch,logs,iam,sts,secretsmanager,ssm,kms,elasticache,route53,cloudfront,events,stepfunctions
      - DEBUG=1
      - DATA_DIR=/tmp/localstack/data
      - DOCKER_HOST=unix:///var/run/docker.sock
      - HOST_TMP_FOLDER=${TMPDIR:-/tmp}/localstack
      - PERSISTENCE=1
      # Lambda configuration
      - LAMBDA_EXECUTOR=docker-reuse
      - LAMBDA_REMOTE_DOCKER=0
      # Network configuration
      - HOSTNAME_EXTERNAL=localhost
      - EDGE_PORT=4566
    volumes:
      - "${TMPDIR:-/tmp}/localstack:/tmp/localstack"
      - "/var/run/docker.sock:/var/run/docker.sock"
      - "./init-scripts:/docker-entrypoint-initaws.d"
    networks:
      - aws-local

  # PostgreSQL (RDS alternative)
  postgres:
    container_name: postgres-local
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=appdb
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - aws-local

  # Redis (ElastiCache alternative)
  redis:
    container_name: redis-local
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - aws-local

  # MySQL (RDS alternative)
  mysql:
    container_name: mysql-local
    image: mysql:8
    ports:
      - "3306:3306"
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=appdb
      - MYSQL_USER=admin
      - MYSQL_PASSWORD=password
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - aws-local

  # DynamoDB Admin UI
  dynamodb-admin:
    container_name: dynamodb-admin
    image: aaronshaf/dynamodb-admin:latest
    ports:
      - "8001:8001"
    environment:
      - DYNAMO_ENDPOINT=http://localstack:4566
      - AWS_REGION=us-east-1
      - AWS_ACCESS_KEY_ID=test
      - AWS_SECRET_ACCESS_KEY=test
    depends_on:
      - localstack
    networks:
      - aws-local

volumes:
  postgres-data:
  redis-data:
  mysql-data:

networks:
  aws-local:
    driver: bridge
```

### Helper Scripts

Create `scripts/start.sh`:
```bash
#!/bin/bash
echo "🚀 Starting AWS Local Environment..."
docker-compose up -d
echo "⏳ Waiting for LocalStack to be ready..."
sleep 10
echo "✅ Environment ready!"
echo "📊 LocalStack: http://localhost:4566"
echo "📊 DynamoDB Admin: http://localhost:8001"
echo "🐘 PostgreSQL: localhost:5432"
echo "🔴 Redis: localhost:6379"
echo "🐬 MySQL: localhost:3306"
```

Create `scripts/stop.sh`:
```bash
#!/bin/bash
echo "🛑 Stopping AWS Local Environment..."
docker-compose down
echo "✅ Environment stopped!"
```

Create `scripts/reset.sh`:
```bash
#!/bin/bash
echo "🔄 Resetting AWS Local Environment..."
docker-compose down -v
docker-compose up -d
echo "✅ Environment reset complete!"
```

Make scripts executable:
```bash
chmod +x scripts/*.sh
```

### AWS CLI Aliases for LocalStack

Add to `~/.bashrc` or `~/.zshrc`:
```bash
# LocalStack aliases
alias awslocal="aws --endpoint-url=http://localhost:4566"
alias tfl="terraform"

# Helper functions
aws-local-status() {
    curl -s http://localhost:4566/_localstack/health | jq
}

aws-local-logs() {
    docker logs -f localstack-main
}
```

Apply changes:
```bash
source ~/.bashrc
```

---

## Phase 3: Service-by-Service Learning Modules

### Module 1: S3 (Simple Storage Service) - Week 2

#### Setup & Exercises

**1. Basic S3 Operations:**
```bash
# Create bucket
awslocal s3 mb s3://my-first-bucket

# List buckets
awslocal s3 ls

# Create test file
echo "Hello AWS!" > test.txt

# Upload file
awslocal s3 cp test.txt s3://my-first-bucket/

# List objects
awslocal s3 ls s3://my-first-bucket/

# Download file
awslocal s3 cp s3://my-first-bucket/test.txt downloaded.txt

# Delete object
awslocal s3 rm s3://my-first-bucket/test.txt

# Delete bucket
awslocal s3 rb s3://my-first-bucket
```

**2. S3 with Python (boto3):**
```bash
# Install boto3
pip3 install boto3
```

Create `s3_practice.py`:
```python
import boto3
from botocore.config import Config

# Configure boto3 for LocalStack
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

# Create bucket
bucket_name = 'python-practice-bucket'
s3.create_bucket(Bucket=bucket_name)
print(f"✅ Created bucket: {bucket_name}")

# Upload file
s3.put_object(
    Bucket=bucket_name,
    Key='data/sample.txt',
    Body=b'Hello from Python!'
)
print("✅ Uploaded file")

# List objects
response = s3.list_objects_v2(Bucket=bucket_name)
for obj in response.get('Contents', []):
    print(f"📄 {obj['Key']}")

# Download file
obj = s3.get_object(Bucket=bucket_name, Key='data/sample.txt')
content = obj['Body'].read().decode('utf-8')
print(f"📥 Content: {content}")

# Enable versioning
s3.put_bucket_versioning(
    Bucket=bucket_name,
    VersioningConfiguration={'Status': 'Enabled'}
)
print("✅ Versioning enabled")
```

**3. S3 Static Website Hosting:**
```bash
# Create website bucket
awslocal s3 mb s3://my-website

# Create index.html
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>My AWS Site</title></head>
<body>
    <h1>Hello from S3!</h1>
    <p>This is hosted on LocalStack S3</p>
</body>
</html>
EOF

# Upload with public-read ACL
awslocal s3 cp index.html s3://my-website/ --acl public-read

# Configure website hosting
awslocal s3 website s3://my-website/ --index-document index.html
```

**Exercise 1:** Create a photo gallery with folders (albums) and multiple images  
**Exercise 2:** Implement S3 lifecycle policies to move objects between storage classes  
**Exercise 3:** Set up bucket policies for public/private access control

---

### Module 2: Lambda (Serverless Functions) - Week 3

#### Setup & Exercises

**1. Simple Lambda Function:**

Create `lambda/hello/index.py`:
```python
import json

def lambda_handler(event, context):
    print("Event:", json.dumps(event))
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'Hello from Lambda!',
            'input': event
        })
    }
```

**Deploy Lambda:**
```bash
# Create deployment package
cd lambda/hello
zip function.zip index.py

# Create Lambda function
awslocal lambda create-function \
    --function-name hello-function \
    --runtime python3.9 \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --handler index.lambda_handler \
    --zip-file fileb://function.zip

# Invoke Lambda
awslocal lambda invoke \
    --function-name hello-function \
    --payload '{"name": "World"}' \
    response.json

# View response
cat response.json
```

**2. Lambda with Environment Variables:**

Create `lambda/env-demo/index.py`:
```python
import os
import json

def lambda_handler(event, context):
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '5432')
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'database': f"{db_host}:{db_port}",
            'environment': os.environ.get('ENVIRONMENT', 'dev')
        })
    }
```

```bash
cd lambda/env-demo
zip function.zip index.py

awslocal lambda create-function \
    --function-name env-demo \
    --runtime python3.9 \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --handler index.lambda_handler \
    --zip-file fileb://function.zip \
    --environment Variables="{DB_HOST=postgres-local,DB_PORT=5432,ENVIRONMENT=local}"
```

**3. Lambda with Layers:**

Create `lambda/layer/python/requests_layer.py`:
```bash
# Create layer directory
mkdir -p lambda/layer/python
cd lambda/layer

# Install dependencies
pip3 install requests -t python/

# Create layer zip
zip -r requests-layer.zip python/

# Create layer
awslocal lambda publish-layer-version \
    --layer-name requests-layer \
    --zip-file fileb://requests-layer.zip \
    --compatible-runtimes python3.9
```

**Exercise 1:** Create a Lambda that processes uploaded S3 files  
**Exercise 2:** Build a Lambda that queries DynamoDB and returns results  
**Exercise 3:** Create a scheduled Lambda (cron job) using EventBridge

---

### Module 3: DynamoDB (NoSQL Database) - Week 4

#### Setup & Exercises

**1. Create Table with AWS CLI:**
```bash
# Create Users table
awslocal dynamodb create-table \
    --table-name Users \
    --attribute-definitions \
        AttributeName=user_id,AttributeType=S \
        AttributeName=email,AttributeType=S \
    --key-schema \
        AttributeName=user_id,KeyType=HASH \
    --global-secondary-indexes \
        "[
            {
                IndexName: "EmailIndex",
                KeySchema: [
                    {AttributeName: "email", KeyType: "HASH"}
                ],
                Projection: {
                    ProjectionType: "ALL"
                },
                ProvisionedThroughput: {
                    ReadCapacityUnits: 5,
                    WriteCapacityUnits: 5
                }
            }
        ] \
    --provisioned-throughput \
        ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --tags \
        Key=Project,Value=AWS-Learning \
        Key=Environment,Value=Local
```

**2. Insert Data:**
```bash
# Insert user record
awslocal dynamodb put-item \
    --table-name Users \
    --item '{
        "user_id": {"S": "1001"},
        "email": {"S": "user1@example.com"},
        "name": {"S": "John Doe"},
        "age": {"N": "30"},
        "created_at": {"S": "2024-01-01T12:00:00Z"},
        "tags": {"SS": ["admin", "user"]}
    }'

# Insert another user
awslocal dynamodb put-item \
    --table-name Users \
    --item '{
        "user_id": {"S": "1002"},
        "email": {"S": "user2@example.com"},
        "name": {"S": "Jane Smith"},
        "age": {"N": "25"},
        "created_at": {"S": "2024-01-02T10:00:00Z"},
        "tags": {"SS": ["user"]}
    }'
```

**3. Query and Scan Operations:**
```bash
# Query by primary key
awslocal dynamodb query \
    --table-name Users \
    --key-condition-expression "user_id = :id" \
    --expression-attribute-values '{":id": {"S": "1001"}}'

# Scan with filter
awslocal dynamodb scan \
    --table-name Users \
    --filter-expression "age > :min_age" \
    --expression-attribute-values '{":min_age": {"N": "20"}}'

# Query GSI (EmailIndex)
awslocal dynamodb query \
    --table-name Users \
    --index-name EmailIndex \
    --key-condition-expression "email = :email" \
    --expression-attribute-values '{":email": {"S": "user1@example.com"}}'
```

**4. DynamoDB with Python (boto3):**
```python
# Create DynamoDB client
dynamodb = boto3.client(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

# Put item
dynamodb.put_item(
    TableName='Users',
    Item={
        'user_id': {'S': '1003'},
        'email': {'S': 'user3@example.com'},
        'name': {'S': 'Bob Johnson'},
        'age': {'N': '35'},
        'created_at': {'S': '2024-01-03T08:00:00Z'},
        'tags': {'SS': ['user', 'premium']}
    }
)

# Get item
response = dynamodb.get_item(
    TableName='Users',
    Key={'user_id': {'S': '1001'}}
)
print("User:", response.get('Item'))

# Update item
dynamodb.update_item(
    TableName='Users',
    Key={'user_id': {'S': '1001'}},
    UpdateExpression='SET age = :age, tags = :tags',
    ExpressionAttributeValues={
        ':age': {'N': '31'},
        ':tags': {'SS': ['admin', 'user', 'premium']}
    }
)
```

**Exercise 1:** Create a shopping cart system with DynamoDB  
**Exercise 2:** Implement a rate-limiting system using DynamoDB counters  
**Exercise 3:** Build a user profile system with GSI for email lookups

---

### Module 4: EC2 (Virtual Machines) - Week 5

#### Setup & Exercises

**1. Create EC2 Instance:**
```bash
# Create key pair
awslocal ec2 create-key-pair --key-name my-key-pair

# Create security group
awslocal ec2 create-security-group \
    --group-name my-security-group \
    --description "Security group for local EC2"

# Add inbound rules
awslocal ec2 authorize-security-group-ingress \
    --group-name my-security-group \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

# Create VPC (simplified)
awslocal ec2 create-vpc --cidr-block 10.0.0.0/16

# Create subnet
awslocal ec2 create-subnet \
    --vpc-id <vpc-id> \
    --cidr-block 10.0.1.0/24

# Create instance
awslocal ec2 run-instances \
    --image-id ami-00000000000000000 \
    --instance-type t2.micro \
    --key-name my-key-pair \
    --security-group-ids <security-group-id> \
    --subnet-id <subnet-id> \
    --user-data 'echo "Hello from EC2" > /tmp/ec2-hello.txt'

# Wait for instance to be running
awslocal ec2 wait instance-status-ok --instance-ids <instance-id>

# Get instance IP
awslocal ec2 describe-instances --instance-ids <instance-id> --query 'Reservations[0].Instances[0].PublicIpAddress' --output text
```

**2. EC2 with Python:**
```python
# Create EC2 client
ec2 = boto3.client(
    'ec2',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

# Create instance
response = ec2.run_instances(
    ImageId='ami-00000000000000000',
    InstanceType='t2.micro',
    KeyName='my-key-pair',
    SecurityGroupIds=['sg-00000000000000000'],
    SubnetId='subnet-00000000000000000',
    UserData='echo "Hello from EC2" > /tmp/ec2-hello.txt'
)

instance_id = response['Instances'][0]['InstanceId']
print(f"✅ Created EC2 instance: {instance_id}")
```

**Exercise 1:** Create a web server EC2 instance with Apache/Nginx  
**Exercise 2:** Implement auto-scaling with EC2 instance launch templates  
**Exercise 3:** Set up EC2 instance monitoring with CloudWatch

---

### Module 5: API Gateway & Lambda Integration - Week 6

#### Setup & Exercises

**1. Create REST API:**
```bash
# Create API
api_id=$(awslocal apigateway create-rest-api --name "MyAPI" --query 'id' --output text)

# Create resource
resource_id=$(awslocal apigateway create-resource --rest-api-id $api_id --parent-id $api_id --path-part "users" --query 'id' --output text)

# Create method
awslocal apigateway put-method --rest-api-id $api_id --resource-id $resource_id --http-method GET --authorization-type NONE

# Create integration
awslocal apigateway put-integration --rest-api-id $api_id --resource-id $resource_id --http-method GET --type AWS --integration-http-method POST --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:000000000000:function:hello-function/invocations --content-handling CONVERT_TO_TEXT

# Deploy API
stage_name=$(awslocal apigateway create-deployment --rest-api-id $api_id --stage-name dev --query 'id' --output text)

# Get API endpoint
api_endpoint=$(awslocal apigateway get-rest-api --rest-api-id $api_id --query 'id' --output text)
echo "API Endpoint: http://localhost:4566/restapis/$api_id/$stage_name"
```

**2. Test API:**
```bash
# Test GET request
http GET http://localhost:4566/restapis/$api_id/$stage_name/users

# Test POST request
http POST http://localhost:4566/restapis/$api_id/$stage_name/users name="John Doe" email="john@example.com"
```

**Exercise 1:** Create a CRUD API for user management  
**Exercise 2:** Implement API authentication with IAM roles  
**Exercise 3:** Set up API rate limiting and throttling

---

### Module 6: RDS (Relational Database Service) - Week 7

#### Setup & Exercises

**1. Create RDS Instance:**
```bash
# Create DB subnet group
awslocal rds create-db-subnet-group \
    --db-subnet-group-name my-subnet-group \
    --db-subnet-group-description "Subnet group for local RDS" \
    --subnet-ids <subnet-id>

# Create DB security group
awslocal rds create-db-security-group \
    --db-security-group-name my-rds-security-group \
    --db-security-group-description "Security group for local RDS"

# Create DB instance
awslocal rds create-db-instance \
    --db-instance-identifier my-rds-instance \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username admin \
    --master-user-password password \
    --allocated-storage 20 \
    --db-subnet-group-name my-subnet-group \
    --vpc-security-group-ids <security-group-id> \
    --publicly-accessible \
    --port 5432

# Wait for instance to be available
awslocal rds wait db-instance-available --db-instance-identifier my-rds-instance

# Get endpoint
awslocal rds describe-db-instances --db-instance-identifier my-rds-instance --query 'DBInstances[0].Endpoint.Address' --output text
```

**2. Connect to RDS:**
```bash
# Connect using psql
psql -h <endpoint> -p 5432 -U admin -W

# Create table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

# Insert data
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');
```

**Exercise 1:** Create a user management system with RDS  
**Exercise 2:** Implement database backups and snapshots  
**Exercise 3:** Set up read replicas for high availability

---

### Module 7: ECS (Elastic Container Service) - Week 8

#### Setup & Exercises

**1. Create ECS Cluster:**
```bash
# Create ECS cluster
awslocal ecs create-cluster --cluster-name my-ecs-cluster

# Create task definition
awslocal ecs register-task-definition \
    --family my-web-app \
    --container-definitions '[
        {
            "name": "web-container",
            "image": "nginx:latest",
            "portMappings": [
                {
                    "containerPort": 80,
                    "hostPort": 80,
                    "protocol": "tcp"
                }
            ],
            "essential": true
        }
    ]'

# Create service
awslocal ecs create-service \
    --cluster my-ecs-cluster \
    --service-name my-web-service \
    --task-definition my-web-app \
    --desired-count 1 \
    --launch-type EC2
```

**Exercise 1:** Deploy a containerized web application  
**Exercise 2:** Implement ECS service discovery  
**Exercise 3:** Set up ECS auto-scaling based on CPU usage

---

## Phase 4: Integrated Projects

### Project 1: Simple Web Application (Week 9-10)

**Architecture:**
```
CloudFront (LocalStack) → S3 (Static Website) → API Gateway → Lambda → DynamoDB
```

**Components:**
1. S3 bucket for static website
2. API Gateway for backend API
3. Lambda functions for CRUD operations
4. DynamoDB for data storage
5. CloudFront for content delivery

**Implementation Steps:**
1. Create S3 bucket with index.html
2. Set up API Gateway with Lambda integration
3. Create DynamoDB table for data storage
4. Implement frontend with HTML/JavaScript
5. Test end-to-end functionality

### Project 2: E-Commerce Platform (Week 11-12)

**Architecture:**
```
API Gateway → Lambda → DynamoDB
               ↓
           S3 (Product Images)
               ↓
           CloudFront (CDN)
```

**Features:**
1. Product catalog with search functionality
2. Shopping cart system
3. User authentication with Cognito (simulated)
4. Order processing system
5. Payment integration (simulated)

---

## Learning Resources

### Documentation
- [LocalStack Documentation](https://docs.localstack.cloud/)
- [AWS CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

### Practice Exercises
1. **Daily Challenges**:
   - Create a new AWS service configuration
   - Debug a failing configuration
   - Optimize an existing configuration

2. **Weekly Projects**:
   - Build a complete web application
   - Implement a CI/CD pipeline
   - Create a monitoring dashboard

3. **Final Project**:
   - Design and implement a complete application architecture
   - Document the architecture and implementation
   - Present the solution to a peer group

---

## Maintenance & Updates

### Regular Tasks
1. **Weekly Updates**:
   - Update LocalStack version
   - Review AWS service changes
   - Update documentation

2. **Monthly Reviews**:
   - Audit all configurations
   - Clean up unused resources
   - Update security practices

3. **Quarterly Assessments**:
   - Test all projects
   - Identify learning gaps
   - Plan next learning phase

### Backup Strategy
1. **Configuration Backups**:
   - Store all IaC code in Git
   - Use Git tags for versioning
   - Implement automated backups

2. **Data Backups**:
   - Regularly export DynamoDB data
   - Backup S3 buckets
   - Test restore procedures

---

## Final Notes

1. **Start Small**: Begin with basic services and gradually add complexity
2. **Practice Daily**: Dedicate 30-60 minutes daily to practice
3. **Document Everything**: Keep detailed notes of your configurations
4. **Ask Questions**: Join AWS communities for support
5. **Stay Updated**: AWS services evolve rapidly

This comprehensive plan allows you to learn AWS services on Linux without an AWS account, using LocalStack for local emulation. The hands-on approach with practical exercises and projects will give you real-world experience in AWS architecture and configuration.