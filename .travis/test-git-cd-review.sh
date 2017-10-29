set -e

# change workdir to travis-gitcd
cd ~/build/claudio-walser/travis-gitcd

/usr/bin/expect <<EOD
spawn git-cd review
expect "Your personal Github token?"
send "$GH_ACCESS_TOKEN\n"
expect "You currently have uncomitted changes. Do you want me to abort and let you commit first?"
send "no\n"
expect "Pull-Request title?"
send "Pull Request Title for travis build $TRAVIS_JOB_NUMBER\n"
expect "Pull-Request body?"
send "Pull Request Body for travis build $TRAVIS_JOB_NUMBER\n"
EOD

# change back to original workdir
cd -
