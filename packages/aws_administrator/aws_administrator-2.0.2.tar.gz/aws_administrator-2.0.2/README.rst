=====================
**aws_administrator**
=====================

Overview
--------

Run AWS administrative scripts. Available scripts are in in the package's "scripts" directory: https://gitlab.com/fer1035_python/modules/pypi-aws_administrator/-/tree/main/src/aws_administrator/scripts 
> (see each script's docstring for more information).

Usage
------

Installation:

.. code-block:: BASH

    pip3 install aws_administrator
    # or
    python3 -m pip install aws_administrator

Prerequisite steps:

1. Copy the "parameters/parameters.ini" file: https://gitlab.com/fer1035_python/modules/pypi-aws_administrator/-/blob/main/src/aws_administrator/parameters/parameters.ini to your current working directory.

2. Update the file with the necessary values.

Example (Python shell):

.. code-block:: PYTHON

    # Get AWS SSO Permission Set details from all accounts in an organization.

    from aws_administrator.scripts import aws_sso_get
