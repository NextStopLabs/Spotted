from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.db import IntegrityError
from django.contrib.auth.models import User
from posts.models import UserProfile

class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def filter_users_by_claims(self, claims):
        """Find existing users by OIDC subject or email."""
        sub = claims.get('sub')
        email = claims.get('email')

        if sub:
            return UserProfile.objects.filter(oidc_sub=sub)
        elif email:
            return User.objects.filter(email__iexact=email)
        return User.objects.none()

    def create_user(self, claims):
        """Create a user or link to an existing one."""
        sub = claims.get('sub')
        email = claims.get('email')
        username = claims.get('preferred_username') or email

        # Check if there's already a user with this email
        existing_user = User.objects.filter(email__iexact=email).first()
        if existing_user:
            # Link OpenID identity to existing account
            UserProfile.objects.filter(user=existing_user).update(oidc_sub=sub)
            print(f"Linked existing user {existing_user.username} to OIDC sub {sub}")
            return existing_user

        try:
            # Otherwise, create a new user
            user = User.objects.create_user(
                username=username,
                email=email,
            )
            UserProfile.objects.create(user=user, oidc_sub=sub)
            user.save()
            print(f"Created new user {user.username} for OIDC sub {sub}")
            return user
        except IntegrityError:
            # Handle rare race conditions (two users with same username/email)
            user = User.objects.filter(email=email).first()
            if user:
                user.oidc_sub = sub
                user.save()
                return user
            raise

    def login_user(self, user, claims):
        """Fetch or create (link) a user on login."""
        sub = claims.get('sub')
        email = claims.get('email')

        # Try by sub first
        user = UserProfile.objects.filter(oidc_sub=sub).first()

        # If not found, fall back to email and link
        if not user and email:
            existing_user = User.objects.filter(email__iexact=email).first()
            if existing_user:
                existing_user.oidc_sub = sub
                existing_user.save()
                user = existing_user

        # Create if nothing exists
        if not user:
            user = self.create_user(claims)

        return user
