from typing import TYPE_CHECKING, Any, Tuple

from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from hct_mis_api.apps.account.models import User

from .models import APIToken

if TYPE_CHECKING:
    from requests import Request


class HOPEAuthentication(TokenAuthentication):
    keyword = "Token"

    def authenticate_credentials(self, key: str) -> Tuple[User, APIToken]:
        try:
            token = (
                APIToken.objects.select_related("user")
                .filter(valid_from__lte=timezone.now())
                .filter(Q(valid_to__gte=timezone.now()) | Q(valid_to__isnull=True))
                .get(key=key)
            )
        except APIToken.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_("User inactive or deleted."))

        return (token.user, token)


class HOPEPermission(IsAuthenticated):
    def has_permission(self, request: Request, view: Any) -> bool:  # type: ignore
        if bool(request.auth):
            if view.permission == "any":
                return True
            elif view.permission:
                return view.permission.name in request.auth.grants
        return False
