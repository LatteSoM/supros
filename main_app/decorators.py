from django.http import HttpResponseForbidden
from functools import wraps

from django.shortcuts import redirect


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role.name not in allowed_roles:
                return redirect('forbidden')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


