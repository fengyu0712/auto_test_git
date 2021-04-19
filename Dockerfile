# 自动化测试python脚本镜像
FROM python:3.7.3

# 更新Alpine的软件源为阿里云，因为从默认官源拉取实在太慢了
RUN echo https://mirrors.aliyun.com/alpine/v3.10/main/ > /etc/apk/repositories && \
    echo https://mirrors.aliyun.com/alpine/v3.10/community/ >> /etc/apk/repositories

# 添加时区支持
RUN apk add -U tzdata

WORKDIR /usr/src/app

COPY . .

# upgrade pip
RUN pip --no-cache-dir install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com --upgrade pip && rm -rf /var/lib/apt/lists/*

# install python components
RUN pip install --user -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r requirements.txt

# log,result,report 路径必须存在
RUN mkdir -p ./log && mkdir -p ./result && mkdir -p ./report

ENTRYPOINT ["pytest"]