FROM python:latest

RUN apt-get update 
RUN apt-get install -y tesseract-ocr tesseract-ocr-dev python-opencv libleptonica-dev

WORKDIR  /app/src

COPY requirements.txt ../
RUN pip install --upgrade --no-cache-dir -r ../requirements.txt

COPY src .

# CMD ["python", "main.py"]
