exitOnError () {
  rtnCd=$?
  if [ ${rtnCd} -ne 0 ]; then
	echo "An error has occurred!  Please check the previous output message(s) for details."
    exit ${rtnCd}
  fi
}

isLocalCluster (){
  rtnVal=$(oc project | grep '[//127.0|//10.0]')
  if [ -z "$rtnVal" ]; then
    # Not a local cluster ..."
	return 1
  else
    # Is a local cluster ..."
	return 0
  fi
}

projectExists (){
  project=$1
  cmd="oc projects | grep '\s"${project}"$'"
  rtnVal=$(eval ${cmd})
  if [ -z "${rtnVal}" ]; then
    # Project does not exist ..."
	  return 1
  else
    # Project exists ..."
	  return 0
  fi
}

assignRole (){
  role=$1
  user=$2
  project=$3
  
  echo "Assigning role [${role}], to user [${user}], in project [${project}] ..."
  oc policy add-role-to-user ${role} ${user} -n ${project}
  echo
}