from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin


class PageView(SingleObjectMixin, View):
    def get_object(self, queryset=None):
        return self.request.page

    def get(self, request):
        self.object = self.get_object()
        context = self.get_context_data()
        return HttpResponse(request.page.content.render(context))

page_view = PageView.as_view()
