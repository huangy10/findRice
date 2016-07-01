import os
import datetime

from fabric.api import run, env, cd, sudo, prompt, lcd, local, put
from fabric.contrib.files import exists

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env.hosts = [
    "find_rice_runner@111.206.219.158:22",
]
env.password = "shanghai"


def deploy_bak():
    prompt("Push you local change to github before deployment!\n(Press any key to continue)")

    with cd("/home/findRice"):
        if not exists("./findRice"):
            print "Project not found, cloning from github: https://github.com/huangy10/findRice.git"
            run("git clone https://github.com/huangy10/findRice.git")
    with cd("/home/findRice/findRice"):
        print "Updating source code from github"
        # update remote code
        run("git checkout .")
        run("git pull origin master")
        print "Applying server settings"
        # replace setting file
        run("rm findRice/settings.py")
        run("mv findRice/settings_remote.py findRice/settings.py")
        # database migrations
        migrate_db = prompt("Did you modify the database? [Y/n]", validate=r'[yYNn]')
        if migrate_db in ["Y", "y"]:
            run("workon find_rice_env && python manage.py makemigrations")
            run("workon find_rice_env && python manage.py migrate")
        # restart service
        print "Restarting server"
        sudo("supervisorctl restart find_rice find_rice_celery")


def deploy():
    temp_zip_path = os.path.join(BASE_DIR, "findRice-temp.zip")
    remote_temp_zip_path = "~/findRice-available/findRice-temp.zip"

    if os.path.isfile(temp_zip_path):
        os.remove(temp_zip_path)
    local('cd {base_dir} && zip -r -q findRice-temp findRice -x "./findRice/media/*"'.format(
        base_dir=BASE_DIR
    ))

    if exists(remote_temp_zip_path):
        run("rm {remote_temp_file}".format(remote_temp_file=remote_temp_zip_path))

    put(temp_zip_path, '~/findRice-available/')

    # os.remove(temp_zip_path)

    proj_name = "findRice_{0}".format(datetime.datetime.now().strftime("%y%m%d_%H%M%S"))
    run("unzip -q {0} -d ~/findRice-available/{1}".format(
        remote_temp_zip_path, proj_name
    ))
    remote_proj_path = os.path.join("~/findRice-available", os.path.join(proj_name, "findRice"))

    with cd(remote_proj_path):
        run("rm findRice/settings.py")
        run("mv findRice/settings_remote.py findRice/settings.py")
        migrate_db = prompt("Did you modify the database? [Y/n]", validate=r'[yYNn]')
        if migrate_db in ["Y", "y"]:
            run("workon find_rice_env && python manage.py makemigrations")
            run("workon find_rice_env && python manage.py migrate")

    enabled_proj_path = "~/findRice"
    if exists(enabled_proj_path):
        run("rm {proj}".format(proj=enabled_proj_path))
    run("ln -s {tar} {src}".format(src=enabled_proj_path, tar=remote_proj_path))

    run("rm {remote_temp_zip}".format(remote_temp_zip=remote_temp_zip_path))
    print "Restarting server"
    sudo("supervisorctl restart find_rice find_rice_celery")
