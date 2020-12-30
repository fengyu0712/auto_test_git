# 自动化测试python脚本镜像
FROM python:3.7.3-alpine

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt --proxy='http://aicloud-privoxy.midea.com'