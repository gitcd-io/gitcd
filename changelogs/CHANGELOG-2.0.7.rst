Changelog for version 2.0.7
===========================

Moved .gitcd-personal
#####################

The personal config file including the token for opening pull requests on github was moved from your current repository into ~/.gitcd/access-token and prepared to store a bitbucket token as well.

There is code to check if you don't have an access-token file yet in your home folder and if it finds a .gitcd-personal in your current repository, it will move it. I don't remove the entry for the file in .gitignore by intend, you may delete it manually if you are sure none of your teammates will commit his token by accident. I might do this by code in some month, still have to think about it.


Improved docs
#############

Docs where improved and adapted more closely with the online version on https://www.gitcd.io. Also screenshots are included on github and on readthedocs now.


Introduced Changelogs
#####################

I also decided to introduce changelogs to let you follow changes more closely.
This is the first changelog and i hope you like it.