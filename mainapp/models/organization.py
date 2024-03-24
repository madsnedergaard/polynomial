from typing import Union

from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models.manager import Manager
from django.urls import reverse

from .user import User


class OrganizationUser(models.Model):
    is_admin = models.BooleanField(default=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,  # Can be null if user is invited but has no account
    )
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
    )
    # Invitations (optional)
    invitation_key = models.UUIDField(unique=True, editable=False, null=True)
    invitee_email = models.EmailField(null=True)
    inviter = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="inviter", null=True
    )

    class Meta:
        unique_together = ("user", "organization", "invitee_email")

    def __str__(self):
        if self.user:
            return "{0} ({1})".format(
                str(self.user) if self.user.is_active else self.user.email,
                self.organization.name,
            )
        else:
            return f"{self.invitee_email} (invited to {self.organization.name})"

    def delete(self, using=None, keep_parents=False) -> tuple[int, dict[str, int]]:
        """
        If the organization user is also the owner, this should not be deleted
        unless it's part of a cascade from the Organization.
        If there is no owner then the deletion should proceed.
        """
        if self.organization.owner.pk == self.pk:
            raise ValueError(
                "Cannot delete organization owner before having transferred ownership"
            )
        return super().delete(using=using, keep_parents=keep_parents)

    def get_absolute_url(self):
        if self.user:
            return reverse(
                "organization_user_detail",
                kwargs={
                    "organization_pk": self.organization.pk,
                    "user_pk": self.user.pk,
                },
            )
        else:
            return reverse("invitation_accept", args=[self.invitation_key])

    def is_owner(self):
        if not self.user:
            return False
        return self.organization.is_owner(self.user)


class Organization(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    organizationuser_set: Manager[OrganizationUser]
    users = models.ManyToManyField(
        User,
        through=OrganizationUser,
        related_name="organization_users",
        through_fields=("organization", "user"),
    )
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    # Used for spreadsheet export
    google_spreadsheet_export_credentials = models.JSONField(blank=True, null=True)
    google_spreadsheet_export_spreadsheet_id = models.CharField(
        max_length=128, blank=True, null=True
    )
    google_spreadsheet_export_sheet_name = models.CharField(
        max_length=128, blank=True, null=True
    )
    # Used for slack notifications
    slack_notifications_credentials = models.JSONField(blank=True, null=True)
    slack_notifications_channel = models.CharField(
        max_length=128, blank=True, null=True
    )

    def __str__(self):
        return self.name

    def add_user(self, user, is_admin=False):
        """
        Adds a new user and if the first user makes the user an admin and
        the owner.
        """
        users_count = self.users.all().count()
        if users_count == 0:
            is_admin = True
        org_user = OrganizationUser.objects.create(
            user=user, organization=self, is_admin=is_admin
        )
        if users_count == 0:
            self.owner = user
            self.save()

        return org_user

    def remove_user(self, user: User):
        org_user = OrganizationUser.objects.get(user=user, organization=self)
        org_user.delete()

    def is_admin(self, user: Union[User, AnonymousUser]):
        if isinstance(user, AnonymousUser):
            return False
        return (
            True
            if self.organizationuser_set.filter(user=user, is_admin=True)
            else False
        )

    def is_owner(self, user: Union[User, AnonymousUser]):
        return self.owner == user

    def is_member(self, user: Union[User, AnonymousUser]):
        return True if user in self.users.all() else False


class OrganizationInvitation(OrganizationUser):
    class Meta:
        proxy = True

    def accept(self, user):
        # Update the associated org user
        self.user = user
        return self.save()
