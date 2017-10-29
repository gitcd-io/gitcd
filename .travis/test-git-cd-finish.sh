set -e

# change workdir to travis-gitcd
cd ~/build/claudio-walser/travis-gitcd

# git-cd finish with deleting the feature branch
/usr/bin/expect <<EOD
spawn git-cd finish
expect "Delete your feature branch?"
send "\n"
EOD

# change back to original workdir
cd -