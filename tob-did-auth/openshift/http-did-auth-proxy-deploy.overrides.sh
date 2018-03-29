# ====================================================================================
# Special deployment configuration needed for the http-did-auth-proxy instance.
# ------------------------------------------------------------------------------------
# Load the http-did-auth-proxy configuration as a config map containing a set of
# literal key/value pairs.
# This allows the config map to be mounted as a set of environment variables.
# ====================================================================================

CONFIG_MAP_NAME=http-did-auth-proxy-config
SOURCE_FILE_NAME=./http-did-auth-proxy
SOURCE_FILE_EXT=.config
OUTPUT_FORMAT=json
OUTPUT_FILE=http-did-auth-proxy-configmap_DeploymentConfig.json

generateConfigMapAsLiterals() {  
  _config_map_name=${1}
  _source_file=${2}
  _output_format=${3}
  _output_file=${4}
  if [ -z "${_config_map_name}" ] || [ -z "${_source_file}" ] || [ -z "${_output_format}" ] || [ -z "${_output_file}" ]; then
    echo -e \\n"generateConfigMapAsLiterals; Missing parameter!"\\n
    exit 1
  fi

  _env_vars=$(<${_source_file})
  for _var in ${_env_vars}; do
    _literals="${_literals} --from-literal=${_var}"
  done

  oc create configmap ${_config_map_name} ${_literals} --dry-run -o ${_output_format} > ${_output_file}
}

resolveSourceFile() {
  _source_file_name=${1}
  _source_file_ext=${2}
  _env_name=${3}

  if [ ! -z "${_env_name}" ]; then
    _source_file="${_source_file_name}.${_env_name}${_source_file_ext}"
  fi

  if [ -f "${_source_file}" ]; then
    echo "${_source_file}"
  else
    echo "${_source_file_name}${_source_file_ext}"
  fi
}

SOURCE_FILE=$(resolveSourceFile "${SOURCE_FILE_NAME}" "${SOURCE_FILE_EXT}" "${DEPLOYMENT_ENV_NAME}")
generateConfigMapAsLiterals "${CONFIG_MAP_NAME}" "${SOURCE_FILE}" "${OUTPUT_FORMAT}" "${OUTPUT_FILE}"

echo ${SPECIALDEPLOYPARMS}

