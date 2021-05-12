FROM bcgovimages/aries-cloudagent:py36-1.16-0_0.7-pre.0

# RUN pip3 install --no-cache-dir -e "git+https://github.com/bcgov/aries-vcr.git#egg=issuer-registration&subdirectory=server/message_families/issuer_registration"
RUN pip3 install --no-cache-dir -e "git+https://github.com/petridishdev/aries-vcr.git@feature/issuer-agency#egg=issuer-registration&subdirectory=server/message_families/issuer_registration"

COPY ./debug-logger.cfg .
