from django.urls import resolve, Resolver404
from .models import CMSPage
from .views import page_view


def page_middleware(get_response):
    """
    Attach a page to the request if one matches the requested path. In case of
    a 404, render a view of the page.
    """
    def middleware(request):
        # If multiple pages match a given slug, just take the first.
        # Maybe we should log some sort of warning in this case?
        request.page = CMSPage.objects.for_slug(request.path_info).first()
        try:
            resolve(request.path_info)
        except Resolver404:
            if request.page and request.page.content:
                return page_view(request)

        return get_response(request)

    return middleware
