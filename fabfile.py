from fabric.api import run, env, cd, sudo, prompt, lcd, local
from fabric.contrib.files import exists

env.hosts = [
    "find_rice_runner@111.206.219.158:22",
]
env.password = "shanghai"


def deploy():
    with cd("/home/findRice"):
        if not exists("./findRice"):
            print "Project not found, cloning from github: https://github.com/huangy10/findRice.git"
            run("git clone https://github.com/huangy10/findRice.git")
    with cd("/home/findRice/findRice"):
        print "Updating source code from github"
        # update remote code
        run("git fetch")
        run("git pull origin master")
        print "Applying server settings"
        # replace setting file
        sudo("rm findRice/settings.py")
        sudo("mv findRice/settings_remote.py findRice/settings.py")
        # database migrations
        migrate_db = prompt("Did you modify the database? [Y/n]", validate=r'[yYNn]')
        if migrate_db in ["Y", "y"]:
            run("workon find_rice_env && python manage.py makemigrations")
            run("workon find_rice_env && python manage.py migrate")
        # restart service
        print "Restarting server"
        sudo("supervisorctl restart find_rice find_rice_celery")


