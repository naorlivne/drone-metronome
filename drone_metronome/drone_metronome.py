from drone_metronome import *
from parse_it import ParseIt


def init():
    # read envvars
    print("reading envvars")
    parser = ParseIt(recurse=False, envvar_prefix="plugin_")
    metronome_host = parser.read_configuration_variable("metronome_host", default_value="http://metronome.mesos:9000")
    metronome_job_file = parser.read_configuration_variable("metronome_job_file", default_value="metronome.json")
    envvar_dict = read_all_envvars_to_dict()

    # get the job json
    print("reading metronome job json file")
    metronome_job_json = read_file(metronome_job_file)

    # populate the job json with the template data
    print("populating metronome job json file with the templated data")
    metronome_job_json = populate_template_string(metronome_job_json, envvar_dict)

    # create/update metronome job
    print("contacting metronome API")
    metronome_connection = Metronome(metronome_host)
    metronome_connection.create_or_update_metronome_job(metronome_job_json)
    print("finished updating metronome")


if __name__ == "__main__":
    init()
