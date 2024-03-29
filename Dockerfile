FROM python:3.11.0b1-alpine3.14

COPY . /drone_metronome

RUN pip install -r /drone_metronome/requirements.txt

WORKDIR /drone_metronome

CMD ["python", "/drone_metronome/drone_metronome_runner.py"]