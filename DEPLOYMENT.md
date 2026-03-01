EC2 Deployment Steps
1. Launch EC2
Ubuntu 24.04 LTS
t2.micro
Enable public IP
Security group:
SSH (22) → My IP
Custom TCP (8000) → 0.0.0.0/0

2. SSH
ssh -i job-key.pem ubuntu@<PUBLIC_IP>

3. Install Docker
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
exit

Reconnect after exit.

4. Install docker-compose
sudo apt install docker-compose -y
Check:
docker-compose --version

5. Clone Repo
git clone https://github.com/VaibhavXBhardwaj/Cloud-Native-Distributed-Job-Processing-System
cd Cloud-Native-Distributed-Job-Processing-System

6. Run System
docker-compose up -d --build

7. Access
http://<PUBLIC_IP>:8000/health