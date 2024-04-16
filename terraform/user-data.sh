sudo yum update -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo service docker start
sudo systemctl enable docker

sudo usermod -a -G docker ec2-user
ECR_LOGIN_PASSWORD=$(aws ecr get-login-password --region eu-west-1)
aws ecr --region eu-west-1 | docker login -u AWS -p ${ECR_LOGIN_PASSWORD}
docker pull 737808743514.dkr.ecr.eu-west-1.amazonaws.com/web-app-review
