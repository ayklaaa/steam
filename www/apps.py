from django.apps import AppConfig
from django.template import engines
from django.template.library import Library

def patch_jazzmin_length_is():
    django_engine = engines['django']
    lib = django_engine.engine.template_libraries.get('django.templatetags.future', Library())
    
    @lib.filter
    def length_is(value, arg):
        return len(value) == int(arg)
    
    django_engine.engine.template_libraries['django.templatetags.future'] = lib

class YourAppConfig(AppConfig):
    def ready(self):
        patch_jazzmin_length_is()

class WwwConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'www'
