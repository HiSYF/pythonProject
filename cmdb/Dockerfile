FROM python:3.9
WORKDIR /root/flask_lhapp/flaskProject/
COPY requirements.txt /root/flask_lhapp/flaskProject/
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && wget https://nodejs.org/dist/v16.17.0/node-v16.17.0-linux-x64.tar.gz \
    && tar --strip-components 1 -xzvf node-v* -C /usr/local
COPY . /root/flask_lhapp/flaskProject/

RUN python manager.py db init \
    && python manager.py db migrate \
    && python manager.py db upgrade
CMD ["gunicorn", "app:app", "-c", "gunconf.py"]
