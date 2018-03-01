.. image:: https://www.gitcd.io/images/logo.svg
    :height: 150px
    :width: 150px


************************************
Continuous tool for working with git
************************************

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
###########

**gitcd** is a little helper for continuous delivery workflows, using git as scm.


Installation of gitcd
#####################



Pre requisites
--------------
Gitcd is written in Python3. Most systems still deliver with Python2 as default.
You need to install Python3 in order to run gitcd properly.

MacOSX
______

.. code-block:: bash

    brew install python3

Ubuntu / Debian
_______________

.. code-block:: bash

    sudo apt-get install python3 python3-pip





Installation of gitcd itself
----------------------------
Now you are ready to install gitcd itself, which is quite easy using pip.

.. code-block:: bash

    pip3 install --user --upgrade gitcd


Trouble using git-cd?
---------------------
If the command "git-cd" or "git cd" is not available now, you probably need to add the pip binary path to your $PATH variable.

MacOSX
______

Open ~/.bash_profile in your favorite editor and add the following lines at the end of the file.

.. container:: alert alert-warning

    **Replace <python-version> with your currently installed python version**

.. code-block:: bash

    if [ -d "$HOME/Library/Python/<python-version>/bin" ] ; then
        PATH="$HOME/Library/Python/<python-version>/bin:$PATH"
    fi

Ubuntu / Debian
_______________

Open ~/.profile in your favorite editor and add the following lines at the end of the file.

.. code-block:: bash

    if [ -d "$HOME/.local/bin" ] ; then
        PATH="$HOME/.local/bin:$PATH"
    fi


Argument Completion
-------------------
Gitcd supports argument completion, to activate it execute the following steps.

MacOSX
______

Under OSX it isn't that simple unfortunately. Global completion requires bash support for complete -D, which was introduced in bash 4.2. On OS X or older Linux systems, you will need to update bash to use this feature. Check the version of the running copy of bash with echo $BASH_VERSION. On OS X, install bash via Homebrew (brew install bash), add /usr/local/bin/bash to /etc/shells, and run chsh to change your shell.

You might consider reading the docs for argcomplete https://argcomplete.readthedocs.io/en/latest/#global-completion

Activate Global argcomplete
_____________________________

You are now ready to activate global argcompletion for python with the following command.

.. code-block:: bash

    activate-global-python-argcomplete




CLI Usage of gitcd
##################

For convenience, you can call gitcd as a git sub command as well as directly. Therefore, you can replace "git cd" in any of the following commands with "git-cd" if you like it more.


.. container:: alert alert-warning

    **Note: Python argument completion wont work if you use it as a git sub command!**


Initializing gitcd
------------------
First of all you probably want to initialize one of your local git repositories with gitcd. Change directory to one of your local git repositories and run git-cd init.
Most of the values should be very self-explanatory. Still, here is a complete list of values you can pass.

- **Branch name for production releases?**

  - This is the branch git-cd is creating a tag from if you execute the release command, you probably want to go with **master** here.

- **Branch name for feature development?**

  - This is more kind of a prefix for feature branches, it is empty by default. If you wish your feature branch has a name like feature/my-new-feature, you can set this prefix to **feature/**.

- **Branch name for test releases?**

  - Pass your branch name where you want to merge code into while executing git-cd test. Let it empty if you don't want to use that feature. At work, we have this for many repositories set to **test**.

- **Version tag prefix?**

  - Prefix for your release tags, this is **v** by default which would result in a tag equals to v0.0.1 for example.

- **Version type? You can either set your tag number manually, read it from a version file or generate it by date.**

  - This is about how git-cd release gets your current version number you want to release.

    - manual means you'll get asked to enter the version number by hand
    - file means gitcd reads the version number from a file, you'll be asked from which file in the next step
    - date means you generate a version number from a date scheme, you'll be asked for the scheme later. As a date version scheme, you can pass any directive for http://strftime.org/.

- **Do you want to execute some additional commands after a release?**

  - This is useful if you want to execute any cli script after creating a tag, for example, gitcd itself uses such a script to publish the new release on pypi after creating a new tag. You can see the script here https://github.com/claudio-walser/gitcd/blob/master/publish.sh.


.. code-block:: bash

    git cd init

The image below represents the configuration for gitcd itself.

.. container:: responsive-image

    .. image:: https://www.gitcd.io/images/cli/git-cd_init.png
        :alt: git cd init


Check version and upgrade
-------------------------
Gitcd is able to check your local version with the one published on pypi and upgrade itself if you wish so.

.. code-block:: bash

    git cd upgrade

.. container:: responsive-image

    .. image:: https://www.gitcd.io/images/cli/git-cd_upgrade-2.png
        :alt: git cd upgrade


Clean up local branches
-----------------------
The tool is able to cleanup all local branches which doesn't exist on remotes. This is done with the clean command.

.. code-block:: bash

    git cd clean

.. container:: responsive-image

    .. image:: https://www.gitcd.io/images/cli/git-cd_clean-2.png
        :alt: git cd clean


Start a new feature
-------------------
Starts a new feature branch from your master branch. If you don't pass a branch name, you will be asked later.

.. code-block:: bash

    git cd start <branchname>

.. container:: responsive-image

    .. image:: https://www.gitcd.io/images/cli/git-cd_start.png
        :alt: git cd start


Testing a feature
-----------------
You might have a testing environment or want to run some integration test on a shared or common branch without the need to push out your feature with the next release. Therefore you can't merge it into the master. That's exactly why the git-cd test command exists. You might even have some dedicated tester checking the new feature on this specific branch. So to merge your new feature into your testing branch you call this command, if you don't pass a branch name, your current feature branch will be merged.

.. code-block:: bash

    git cd test <branchname>

.. container:: responsive-image

    .. image:: https://www.gitcd.io/images/cli/git-cd_test.png
        :alt: git cd test


Open a pull request for code review
-----------------------------------
Opens a pull request to your master branch. If you don't pass a branch name, your current branch will be taken.

.. code-block:: bash

    git cd review <branchname>

.. container:: responsive-image

    .. image:: https://www.gitcd.io/images/cli/git-cd_review.png
        :alt: git cd review


See the status of a pull request
--------------------------------
You can see the status of a pull request directly in the command line. If you don't pass a branch name, your current branch will be taken.

.. code-block:: bash

    git cd status <branchname>

.. container:: responsive-image

    .. image:: https://www.gitcd.io/images/cli/git-cd_status.png
        :alt: git cd status

Finish a feature branch
-----------------------
If your pull request got approved by a fellow developer and all your tests were running properly, you probably want to merge your feature into the master branch. If you don't pass a branch name, your current branch will be taken.

.. code-block:: bash

    git cd finish <branchname>

.. container:: responsive-image

    .. image:: https://www.gitcd.io/images/cli/git-cd_finish.png
        :alt: git cd finish


Compare different branches or tags
----------------------------------
By now, your code is in the master branch. Personally, I always like to see what I am going to release by comparing the current branch (which is master after the finish) against the latest tag. If you don't pass a branch or tag name, the latest tag will be taken.

.. code-block:: bash

    git cd compare <branchname>||<tagname>

.. container:: responsive-image

    .. image:: https://www.gitcd.io/images/cli/git-cd_compare.png
        :alt: git cd compare


Release a new version
---------------------
Now your feature is merged and you made sure you know the changes going out, you are ready to ship it. This command creates a new tag from the master branch and executes any command you've setup in the initialize command.

.. code-block:: bash

    git cd release

.. container:: responsive-image

    .. image:: https://www.gitcd.io/images/cli/git-cd_release.png
        :alt: git cd release

Known Issues
############

If you discover any bugs, feel free to create an issue on GitHub fork
and send us a pull request.

`Issues List`_.


Authors
#######

-  Claudio Walser (https://github.com/claudio-walser)
-  Urban Etter (https://github.com/mms-uret)
-  Gianni Carafa (https://github.com/mms-gianni)


Contributing
############

1. Fork it
2. Add this repository as an origin (``git remote add upstream https://github.com/claudio-walser/gitcd.git``)
3. Create your feature branch (``git cd start my-new-feature``)
4. Commit your changes (``git commit -am 'Add some feature'``)
5. Push to the branch (``git push origin feature/my-new-feature``)
6. Create new Pull Request against upstream (``git cd review my-new-feature``)


License
#######

Apache License 2.0 see
https://github.com/claudio-walser/gitcd/blob/master/LICENSE

.. _Issues List: https://github.com/claudio-walser/gitcd/issues

