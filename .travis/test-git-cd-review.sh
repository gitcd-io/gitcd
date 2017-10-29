set -e

# change workdir to travis-gitcd
cd ~/build/claudio-walser/travis-gitcd
git status
git diff

/usr/bin/expect <<EOD
spawn git-cd review
expect "Your personal Github token?"
send "$GH_ACCESS_TOKEN\n"
expect "Pull-Request title?"
send "Pull Request Title for travis build $TRAVIS_JOB_NUMBER\n"
expect "Pull-Request body?"
send "Pull Request Body for travis build $TRAVIS_JOB_NUMBER\n"
EOD

# change back to original workdir
cd -
