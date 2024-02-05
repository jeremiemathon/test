# context_processors.py

from .models import SiteSettings

def global_settings(request):
    settings = SiteSettings.objects.first()
    print(settings)
    return {'global_settings': settings}
