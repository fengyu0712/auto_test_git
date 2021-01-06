# 自动化测试python脚本镜像
FROM python:3.7.3-alpine

# 更新Alpine的软件源为阿里云，因为从默认官源拉取实在太慢了
RUN echo http://mirrors.aliyun.com/alpine/v3.10/main/ > /etc/apk/repositories && \
    echo http://mirrors.aliyun.com/alpine/v3.10/community/ >> /etc/apk/repositories

# 添加时区支持
RUN apk add -U tzdata

WORKDIR /usr/src/app

COPY . .

# log,result,report 路径必须存在
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r requirements.txt && mkdir -p ./log && mkdir -p ./result && mkdir -p ./report

ENTRYPOINT ["pytest"]