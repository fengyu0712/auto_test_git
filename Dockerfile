# 自动化测试python脚本镜像
FROM python:3.7.3-alpine

WORKDIR /usr/src/app

COPY . .

# log,result,report 路径必须存在
#RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --no-cache-dir -r requirements.txt --proxy='http://aicloud-privoxy.midea.com' && mkdir -p ./log && mkdir -p ./result && mkdir -p ./report
RUN pip install --no-cache-dir -r requirements.txt --proxy='http://aicloud-privoxy.midea.com' && mkdir -p ./log && mkdir -p ./result && mkdir -p ./report

ENTRYPOINT ["pytest"]