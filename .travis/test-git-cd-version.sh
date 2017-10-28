# . .travis/exit-on-error.sh

git-cd version

#exitOnError()
if [ $? != 0 ]; then
	echo "Exit code is not 0"
    exit 1
fi
