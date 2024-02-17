from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps

def only_for(role):
    
    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if role == 'user':
                if request.user.is_superuser:
                    return redirect(reverse('admin:index'))
                elif request.user.is_staff:
                    return redirect(reverse('dimpro:control'))
                elif not request.user.is_authenticated:
                    return redirect('dimpro:start')
                else:
                    return view_func(request, *args, **kwargs)
            elif role == 'staff':
                if request.user.is_superuser:
                    return redirect(reverse('admin:index'))
                elif not request.user.is_staff and request.user.is_authenticated:
                    return redirect(reverse('dimpro:index'))
                elif not request.user.is_authenticated:
                    return redirect(reverse('dimpro:start'))
                else:
                    return view_func(request, *args, **kwargs)
            elif role == 'anonymous':
                if request.user.is_superuser:
                    return redirect(reverse('admin:index'))
                elif not request.user.is_staff and request.user.is_authenticated:
                    return redirect(reverse('dimpro:index'))
                elif request.user.is_staff and request.user.is_authenticated:
                    return redirect(reverse('dimpro:control'))
                else:
                    return view_func(request, *args, **kwargs)
            elif role == 'operator':
                if request.user.is_superuser:
                    return redirect(reverse('admin:index'))
                elif not request.user.is_staff and request.user.is_authenticated and request.user.is_operator:
                    return redirect(reverse('dimpro:index'))
                elif not request.user.is_authenticated:
                    return redirect(reverse('dimpro:start'))
                else:
                    return view_func(request, *args, **kwargs)
            else:
                raise ValueError
        return wrapper
    return decorator

