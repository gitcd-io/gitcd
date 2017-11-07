set -e

# change workdir to travis-gitcd
cd ~/build/claudio-walser/travis-gitcd

# git-cd finish with deleting the feature branch
/usr/bin/expect <<EOD
spawn git-cd release
expect "What message your new tag should have?"
send "New Travis Release by File\n"
expect
EOD

cat done.txt

# assert that the new tag exists

# change back to original workdir
cd -