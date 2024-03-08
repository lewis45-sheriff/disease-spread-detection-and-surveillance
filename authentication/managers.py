from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, role, password=None, **extra_fields):
        if role not in ['admin', 'healthcare_worker']:
            raise ValueError('User must have role="admin" or role="healthcare_worker".')

        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
