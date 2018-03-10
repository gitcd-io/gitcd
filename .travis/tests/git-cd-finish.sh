set -e

# change workdir to travis-gitcd
cd ~/build/gitcd-io/travis-gitcd

# git-cd finish with deleting the feature branch
/usr/bin/expect <<EOD
spawn git-cd finish
expect "Delete your feature branch?"
send "yes\n"
expect
EOD

# assert that the feature branch doesent exists anymore

# change back to original workdir
cd -