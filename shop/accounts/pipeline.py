from .models import CustomUser


def associate_by_email(strategy, details, backend, uid, user=None, *args, **kwargs):

    if user:
        return {'user': user}

    email = details.get('email')

    if email:
        try:
            custom_user = CustomUser.objects.get(email=email)
            return {'user': custom_user}
        except CustomUser.DoesNotExist:
            pass

    return {}