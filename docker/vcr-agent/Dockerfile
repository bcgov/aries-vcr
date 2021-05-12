FROM bcgovimages/aries-cloudagent:py36-1.16-0_0.7-pre.0

RUN pip3 install --no-cache-dir -e "git+https://github.com/bcgov/aries-vcr.git@issuer-agency#egg=issuer-registration&subdirectory=server/message_families/issuer_registration"

COPY ./debug-logger.cfg .
