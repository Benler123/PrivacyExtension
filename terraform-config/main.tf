provider "aws" {
  region = "us-east-1"  # N. Virginia region
}

# VPC Configuration
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "web-server-vpc"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "web-server-igw"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"

  tags = {
    Name = "web-server-subnet"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  tags = {
    Name = "web-server-rt"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Security Group
resource "aws_security_group" "web" {
  name        = "web-server-sg"
  description = "Security group for web server"
  vpc_id      = aws_vpc.main.id

  # SSH access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP access
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS access
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Uvicorn port
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web-server-sg"
  }
}

# EC2 Instance
resource "aws_instance" "web" {
  ami           = "ami-0c7217cdde317cfec"  # Ubuntu 22.04 LTS in us-east-1
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public.id
  key_name      = "my-ec2-key"

  root_block_device {
    volume_size = 8
    volume_type = "gp2"
  }

  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = <<-EOF
              #!/bin/bash
              # Update system
              apt-get update
              apt-get upgrade -y

              # Install required packages
              apt-get install -y python3-pip python3-venv nginx git supervisor

              # Create app directory
              mkdir -p /app
              cd /app

              # Clone repository
              git clone https://github.com/Benler123/PrivacyExtension.git .

              # Create and activate virtual environment
              python3 -m venv venv
              source venv/bin/activate

              # Install Python packages
              pip install fastapi uvicorn
              if [ -f requirements.txt ]; then
                pip install -r requirements.txt
              fi

              # Create supervisor configuration for Uvicorn
              cat > /etc/supervisor/conf.d/uvicorn.conf <<EOL
              [program:uvicorn]
              command=/app/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000 --workers 2
              directory=/app
              user=www-data
              autostart=true
              autorestart=true
              stopasgroup=true
              killasgroup=true
              stderr_logfile=/var/log/uvicorn.err.log
              stdout_logfile=/var/log/uvicorn.out.log
              EOL

              # Configure Nginx as reverse proxy
              cat > /etc/nginx/sites-available/default <<EOL
              server {
                  listen 80 default_server;
                  listen [::]:80 default_server;

                  server_name _;

                  location / {
                      proxy_pass http://127.0.0.1:8000;
                      proxy_set_header Host \$host;
                      proxy_set_header X-Real-IP \$remote_addr;
                      proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
                      proxy_set_header X-Forwarded-Proto \$scheme;

                      # WebSocket support
                      proxy_http_version 1.1;
                      proxy_set_header Upgrade \$http_upgrade;
                      proxy_set_header Connection "upgrade";
                  }
              }
              EOL

              # Set proper permissions
              chown -R www-data:www-data /app

              # Start services
              systemctl restart nginx
              systemctl enable supervisor
              systemctl start supervisor
              supervisorctl reread
              supervisorctl update
              supervisorctl start uvicorn
              EOF

  tags = {
    Name = "web-server"
  }
}

# Outputs
output "public_ip" {
  value = aws_instance.web.public_ip
}

output "public_dns" {
  value = aws_instance.web.public_dns
}
