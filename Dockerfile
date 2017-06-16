FROM alpine:3.5
RUN apk add --no-cache py-pip
ADD . /usr/app/toy_app
WORKDIR /usr/app/toy_app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["toy_app.py"]
