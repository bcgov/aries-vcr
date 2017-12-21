export PROJECT_NAMESPACE="devex-von"

# The templates that should not have their GIT referances(uri and ref) over-ridden
# Templates NOT in this list will have they GIT referances over-ridden
# with the values of GIT_URI and GIT_REF
export -a skip_git_overrides=("schema-spy-build.json" "solr-base-build.json")
export GIT_URI="https://github.com/bcgov/TheOrgBook.git"
export GIT_REF="master"

# The project components
export -a components=("tob-db" "tob-solr" "tob-api" "tob-web")

# The builds to be triggered after buildconfigs created (not auto-triggered)
export -a builds=("nginx-runtime" "angular-builder")

# The images to be tagged after build
export -a images=("angular-on-nginx" "django" "solr" "schema-spy")

# The routes for the project
export -a routes=("angular-on-nginx" "django" "solr" "schema-spy")