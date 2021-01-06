# 自动化测试python脚本镜像
FROM python:3.7.3-alpine

WORKDIR /usr/src/app

COPY . .

# log,result,report 路径必须存在
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r requirements.txt && mkdir -p ./log && mkdir -p ./result && mkdir -p ./report

ENTRYPOINT ["pytest"]