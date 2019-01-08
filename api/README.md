# Reviews API #

## Dependencies ##

* git
* sqlite3
* python 3.7.2
* virtualenv
* virtualenvwrapper

Installation:
```
cd ~/
mkdir .virtualenvs
mkdir projects
# Create a backup of your .bashrc file
cp ~/.bashrc ~/.bashrc-org

edit .bashrc:
# where to store our virtual envs
export WORKON_HOME=$HOME/.virtualenvs
# where projects will reside
export PROJECT_HOME=$HOME/projects
# where is the virtualenvwrapper.sh
source /usr/local/bin/virtualenvwrapper.sh

git clone <this project>

cd ~/projects/api

mkvirtualenv -a ~/projects/api -p /usr/local/bin/python3.7 -r requirements/develop.txt 

python manage.py migrate

python manage.py createsuperuser

python -m pytest trsAPI/reviews/tests

python manage.py runserver 0.0.0.0:7777
```

http://localhost:7777/admin/ - admin/superuser dashboard

http://localhost:7777/api/docs/ - docs of API

about authentication - https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication

Then its better to upgrade to posgresql database.
