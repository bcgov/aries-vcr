FROM ghcr.io/hyperledger/aries-cloudagent-python:py3.9-indy-1.16.0-0.12.1

RUN pip3 install --no-cache-dir -e "git+https://github.com/bcgov/aries-vcr.git#egg=issuer-registration&subdirectory=server/message_families/issuer_registration"

COPY ./debug-logger.cfg .
