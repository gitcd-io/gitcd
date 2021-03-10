set -e

# change workdir to travis-gitcd
cd ~/build/gitcd-io/travis-gitcd

# write version file because git-cd init checks its existence
echo $TRAVIS_JOB_NUMBER.1 > version.txt

# git-cd init with accepting all the defaults
/usr/bin/expect <<EOD
spawn git-cd init
expect "Branch name for production releases?"
send "\n"
expect "Branch name for feature development?"
send "feature/\n"
expect "Branch name for test releases?"
send "test\n"
expect "Version tag prefix?"
send "\n"
expect "Version type? You can either set your tag number manually, read it from a version file or generate it by date."
send "file\n"
expect "From what file do you want to load your version?"
send "version.txt\n"
expect "Do you want to execute some additionalcommands after a release?"
send "echo 'well done' > done.txt\n"
expect "Do you want to execute some additionalcommands before a release?"
send "\n"
expect
EOD

cat .gitcd | grep "versionType: file"

# change back to original workdir
cd -
