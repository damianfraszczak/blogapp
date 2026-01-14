Django Docker Project Template
==================================

This is a template project for building a web application using Django, Vue.js and Docker.

Prerequisites
-------------

Before starting, you should have the following software installed on your machine:

*   [Docker](https://www.docker.com/)
*   [Docker Compose](https://docs.docker.com/compose/)


Getting Started
---------------

### Setting up the Backend

To set up the Django backend, navigate to the `root` directory and run the following commands:

```bash
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
docker-compose up -d
```

These commands will start the Docker containers, run the necessary database migrations, and create a superuser for the Django admin interface.

### Accessing the Application

You can access the application by navigating to [http://localhost:8080](http://localhost:8080) in your web browser. You should see a default Vue.js application running.

To access the Django admin interface, navigate to [http://localhost:8000/admin](http://localhost:8000/admin) and log in using the superuser credentials you created earlier.

## Pre-commit Hooks

This project supports [**pre-commit**](https://pre-commit.com/). To use it please install it
in the `pip install pre-commit` and then run `pre-commit install` and you are ready to go.
Bunch of checks will be executed before commit and files will be formatted correctly.

Pre-commit works on staged files while commiting. To run it without a command one should run `pre-commit run`. Changes has to be staged.

To run pre-commit hooks on all changes in the branch:

1.  Sync branch with main
2.  Run `git diff --name-only --diff-filter=MA origin/master | xargs pre-commit run --files`

or you can use it on all files `pre-commit run --all-files`

For branches that are not based on `master` you might replace `origin/master` with `origin/{your_branch}`


License
-------

This project is licensed under the MIT License - see the [LICENSE](LICENCE) file for details.
