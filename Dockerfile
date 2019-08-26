FROM python:3.7.4-alpine3.10

COPY . /drone_metronome

RUN pip install -r /drone_metronome/requirements.txt

CMD ["python", "/drone_metronome/drone_metronome_runner.py"]