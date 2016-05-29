from fabric.api import run, env, cd

env.hosts = ["zuolu@111.206.219.158"]
env.password = "Zuolu0504"


def host_type():
    run("uname -s")

