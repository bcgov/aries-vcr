FROM bcgovimages/aries-cloudagent:py36-1.14-1_0.4.5

RUN pip3 install aries-cloudagent

RUN pip3 install --no-cache-dir -e "git+https://github.com/bcgov/indy-catalyst.git@master#egg=subdir&subdirectory=server/message_families/issuer_registration"
COPY ./debug-logger.cfg .
