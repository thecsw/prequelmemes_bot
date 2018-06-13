FROM python:latest

RUN apt-get update 
RUN apt-get install -y tesseract-ocr tesseract-ocr-dev python-opencv libleptonica-dev

WORKDIR  /app/src
ADD . /app

RUN pip install --upgrade --no-cache-dir -r ../requirements.txt

CMD ["python", "main.py"]
