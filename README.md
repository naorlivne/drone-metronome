# drone-metronome

CI/CD build status: [![Build Status](https://cloud.drone.io/api/badges/naorlivne/drone-metronome/status.svg)](https://cloud.drone.io/naorlivne/drone-metronome)

Code coverage: [![codecov](https://codecov.io/gh/naorlivne/drone-metronome/branch/master/graph/badge.svg)](https://codecov.io/gh/naorlivne/drone-metronome)

Drone plugin for deploying to [metronome](https://dcos.github.io/metronome/).

Drone plugin to build and publish Docker images to a container registry. For the usage information and a listing of the available options please take a look at [the docs](http://plugins.drone.io/drone-plugins/drone-docker/).

## Usage

This plugin can be used to deploy applications to a Metronome server. The below pipeline configuration demonstrates simple usage:

```yaml
pipeline:
name: default

steps:
- name: metronome_deploy
  image: naorlivne/drone-metronome
  settings:
    metronome_host: http://metronome.mesos:9000
    metronome_job_file: metronome.json
```
