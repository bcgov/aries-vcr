# FROM bcgovimages/aries-cloudagent:py36-1.11-1_0.3.2
FROM tob-agent:latest

RUN pip3 install --no-cache-dir -e "git+https://github.com/bcgov/indy-catalyst.git@master#egg=subdir&subdirectory=credential-registry/message_families/issuer_registration"
