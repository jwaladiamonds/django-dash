from six import text_type
from django.conf import settings as conf
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivation(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk) + text_type(timestamp) +
                text_type(user.email_verified))


class Gmail:

    def __init__(self):
        self.activated = False
        self.flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_file=conf.GMAIL_SECRET,
            scopes=conf.GMAIL_SCOPES,
            redirect_uri=conf.GMAIL_REDIRECT)
        self.auth_uri, self.auth_state = self.flow.authorization_url()

    def verify(self, code):
        try:
            self.flow.fetch_token(code=code)
            self.credentials = self.flow.credentials
            self.service = build('gmail', 'v1', credentials=self.credentials)
            self.email = conf.GMAIL_USER + " <" + (self.service.users().getProfile(
                userId="me").execute())['emailAddress'] + ">"
            self.activated = True
        except:
            self.revoke()

    def revoke(self):
        if hasattr(self, 'service'):
            self.service.close()
        self.activated = False
        self.credentials = None
        self.service = None
        self.email = None

    def set_state_session(self, request):
        request.session['oauth_state'] = self.auth_state

    def _create_message(self, subject, message_text, from_email, recipient_list, html):
        message = MIMEMultipart()
        message['to'] = ', '.join(recipient_list)
        message['from'] = from_email
        message['subject'] = subject
        if html:
            message.attach(MIMEText(message_text, 'html'))
        else:
            message.attach(MIMEText(message_text, 'plain'))
        raw = urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw': raw}

    def send_mail(self, subject, message, recipient_list, html=False):
        if self.activated:
            try:
                body = self._create_message(
                    subject,
                    message,
                    self.email,
                    recipient_list,
                    html)
                sent_message = (self.service.users().messages().send(
                    userId="me",
                    body=body).execute())
                print('Message sent with id: %s' % sent_message['id'])
            except HttpError as error:
                print('An error occurred: %s' % error)
        else:
            print("Gmail not activated")


activater = AccountActivation()
mailer = Gmail()
