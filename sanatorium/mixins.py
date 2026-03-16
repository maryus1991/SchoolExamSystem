from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from user.models import User

class SanatorPermissionRequire(LoginRequiredMixin):
    """for set the sanator perimission ro enter the panel"""

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        if request.user.is_staff and request.user.type_of_user == User.TypeOfUser.SANATORUM:
            return response
        else:
            raise Http404()