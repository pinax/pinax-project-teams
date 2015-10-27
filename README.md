Pinax Project Teams
========================

[![Join us on Slack](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)


Pinax
-------

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable Django apps, themes, and starter project templates. 
This collection can be found at http://pinaxproject.com.


pinax-project-teams
--------------------

`pinax-project-teams` is a starter project that has account management with profiles and teams and basic
collaborative content (wikis). It's a good demonstration of integration of [pinax-teams](http://github.com/pinax/pinax-teams/)
and [pinax-wiki](http://github.com/pinax/pinax-wiki)

The source code for this project template has moved to the [teams-wiki branch](https://github.com/pinax/pinax-projects/tree/team-wiki) of [pinax-projects](https://github.com/pinax/pinax-projects/).


Prerequisites
--------------

* pip
* npm


Getting Started
-----------------

You can get started with this project by doing the following:

```
pip install virtualenv
virtualenv mysiteenv
source mysiteenv/bin/activate
pip install Django==1.8.3
django-admin.py startproject --template=https://github.com/pinax/pinax-project/zipball/teams-wiki mysite -n webpack.config.js
cd mysite
chmod +x manage.py
pip install -r requirements.txt
npm install
./manage.py migrate
./manage.py loaddata sites
./manage.py runserver
```

Static Media
-------------

Static media is managed by `webpack`, and is configured out of the box to watch
and rebuild on change by running:

```
npm run watch
```

We recommend running that in a separate terminal window than `manage.py runserver`
if and when you are editing `js` or `less` files.


Documentation
--------------

The pinax-project-teams documentation is currently under construction. If you would like to help us write documentation, please join our Slack channel and let us know! The Pinax documentation is available at http://pinaxproject.com/pinax/.


Code of Conduct
----------------

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a code of conduct, which can be found here  http://pinaxproject.com/pinax/code_of_conduct/.


Pinax Project Blog and Twitter
--------------------------------

For updates and news regarding the Pinax Project, please follow us on Twitter at [@pinaxproject](https://twitter.com/pinaxproject) and check out our blog http://blog.pinaxproject.com.


