from six import text_type
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivation(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk) + text_type(timestamp) +
                text_type(user.email_verified))

activater = AccountActivation()
