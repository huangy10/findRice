from fabric.api import run, env, cd, sudo, prompt, lcd, local

env.hosts = [
    "find_rice_runner@111.206.219.158:22",
]
env.password = "shanghai"


def get_latest_project_file():
    with cd("/home/findRice/findRice"):
        # update remote code
        run("git fetch")
        run("git merge")
        # replace setting file
        run("rm findRice/settings.py")
        run("mv findRice/settings_remote.py findRice/settings.py")
        # database migrations
        migrate_db = prompt("Did you modify the database? [Y/n]", validate=r'[yYNn]')
        if migrate_db in ["Y", "y"]:
            run("workon find_rice_env && python manage.py makemigrations")
            run("workon find_rice_env && python manage.py migrate")
        # restart service
        sudo("supervisorctl restart find_rice")
        sudo("supervisorctl restart find_rice_celery")


def test_local():
    with lcd("~/Project"):
        local("ls -al")

