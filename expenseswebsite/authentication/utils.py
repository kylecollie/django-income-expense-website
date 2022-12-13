from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AppTokenGenerator(PasswordResetTokenGenerator):
    