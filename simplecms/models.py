import re

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.validators import RegexValidator
from django.db import models, transaction

from treebeard.mp_tree import MP_Node, MP_NodeManager

SLUG_RE = re.compile(r'^[-a-zA-z0-9_]*$')
FULL_SLUG_RE = re.compile(r'^[-a-zA-z0-9_/]*$')


class PageTreeParseError(Exception):
    pass


class CMSSite(models.Model):
    site = models.OneToOneField(Site, models.CASCADE)

    class Meta:
        verbose_name = "CMS Site"

    def update_pagetree(self, data):
        # TODO: Optimistic locking
        pks = []
        content_ids = {
            page.id: page.content_id for page in CMSPage.objects.filter(cmssite=self)
        }

        def parse_json_data(data, partial_slug=''):
            parsed_data = []
            for d in data:
                if d.get('id') is None:
                    page = CMSPage.add_root(slug=d['name'], cmssite=self)
                    page.save()
                    pk = page.pk
                else:
                    pk = d['id']
                slug = d.get('name')
                slug = '' if slug == '</>' else slug
                if slug is None or not SLUG_RE.match(slug):
                    raise PageTreeParseError()
                if partial_slug:
                    slug = '/'.join((partial_slug, slug))
                data = {'slug': slug, 'cmssite': self.pk}
                content_id = content_ids.get(pk)
                if content_id is not None:
                    data['content'] = content_ids.get(pk)
                parsed_data.append({
                    'id': pk,
                    'data': data,
                    'children': parse_json_data(d.get('children', []), slug),
                })
                pks.append(pk)
            return parsed_data

        with transaction.atomic():
            cleaned_data = parse_json_data(data)
            CMSPage.objects.filter(cmssite=self).exclude(pk__in=pks).delete()
            CMSPage.load_bulk(cleaned_data, keep_ids=True)

    def get_pagetree_data(self):
        def parse_tree_data(data):
            return [{
                'id': d['id'],
                'name': d['data']['slug'].split('/')[-1] or '</>',
                'children': parse_tree_data(d.get('children', []))
            } for d in data if d['data']['cmssite'] == 1]

        return parse_tree_data(CMSPage.dump_bulk())

    def __str__(self):
        return "CMS site for {}".format(self.site)


class AbstractCMSContent(models.Model):
    class Meta:
        abstract = True


class CMSContent(AbstractCMSContent):
    content = models.TextField()

    def render(self, context):
        return self.content

    class Meta(AbstractCMSContent.Meta):
        swappable = 'SIMPLECMS_CONTENT_MODEL'
        verbose_name = 'CMS Content'
        verbose_name_plural = 'CMS Content'


class PageManager(MP_NodeManager):
    def for_slug(self, slug):
        normalized = slug.strip('/')
        return self.filter(slug=normalized)


class CMSPage(MP_Node):
    cmssite = models.ForeignKey(CMSSite, related_name='pages', verbose_name='CMS Site')
    slug = models.CharField(max_length=255, validators=[RegexValidator(FULL_SLUG_RE)], blank=True)
    content = models.ForeignKey(
        settings.SIMPLECMS_CONTENT_MODEL, models.SET_NULL, null=True,
        blank=True, related_name='pages',
    )

    objects = PageManager()

    def get_absolute_url(self):
        return '/{}/'.format(self.slug)

    class Meta:
        verbose_name = 'CMS Page'

    def __str__(self):
        return "Page for '{}'".format(self.slug)
