# accounts/decorators.py
from functools import wraps

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.http import JsonResponse
from django.shortcuts import render


def role_required(allowed_roles):
    """
    دکوریتور برای محدود کردن دسترسی به نقش‌های خاص
    سوپرادمین به همه چیز دسترسی داره
    """
    if isinstance(allowed_roles, str):
        allowed_roles = (allowed_roles,)
    else:
        allowed_roles = tuple(allowed_roles)

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(
                    request.get_full_path(),
                    settings.LOGIN_URL,
                )

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if request.user.role not in allowed_roles:
                accepts_json = 'application/json' in request.headers.get('accept', '')
                if (
                    request.headers.get('x-requested-with') == 'XMLHttpRequest'
                    or accepts_json
                ):
                    return JsonResponse({'error': 'دسترسی غیرمجاز'}, status=403)

                return render(request, '403.html', status=403)

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
