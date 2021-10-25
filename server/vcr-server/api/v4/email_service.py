import logging
import os
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
from smtplib import SMTP, SMTPException

LOGGER = logging.getLogger(__name__)


def email_contact(reply_name, reply_email, reason, comments, error=None, identifier=None):
    server_addr = os.getenv("SMTP_SERVER_ADDRESS")
    recip_email = os.getenv("FEEDBACK_TARGET_EMAIL").split(",")
    app_url = os.getenv("APPLICATION_URL")

    from_name = "OrgBook BC"
    from_email = "no-reply@orgbook.gov.bc.ca"

    reason_map = {
        "incorrect": "Reporting incorrect information",
        "additional": "Requesting additional information on BC organizations",
        "signup": "Looking to sign up my government organization",
        "developer": "Developer request",
    }
    reason_text = reason_map.get(reason) or reason

    subject = "OrgBook BC Contact: {}".format(reason_text)

    LOGGER.info("Received contact from %s <%s>", reply_name, reply_email)
    LOGGER.info("Contact request content: %s\n%s", subject, comments)

    if not reason or not reply_email:
        LOGGER.info("Skipped blank contact")
        return False

    if server_addr and recip_email:
        body = ""
        if app_url:
            body = "{}Application URL: {}\n".format(body, app_url)
        if reply_name:
            body = "{}Name: {}\n".format(body, reply_name)
        if reply_email:
            body = "{}Email: {}\n".format(body, reply_email)
        if reason_text:
            body = "{}Contact reason: {}\n".format(body, reason_text)
        if error:
            body = "{}Incorrect information: {}\n".format(body, error)
        if identifier:
            body = "{}Identifier: {}\n".format(body, identifier)
        if comments:
            body = "{}Comments:\n{}\n".format(body, comments)
        msg = MIMEText(body, "plain")
        recipients = ",".join(recip_email)
        from_line = formataddr((str(Header(from_name, "utf-8")), from_email))
        reply_line = formataddr((str(Header(reply_name, "utf-8")), reply_email))
        msg["Subject"] = subject
        msg["From"] = from_line
        msg["Reply-To"] = reply_line
        msg["To"] = recipients
        # LOGGER.info("encoded:\n%s", msg.as_string())

        with SMTP(server_addr) as smtp:
            try:
                smtp.sendmail(from_line, recip_email, msg.as_string())
                LOGGER.debug("Feedback email sent")
            except SMTPException:
                LOGGER.exception("Exception when emailing feedback results")

    return True


def email_feedback(reason, comments, improvements=None):
    server_addr = os.getenv("SMTP_SERVER_ADDRESS")
    recip_email = os.getenv("FEEDBACK_TARGET_EMAIL").split(",")
    app_url = os.getenv("APPLICATION_URL")

    from_name = "OrgBook BC"
    from_email = "no-reply@orgbook.gov.bc.ca"

    reason_text = reason

    subject = "OrgBook BC Feedback: {}".format(reason_text)

    LOGGER.info("Feedback content: %s\n%s", subject, comments)

    if not reason:
        LOGGER.info("Skipped blank feedback")
        return False

    if server_addr and recip_email:
        body = ""
        if app_url:
            body = "{}Application URL: {}\n".format(body, app_url)
        if reason_text:
            body = "{}Contact reason: {}\n".format(body, reason_text)
        if comments:
            body = "{}Comments:\n{}\n".format(body, comments)
        if improvements:
            body = "{}Improvements:\n{}\n".format(body, improvements)
        msg = MIMEText(body, "plain")
        recipients = ",".join(recip_email)
        from_line = formataddr((str(Header(from_name, "utf-8")), from_email))
        msg["Subject"] = subject
        msg["From"] = from_line
        msg["To"] = recipients
        # LOGGER.info("encoded:\n%s", msg.as_string())

        with SMTP(server_addr) as smtp:
            try:
                smtp.sendmail(from_line, recip_email, msg.as_string())
                LOGGER.debug("Feedback email sent")
            except SMTPException:
                LOGGER.exception("Exception when emailing feedback results")

    return True


