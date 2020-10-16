FROM bcgovimages/aries-cloudagent:py36-1.15-0_0.5.5

RUN pip3 install --no-cache-dir -e "git+https://github.com/bcgov/aries-vcr.git#egg=subdir&subdirectory=server/message_families/issuer_registration"

COPY ./debug-logger.cfg .
