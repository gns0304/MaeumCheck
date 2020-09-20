from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import get_object_or_404

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maeumCheck.settings")
django.setup()

def refreshUsername(request):
    user = get_object_or_404(User, username=request.user)
    userName = user.get_full_name()
    socialUser = get_object_or_404(SocialAccount, user=request.user)
    if userName == "" or userName != socialUser.extra_data['name']:
        user.first_name = socialUser.extra_data['name']
        user.last_name = socialUser.uid
        user.save()

    return user.first_name
