
```bash
# git setting
git config --global --get-all safe.directory
git config --global --add safe.directory '//wsl.localhost/Ubuntu/home/tanaka/sd-upload-image-to-s3'

# aws cli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

aws configure --profile userprofile
# AWS Access Key ID [None]: XXXXXXXXXXXXXXX
# AWS Secret Access Key [None]: XXXXXXXXXXXXXXXXXXXXXXX
# Default region name [None]: us-east-1
# Default output format [None]: 

export AWS_PROFILE=userprofile
aws configure list


# paperspace
sudo ./aws/install
mkdir ~/.aws
cp credentials ~/.aws/

aws --version

# バケット確認
aws s3 ls --profile userprofile
# 転送
aws s3 mv stable-diffusion-webui/outputs/ s3://mybucket/outputs/ --recursive --profile userprofile
```