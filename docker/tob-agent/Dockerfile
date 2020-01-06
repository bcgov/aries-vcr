# FROM bcgovimages/aries-cloudagent:py36-1.11-1_0.4.0

FROM bcgovimages/von-image:py36-dev 

RUN pip3 install aries-cloudagent

RUN pip3 install --no-cache-dir -e "git+https://github.com/bcgov/indy-catalyst.git@master#egg=subdir&subdirectory=credential-registry/message_families/issuer_registration"
COPY ./debug-logger.cfg .