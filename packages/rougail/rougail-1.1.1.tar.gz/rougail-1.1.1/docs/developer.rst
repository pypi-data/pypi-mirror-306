Developer notes
==========================

.. admonition:: team developer material

   This section is intended to be usefull for team developers only.


Quick installation process
---------------------------------------

This process describes how to install and run the project locally, e.g. for development purposes.

*Nota*: command is to be executed through the terminal

`pip install rougail`

Code quality
---------------

We are using `pre-commit <https://pre-commit.com/>`_, there is a :file:`.pre-commit-config.yaml`
pre-commit config file in the root's project.

You need to:

- install the pre-commit library::

    pip install pre-commit

- registrer the pre-commit git hooks with this command::

    pre-commit install

- launch the quality code procedure with::

    pre-commit

  or simply just commit your changes, pre-commit will automatically be launched.

.. attention:: If an error is found, the commit will not happen.
   You must resolve all errors that pre-commit that pre-commit points out to you before.

.. note:: If you need for some reason to disable `pre-commit`, just set
          the `PRE_COMMIT_ALLOW_NO_CONFIG` environment variable before commiting::

              PRE_COMMIT_ALLOW_NO_CONFIG=1 git commit

Coding standard
------------------

We use black

.. code-block:: yaml

  - repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
      - id: black

And some YAML and JSON validators.
