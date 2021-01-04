# 自动化测试python脚本镜像
FROM python:3.7.3-alpine

WORKDIR /usr/src/app

COPY . .

# log,result,report 路径必须存在
RUN pip install --no-cache-dir -r requirements.txt --proxy='http://aicloud-privoxy.midea.com' && mkdir -p ./log && mkdir -p ./result && mkdir -p ./report

ENTRYPOINT ['/usr/local/bin/pytest', '/usr/src/app']