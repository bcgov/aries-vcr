# Example patterns:
# - "api\/search\/credential\/topic?name="
queryPattern=${1:-"api\/search\/credential\/topic?name="}

echoYellow (){
  _msg=${1}
  _yellow='\e[33m'
  _nc='\e[0m' # No Color
  echo -e "${_yellow}${_msg}${_nc}"
}

startLineCount=$(wc -l < blacklist.conf)

echo ""
echoYellow "$(date)"

echo "Dumping a recent copy of the logs ..."
echo "" > blacklist.raw
oc -n devex-von-bc-tob-prod get pods -o name -l app=angular-on-nginx | xargs -I {} oc -n devex-von-bc-tob-prod logs {} >> blacklist.raw

echo "Building blacklist ..."
./blackListBuilder.sh "${queryPattern}"

endLineCount=$(wc -l < blacklist.conf)
addedLines=$(expr ${endLineCount} - ${startLineCount})
echoYellow "- ${addedLines} new entries where added to the list."

if (( ${addedLines} > 0 )); then
  echo -e \\n"Generating updated config map ..."
  cd ..
  ./angular-on-nginx-deploy.overrides.sh

  echo "Updating config map ..."
  oc -n devex-von-bc-tob-prod replace -f ./blacklist-conf-configmap_DeploymentConfig.json

  echo "Rolling out angular-on-nginx with updated blacklist..."
  oc -n devex-von-bc-tob-prod rollout latest dc/angular-on-nginx
else
  echo -e \\n"No updates needed."
fi

rm -f blacklist.raw
