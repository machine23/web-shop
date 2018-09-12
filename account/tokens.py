from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ActivationTokenGenerator(PasswordResetTokenGenerator):
    key_salt = 'account.tokens.ActivationTokenGenerator'

    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + user.email + str(timestamp)


account_activation_token = ActivationTokenGenerator()
