> **Warning**
> Drone cloud stopped working for months and as the developers of Drone seemed to stop caring I'm no longer able to fully test this nor will I longer have any use of it, as a result I'm stopping all development of this plugin.

# drone-metronome

CI/CD build status: [![Build Status](https://cloud.drone.io/api/badges/naorlivne/drone-metronome/status.svg)](https://cloud.drone.io/naorlivne/drone-metronome)

Code coverage: [![codecov](https://codecov.io/gh/naorlivne/drone-metronome/branch/master/graph/badge.svg)](https://codecov.io/gh/naorlivne/drone-metronome)

Drone plugin for deploying to [metronome](https://dcos.github.io/metronome/).

## Usage

This plugin can be used to deploy applications to a Metronome server, it will create\update the given Metronome tasks as needed.

The below pipeline configuration demonstrates simple usage:

> In addition to the `.drone.yml` file you will need to create a `metronome.json` file that contains the Metronome configuration. Please see [here](test/test_files/metronome.json) for an example. 

```yaml
kind: pipeline
type: docker
name: default

steps:
- name: metronome_deploy
  image: naorlivne/drone-metronome
  settings:
    metronome_host: http://metronome.mesos:9000
    metronome_job_file: metronome.json
```

### Value substitution

Example configuration with values substitution:
```yaml
kind: pipeline
type: docker
name: default

steps:
- name: metronome_deploy
  image: naorlivne/drone-metronome
  settings:
    metronome_host: http://metronome.mesos:9000
    metronome_job_file: metronome.json
    my_image_tag: my_dynamic_image
```

In the metronome.json file (please note the $ before the PLUGIN_MY_IMAGE_TAG key):

```json
{
  ...
  "image": "myrepo/myimage:$PLUGIN_MY_IMAGE_TAG",
  ...
}
```

will result in:

```json
{
  ...
  "image": "myrepo/myimage:my_dynamic_image",
  ...
}
```

## Parameter Reference

#### metronome_host

The Metronome server URL (no trailing slash should be used), defaults to `http://metronome.mesos:9000`

#### metronome_job_file

The Metronome configuration file location relative to the root folder of the repo, defaults to `metronome.json`
