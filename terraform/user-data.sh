echo export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" >> /etc/profile
echo export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" >> /etc/profile

sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

sudo chmod 666 /var/run/docker.sock
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 737808743514.dkr.ecr.eu-west-1.amazonaws.com
docker pull 737808743514.dkr.ecr.eu-west-1.amazonaws.com/web-app-review
docker run -d -p 80:8000 737808743514.dkr.ecr.eu-west-1.amazonaws.com/web-app-review

