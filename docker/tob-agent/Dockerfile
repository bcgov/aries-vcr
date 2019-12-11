# Use stable alpha image while awaiting the official 0.4.x release
FROM bcgovimages/aries-cloudagent:py36-1.11-1_0.4.0-alpha3

RUN pip3 install --no-cache-dir -e "git+https://github.com/bcgov/indy-catalyst.git@master#egg=subdir&subdirectory=credential-registry/message_families/issuer_registration"
COPY ./debug-logger.cfg .
