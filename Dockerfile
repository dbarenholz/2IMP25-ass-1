FROM python:3

ADD entry_script.py /
ADD helpers.py /
ADD preprocessing.py /
ADD requirements.txt /
ADD stopwords.txt /

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "./entry_script.py" ]   