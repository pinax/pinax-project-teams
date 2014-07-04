pinax-project-teams
===================

a starter project that has account management with profiles and teams
and basic collaborative content (wikis).



Usage:

    django-admin.py startproject -e py,.coveragerc --template=https://github.com/pinax/pinax-project-teams/zipball/master <project_name>


Getting Started:

    pip install virtualenv
    virtualenv mysiteenv
    source mysiteenv/bin/activate
    pip install Django==1.6.5
    django-admin.py startproject -e py,.coveragerc --template=https://github.com/pinax/pinax-project-teams/zipball/master mysite
    cd mysite
    pip install -r requirements.txt
    python manage.py syncdb
    python manage.py runserver
