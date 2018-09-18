from urllib.parse import urlsplit
from urllib.request import urlopen
from django.core.files.base import ContentFile
from django.conf import settings

if settings.DEBUG:
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context


def save_user_profile(backend, user, response, *args, **kwargs):
    if 'gender' in response:
        if response['gender'] == 'male':
            user.profile.gender = user.profile.MALE
        else:
            user.profile.gender = user.profile.FEMALЕ

    if 'image' in response and 'url' in response['image']:
        r = urlsplit(response['image']['url'])
        img_url = r._replace(query=None).geturl()
        content = None
        if img_url:
            with urlopen(img_url) as f:
                content = ContentFile(f.read())

        if content:
            img_name = user.username + '.jpg'
            user.profile.avatar.save(img_name, content, save=True)
