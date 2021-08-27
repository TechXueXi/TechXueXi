

from pdlearn import globalvar


def get_docker_mode():
    return globalvar.nohead


def prompt(prompt_str):
    if get_docker_mode() == False:
        return input(prompt_str)
    else:
        pass

