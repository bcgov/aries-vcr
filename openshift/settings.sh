export PROJECT_NAMESPACE="devex-von"
export PROJECT_OS_DIR=${PROJECT_OS_DIR:-../../openshift}

# The templates that should not have their GIT referances(uri and ref) over-ridden
# Templates NOT in this list will have they GIT referances over-ridden
# with the values of GIT_URI and GIT_REF
export skip_git_overrides="schema-spy-build.json solr-base-build.json"
export GIT_URI="https://github.com/bcgov/TheOrgBook.git"
export GIT_REF="master"

# The project components
export components="tob-db tob-solr tob-api tob-web tob-wallet tob-ghost"

# The builds to be triggered after buildconfigs created (not auto-triggered)
export builds=""

# The images to be tagged after build
export images="angular-on-nginx django solr schema-spy ghost"

# The routes for the project
export routes="angular-on-nginx django solr schema-spy"
