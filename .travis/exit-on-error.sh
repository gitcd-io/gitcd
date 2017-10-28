exitOnError() {
    if [ $? != 0 ]; then
        exit $?
    fi
}
