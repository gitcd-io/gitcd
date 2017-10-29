trap "exit 1" TERM
export TOP_PID=$$

function exitOnError()
{
    if [ $? != 0 ]; then
        kill -s TERM $TOP_PID
    fi
}
