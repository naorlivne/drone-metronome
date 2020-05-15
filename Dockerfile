FROM python:3.8.3-alpine3.10

COPY . /drone_metronome

RUN pip install -r /drone_metronome/requirements.txt

WORKDIR /drone_metronome

CMD ["python", "/drone_metronome/drone_metronome_runner.py"]