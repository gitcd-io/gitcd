# . .travis/exit-on-error.sh

git-cd version
echo $?
#exitOnError()
if [ $? != 0 ]; then
    exit $?
fi
