#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
<<<<<<< HEAD
from django.core.management.commands.runserver import Command as Runserver
=======
>>>>>>> 130d08e2b406837cdb4158d192f7bd40c689a511


def main():
    """Run administrative tasks."""
<<<<<<< HEAD
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CPCS.settings')
=======
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
>>>>>>> 130d08e2b406837cdb4158d192f7bd40c689a511
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
<<<<<<< HEAD
    Runserver.default_addr = '127.0.0.1'
    Runserver.default_port = '9000'
    main()

# python manage.py runserver
=======
    main()
>>>>>>> 130d08e2b406837cdb4158d192f7bd40c689a511
