FROM aries-agent

RUN pip3 install --no-cache-dir -e "git+https://github.com/bcgov/indy-catalyst.git@master#egg=subdir&subdirectory=credential-registry/message_families/issuer_registration"

ENTRYPOINT ["/bin/bash", "-c", "icatagent \"$@\"", "--"]
