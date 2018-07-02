FROM python:3.6.5

RUN apt-get update 
RUN apt-get install -y tesseract-ocr tesseract-ocr-dev python-opencv libleptonica-dev

WORKDIR  /app/src

COPY requirements.txt ../
RUN pip install --upgrade --no-cache-dir -r ../requirements.txt

CMD ["python", "main.py"]
