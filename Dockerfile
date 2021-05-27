FROM tensorflow/tensorflow
FROM pytorch/pytorch

COPY requirements.txt . 

RUN pip install -r requirements.txt 

COPY code.py .

CMD ["python3", "code.py"]
