FROM python:3.13.0a2-alpine3.19

ENV API_KEY=bRBk9qircBeL0vegXBbgVAaPTBE96UqeWcC65evRCkW5oegVzjx7AmYD7uAtT8o2

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python main.py -i
RUN python main.py -add

CMD ["python", "main.py", "-p", "80"]
