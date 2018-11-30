from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
import logging
import os
from smtplib import SMTP, SMTPException

LOGGER = logging.getLogger(__name__)


def email_feedback(reply_name, reply_email, reason, comments):
    server_addr = os.getenv('SMTP_SERVER_ADDRESS')
    recip_email = os.getenv('FEEDBACK_TARGET_EMAIL')
    from_name = 'BC OrgBook'
    from_email = 'no-reply@orgbook.gov.bc.ca'

    reason_text = {
        "incorrect": "Reporting incorrect information",
        "additional": "Requesting additional information on BC organizations",
        "signup": "Looking to sign up my government organization",
        "developer": "Developer request",
    }

    subject = 'OrgBook Feedback: {}'.format(reason_text.get(reason))

    LOGGER.info("Received feedback from %s <%s>", reply_name, reply_email)
    LOGGER.info("Feedback content: %s\n%s", subject, comments)

    if not reason or not reply_email:
        LOGGER.info("Skipped blank feedback")
        return False

    if server_addr and recip_email:
        msg = MIMEText(comments, 'text')
        recipients = ",".join(recip_email)
        from_line = formataddr( (str(Header(from_name, 'utf-8')), from_email) )
        reply_line = formataddr( (str(Header(reply_name, 'utf-8')), reply_email) )
        msg['Subject'] = subject
        msg['From'] = from_line
        msg['Reply-To'] = reply_line
        msg['To'] = recip_email
        LOGGER.info("encoded:\n%s", msg.as_string())

        with SMTP(server_addr) as smtp:
            try:
                smtp.sendmail(from_line, (recip_email,), msg.as_string())
                LOGGER.debug("Feedback email sent")
            except SMTPException:
                LOGGER.exception("Exception when emailing feedback results")


    return True
