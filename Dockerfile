FROM centos/python-38-centos7

EXPOSE 8080

USER 1001

RUN pip install --upgrade pip

# Install pip requirements
ADD requirements.txt /opt/app-root/src/requirements.txt
ADD app/ /opt/app-root/src/app
ADD tests/ /opt/app-root/src/tests
ADD migrations/ /opt/app-root/src/migrations
ADD wsgi.py /opt/app-root/src/wsgi.py
ADD conf/ /opt/app-root/src/conf

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8080", "wsgi:application"]
