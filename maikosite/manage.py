#!/opt/rh/python27/root/usr/bin/python

##/usr/bin/env python
import os
import sys

from sdg.scl import SDGCollections
SDGCollections.enable('python27', 'sdg_2015a_python27')

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
