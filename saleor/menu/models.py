from django.db import models
from django.db.models import Max
from django.utils.translation import pgettext_lazy
from mptt.managers import TreeManager
from mptt.models import MPTTModel

from ..page.models import Page
from ..product.models import Category, Collection


class Menu(models.Model):
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        permissions = (
            ('view_menu',
             pgettext_lazy('Permission description', 'Can view menus')),
            ('edit_menu',
             pgettext_lazy('Permission description', 'Can edit menus')))

    def __str__(self):
        return self.slug


class MenuItem(MPTTModel):
    menu = models.ForeignKey(
        Menu, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    sort_order = models.PositiveIntegerField(editable=False)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.CASCADE)

    # not mandatory fields, usage depends on what type of link is stored
    url = models.URLField(max_length=256, blank=True, null=True)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.CASCADE)
    collection = models.ForeignKey(
        Collection, blank=True, null=True, on_delete=models.CASCADE)
    page = models.ForeignKey(
        Page, blank=True, null=True, on_delete=models.CASCADE)

    objects = models.Manager()
    tree = TreeManager()

    class Meta:
        ordering = ('sort_order',)
        app_label = 'menu'

    def __str__(self):
        return self.name

    def get_ordering_queryset(self):
        return (
            self.menu.items.all() if not self.parent
            else self.parent.children.all())

    def save(self, *args, **kwargs):
        if self.sort_order is None:
            qs = self.get_ordering_queryset()
            existing_max = qs.aggregate(Max('sort_order'))
            existing_max = existing_max.get('sort_order__max')
            self.sort_order = 0 if existing_max is None else existing_max + 1
        super().save(*args, **kwargs)

    @property
    def linked_object(self):
        return self.category or self.collection or self.page

    @property
    def destination_display(self):
        linked_object = self.linked_object

        if not linked_object:
            prefix = pgettext_lazy('Link object type description', 'URL: ')
            return prefix + self.url

        if isinstance(linked_object, Collection):
            prefix = pgettext_lazy(
                'Link object type description', 'Collection: ')
        elif isinstance(linked_object, Category):
            prefix = pgettext_lazy(
                'Link object type description', 'Category: ')
        else:
            prefix = pgettext_lazy(
                'Link object type description', 'Page: ')

        return prefix + str(linked_object)

    def get_url(self):
        linked_object = self.linked_object
        return linked_object.get_absolute_url() if linked_object else self.url
