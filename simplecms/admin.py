from django.conf.urls import url
from django.contrib import admin
from django.http import JsonResponse

import json

from .models import CMSContent, CMSPage, CMSSite, PageTreeParseError


@admin.register(CMSContent)
class CMSContentAdmin(admin.ModelAdmin):
    pass


@admin.register(CMSSite)
class CMSSiteAdmin(admin.ModelAdmin):
    fields = ('site', )

    class Media:
        css = {
            'all': ('admin/css/jqtree.css', 'admin/css/jquery.modal.min.css')
        }
        js = (
            'admin/js/csrf.js',
            'admin/js/pagetree.js',
            'admin/js/tree.jquery.js',
            'admin/js/jquery.modal.min.js',
        )

    def has_tree_edit_perm(self, request):
        page_opts = CMSPage._meta
        return all(request.user.has_perm(
            '%s.%s_%s' % (page_opts.app_label, kind, page_opts.model_name)
        ) for kind in ['change', 'add', 'delete'])

    def pagetree_view(self, request, pk):
        def JsonError(status):
            return JsonResponse(data={"error": status}, status=status)

        if not request.user.is_authenticated():
            return JsonError(401)
        if not self.has_module_permission(request):
            return JsonError(403)
        try:
            cmssite = CMSSite.objects.prefetch_related('pages').get(pk=pk)
        except CMSSite.DoesNotExist:
            return JsonError(404)

        if request.method == 'POST':
            if not self.has_tree_edit_perm(request):
                return JsonError(403)
            try:
                tree_data = json.loads(request.POST.get('tree'))
            except json.JSONDecodeError:
                return JsonError(400)
            try:
                cmssite.update_pagetree(tree_data)
            except PageTreeParseError:
                return JsonError(400)
            # TODO: catch bulk_load errors and return a 409 error with
            # appropriate info.

        # TODO: Sanitize this data
        data = cmssite.get_pagetree_data()
        return JsonResponse(data, safe=False)

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        return [
            url(
                r'^(.+)/pagetree/$',
                self.pagetree_view,
                name='%s_%s_pagetree' % info,
            ),
        ] + super().get_urls()
