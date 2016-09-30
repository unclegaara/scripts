#!/bin/bash
set -u -e
retcode=0
host=""
user=""
password=""
dir="$(date +%Y_%m_%d)"

mkdir "$dir"
for db_name in $(< $1)
do
    T="$(date +%Y_%m_%d_%H:%M)"
    dump_name="${db_name}_$T.sql"
    echo "db_$db_name backup start time $T"
    if ! ssh "$host" "mysqldump '$db_name' -u '$user' -p'$password' > '$db_name'_'$T'.sql"; then
        echo "mysqldump or ssh failed" 2>&1
        retcode=1
        continue
    fi
    if ! scp -q "$host":"$dump_name" "$dir"; then
        echo "scp failed" 2>&1
        retcode=1
        continue
    fi
    echo "$dump_name copying succeeded, removing remote copy..." 2>&1
    ssh "$host" "rm $dump_name" || true
    echo "removing completed!" 2>&1
    echo "db_$db_name backup end time $(date +%Y_%m_%d_%H:%M)" 2>&1
done
exit $retcode
