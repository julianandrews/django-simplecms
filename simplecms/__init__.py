from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_simplecms_content_model():
    """
    Returns the Content model that is active in this project.
    """
    try:
        content_model = getattr(
            settings, 'SIMPLECMS_CONTENT_MODEL', 'simplecms.CMSContent'
        )
        return apps.get_model(content_model)
    except ValueError:
        raise ImproperlyConfigured(
            "SIMPLECMS_CONTENT_MODEL must be of the form "
            "'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "SIMPLECMS_CONTENT_MODEL refers to model '%s' that has not been "
            "installed" % settings.SIMPLECMS_CONTENT_MODEL
        )
