Ginger arxiv
============

Ginger Engineering Test Project

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Getting Started
---------------
1. Clone this repo:

::

    $ git clone git@github.com:pjhoberman/ginger-arxiv.git pj-ginger-test && cd pj-ginger-test

2. Set up and start a virtual environment

::

    $ python3 -m venv .
    $ source bin/activate

3. Install requirements

::

    $ pip install -r requirements/local.txt

- There are a lot due to cookiecutter so this might take a minute.

4. Create a postgres database named `ginger_arxiv`

5. You can run the server now

::

    $ python manage.py runserver

6. Start redis

- Install redis first if you don't have it.
- You can check if ``$ which redis`` returns a path or nothing.
- Assuming you have homebrew, install redis with ``$ brew update && brew install redis``.

::

    $ redis-server

7. Start celery

::

    $ celery -A config.celery_app worker --loglevel=info

8. To start downloading articles, navigate to http://127.0.0.1:8000/import_articles.

- Note: running a test will go quickly, but will make the full import quit early due to the way the the full import checks for existing entries.
- To run a test and then run the full import, delete all authors and articles.


Notes:

- Not set up for production
- Used cookiecutter but didn't use most of the features yet
- No daemons, all manual for now

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy ginger_arxiv

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html



Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd ginger_arxiv
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.




Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at  https://sentry.io/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.


Deployment
----------

The following details how to deploy this application.


Heroku
^^^^^^

See detailed `cookiecutter-django Heroku documentation`_.

.. _`cookiecutter-django Heroku documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html
