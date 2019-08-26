import os


# read all envvars to dict
def read_all_envvars_to_dict() -> dict:
    """Read all environment variables and return them in a dict form, if

            Arguments:
                force_uppercase -- while counter-intuitive in the naming it means that if the environment variable
                    is uppercase the dict will treat it as the same one as a lowercase one & will return it in
                    lowercase form (name saved to match all the other uses of said function)
            Returns:
                envvar_dict -- A dict of all environment variables key/value pairs
        """
    envvar_dict = {}
    for envvar in os.environ:
        envvar_dict[envvar] = os.environ.get(envvar)
    return envvar_dict
