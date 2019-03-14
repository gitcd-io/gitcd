set -e

CURRENT_VERSION=$(cat version.txt)

/usr/bin/expect <<EOD
spawn git-cd version
expect "You run git-cd in version $CURRENT_VERSION\n"
expect
EOD
