FROM python:latest

ADD requirements.txt /

RUN pip install -r requirements.txt

ADD entry_script.py /
ADD helpers.py /
ADD preprocessing.py /
ADD input_output.py /
ADD stopwords.txt /

ENTRYPOINT [ "python", "./entry_script.py" ] 