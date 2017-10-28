# . .travis/exit-on-error.sh

git-cd version
#exitOnError()
if [ $? != 0 ]; then
    exit $?
fi
