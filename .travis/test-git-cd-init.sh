set -e

# git-cd init with accepting all the defaults
/usr/bin/expect <<EOD
spawn git-cd init
expect "Branch name for production releases?"
send "\n"
expect "Branch name for feature development?"
send "\n"
expect "Branch name for test releases?"
send "\n"
expect "Version tag prefix?"
send "\n"
expect "Version type? You can either set your tag number manually, read it from a version file or generate it by date."
send "\n"
expect "Do you want to execute some additionalcommands after a release?"
send "\n"
EOD
