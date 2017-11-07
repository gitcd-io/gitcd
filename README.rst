Continuous tool for working with git
====================================

**Development Status**

.. image:: https://img.shields.io/pypi/status/gitcd.svg
   :target: https://pypi.org/project/gitcd/

.. image:: https://travis-ci.org/claudio-walser/gitcd.svg?branch=master
    :target: https://travis-ci.org/claudio-walser/gitcd

.. image:: https://readthedocs.org/projects/gitcd/badge/?version=latest
    :target: https://gitcd.readthedocs.org/en/latest/?badge=latest

.. image:: https://img.shields.io/github/last-commit/claudio-walser/gitcd.svg
    :target: https://github.com/claudio-walser/gitcd/commits/master



**Package Info**

.. image:: https://badge.fury.io/py/gitcd.svg
    :target: https://pypi.org/project/gitcd/

.. image:: https://img.shields.io/pypi/wheel/gitcd.svg
    :target: https://pypi.org/project/gitcd/

.. image:: http://img.shields.io/badge/license-APACHE2-blue.svg
    :target: https://github.com/claudio-walser/gitcd/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/pyversions/gitcd.svg
    :target: https://pypi.org/project/gitcd/


Description
-----------

**gitcd** is a little helper for continuous integration workflows using
git as scm.

Installation
------------

Since gitcd is using python3 by default, you better upgrade.

After successful installation of python3 and pip for pyhton3, run the following command to install or upgrade gitcd:

.. code:: console

    pip3 install --user --upgrade gitcd

If you are on mac osx and your local python folder isn't in your PATH variable you might add it to $PATH or symlink it in /usr/local/bin with sudo.

**Max OSX**

.. code:: console

    sudo ln -s /Users/<username>/Library/Python/<python-version>/bin/git-cd /usr/local/bin/

The same applies to linux, however, the path is different. (On usual Distributions this is in $PATH already)

.. code:: console

    sudo ln -s /home/<username>/.local/bin/git-cd /usr/local/bin/

Argument Completion
-------------------

Gitcd supports argument completion, to activate this feature in linux run:

.. code:: console

    sudo activate-global-python-argcomplete3

Under OSX it isn't that simple unfortunately. Global completion requires bash support for complete -D, which was introduced in bash 4.2. On OS X or older Linux systems, you will need to update bash to use this feature. Check the version of the running copy of bash with echo $BASH_VERSION. On OS X, install bash via Homebrew (brew install bash), add /usr/local/bin/bash to /etc/shells, and run chsh to change your shell.
Afterwards you might be able to also just run:

.. code:: console

    sudo activate-global-python-argcomplete3

Usage
-----

Check version and upgrade
~~~~~~~~~~~~~~~~~~~~~~~~

Gitcd is aware of it's local and remote versions and may upgrade itself if you want to.

.. code:: console

    git cd upgrade


Initialize a project
~~~~~~~~~~~~~~~~~~~~

cd into one of your local directories
representing a git repository and run the init command. Pass your configuration, for most cases the default values should be ok.

.. code:: console

    git cd init


Pull request status
~~~~~~~~~~~~~~~~~~~

You are able to see the status of a feature
branch including the pull request and if it has already been reviewed by
someone.

.. code:: console

    git cd status


Clean up local branches
~~~~~~~~~~~~~~~~~~~~~~~

The tool is able to cleanup all local
branches which doesent exist on the origins. This is done with the clean command.

.. code:: console

    git cd clean


Start new feature
~~~~~~~~~~~~~~~~~

Starts a new feature branch from your master branch. If you dont pass a branchname, you will be asked later.

.. code:: console

    git cd start <branchname>


Test a feature branch
~~~~~~~~~~~~~~~~~~~~~

Merges a feature branch into your development branch. If you dont pass a branchname, your current branch will be taken.

.. code:: console

    git cd test <branchname>


Open a pull request for code review
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Opens a pull request to your master branch. If you dont pass a branchname, your current branch will be taken.

.. code:: console

    git cd review <branchname>


Finish a feature branch
~~~~~~~~~~~~~~~~~~~~~~~

Merges it into your master and asks for permission to delete your
feature branch. If you dont pass a branchname, your current branch will be taken.

.. code:: console

    git cd finish <branchname>


Compare your current branch
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compares your current branch against the given branchname or the latest
tag if none is given.

.. code:: console

    git cd compare <branchname>


Tagging the master branch
~~~~~~~~~~~~~~~~~~~~~~~~~

Creates a tag from your master branch and pushes it to remote.

.. code:: console

    git cd release


Known Issues
------------

If you discover any bugs, feel free to create an issue on GitHub fork
and send us a pull request.

`Issues List`_.


Authors
-------

-  Claudio Walser (https://github.com/claudio-walser)
-  Gianni Carafa (https://github.com/mms-gianni)


Contributing
------------

1. Fork it
2. Create your feature branch (``git cd start my-new-feature``)
3. Commit your changes (``git commit -am 'Add some feature'``)
4. Push to the branch (``git push origin feature/my-new-feature``)
5. Create new Pull Request (``git cd review my-new-feature``)


License
-------

Apache License 2.0 see
https://github.com/claudio-walser/gitcd/blob/master/LICENSE

.. _Issues List: https://github.com/claudio-walser/gitcd/issues
