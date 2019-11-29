FROM bcgovimages/aries-cloudagent:py36-1.11-1_0.3.5
#FROM bcgovimages/aries-cloudagent:py36-1.11-1_0.4.0-alpha1

RUN pip3 install --no-cache-dir -e "git+https://github.com/bcgov/indy-catalyst.git@master#egg=subdir&subdirectory=credential-registry/message_families/issuer_registration"
COPY ./debug-logger.cfg .
