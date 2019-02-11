queryPattern=${1}
blacklistRaw=${2:-blacklist.raw}
blacklistConf=${3:-blacklist.conf}

echo "" >> ${blacklistConf}

# Generate a blacklist from the logs
# - Exclude IPs that are already being blocked.
# - Include queries matching suspicious pattern(s)
# - Filter out any cruft
# - Remove duplicate lines
sed '/access forbidden by rule/d' ${blacklistRaw} \
  | sed "/${queryPattern}/!d" \
  | sed -r 's~(^.*) - - .*$~deny \1;~' \
  | sed '/deny/!d' \
  | awk '!seen[$0]++' >> ${blacklistConf}

# Remove any duplicat entries
awk '!seen[$0]++' ${blacklistConf} > ${blacklistConf}.tmp
rm ${blacklistConf}
mv ${blacklistConf}.tmp ${blacklistConf}