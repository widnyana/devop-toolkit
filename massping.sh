#!/bin/bash
#: ping list of IP.
#:
#: usage:
#: put list of target, one address per line inside file named: "massping_target" in the same dir with this script.

cat ./massping_target |  while read output
do
    ping -c 1 "$output" >> /dev/null
    if [ $? -eq 0 ]; then
    echo "node $output is up" 
    else
    echo "node $output is down"
    fi
    echo -e "==================================\n\n"
done
