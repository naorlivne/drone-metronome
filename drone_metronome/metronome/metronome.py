import requests


class Metronome:

    def __init__(self, metronome_host: str = "http://metronome.mesos:9000"):
        """Init the metronome api conenction object with host & headers

            Arguments:
                metronome_host -- the url of the metronome host without a trailing slash (/), defaults to
                "http://metronome.mesos:9000"
        """
        self.headers = {
            'cache-control': "no-cache",
            'Connection': "keep-alive",
            'Content-Type': "application/json"
        }
        self.metronome_host = metronome_host
        self.timeout = 60

    def check_metronome_job_exists(self, job_name: str) -> bool:
        """Checks if a given metronome jobs exists or not & raise an error if it can't tell

            Arguments:
                job_name -- a string to apply the templating to without a prefixed slash (/)
            Returns:
                True if the job exists, False if it's not
        """

        url = self.metronome_host + "/v1/jobs/" + job_name

        # only need the status code to tell if a job exist so HEAD is less traffic
        response = requests.request("HEAD", url, headers=self.headers, timeout=self.timeout)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        else:
            print("unable to determine if metronome job exists")
            raise Exception

    def create_metronome_job(self, job_json: str) -> dict:
        """creates a metronome jobs & raise an error if it can't

            Arguments:
                job_json -- a string of the job JSON description (string because it's taken directly from a file)
            Returns:
                response_json -- the response JSON returned from metronome
        """

        url = self.metronome_host + "/v0/scheduled-jobs"

        response = requests.request("POST", url, headers=self.headers, timeout=self.timeout, data=job_json,)
        if response.status_code == 201:
            return response.json()
        else:
            print(response.json())
            print("failed creating metronome job")
            raise Exception

    # update existing metronome job

    # create or update metronome job
