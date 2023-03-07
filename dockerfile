FROM alpine

EXPOSE 5000

RUN apk update
RUN apk add python3
RUN apk add git
RUN apk add py3-pip

RUN git clone https://github.com/PvonK/final_c2

WORKDIR /final_c2

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py" ]
