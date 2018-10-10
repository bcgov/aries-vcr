# Setting for the TheOrgBook-BC environments.
# Uses the existing `devex-von-tools` environment for builds and images
export TOOLS="devex-von-tools"
export PROJECT_NAMESPACE="devex-von-bc-tob"

# The project components
export components="tob-db tob-solr tob-api tob-web tob-wallet tob-backup"

export skip_git_overrides="${skip_git_overrides} backup-build.json"
