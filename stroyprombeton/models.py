from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from catalog.models import AbstractProduct, AbstractCategory
from ecommerce.models import Order as ecOrder
from mptt import models as mptt_models
from pages import models as page_models


class Order(ecOrder):
    company = models.CharField(max_length=255, verbose_name='company')
    address = models.TextField(default='', blank=True, verbose_name='address')
    comment = models.TextField(default='', blank=True, verbose_name='comment')


class Category(AbstractCategory, page_models.PageMixin):
    specification = models.TextField(
        default='',
        blank=True,
        verbose_name=_('specification'),
    )

    @classmethod
    def get_default_parent(cls):
        return page_models.CustomPage.objects.filter(slug='gbi').first()

    def get_absolute_url(self):
        """Return url for model."""
        return reverse('category', args=(self.id,))


class Product(AbstractProduct, page_models.PageMixin):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('category'),
    )
    is_new_price = models.NullBooleanField(
        blank=True,
        null=True,
        verbose_name=_('is new price'),
    )
    date_price_updated = models.DateField(auto_now_add=True, verbose_name=_('date price updated'))
    code = models.BigIntegerField(null=True, blank=True, verbose_name=_('code'))
    mark = models.CharField(default='', max_length=500, blank=True, verbose_name=_('mark'))
    specification = models.TextField(default='', blank=True, verbose_name=_('specification'),)
    length = models.IntegerField(null=True, blank=True, verbose_name=_('length'))
    width = models.IntegerField(null=True, blank=True, verbose_name=_('width'))
    height = models.IntegerField(null=True, blank=True, verbose_name=_('height'))
    weight = models.FloatField(null=True, blank=True, verbose_name=_('weight'))
    volume = models.FloatField(null=True, blank=True, verbose_name=_('volume'))
    diameter_out = models.IntegerField(null=True, blank=True, verbose_name=_('diameter out'))
    diameter_in = models.IntegerField(null=True, blank=True, verbose_name=_('diameter in'))

    def get_absolute_url(self):
        return reverse('product', args=(self.id,))

    def get_admin_tree_title(self):
        return '[{id}] {name} {mark}'.format(id=self.id, mark=self.mark, name=self.name)


class CategoryPage(page_models.ModelPage):
    """Proxy model for Admin."""

    class Meta(page_models.ModelPage.Meta):
        proxy = True
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    objects = page_models.ModelPage.create_model_page_managers(Category)


class ProductPage(page_models.ModelPage):
    """Proxy model for Admin."""

    class Meta(page_models.ModelPage.Meta):
        proxy = True
        verbose_name = _('product')
        verbose_name_plural = _('products')

    objects = page_models.ModelPage.create_model_page_managers(Product)


def get_manager(parent_slug):
    class FlatPageTypeManager(mptt_models.TreeManager):
        def get_queryset(self):
            return (
                super(FlatPageTypeManager, self)
                .get_queryset()
                .filter(parent__slug=parent_slug)
            )

    return FlatPageTypeManager()


class NewsForAdmin(page_models.Page):
    class Meta:
        proxy = True
        verbose_name = _('News')
        verbose_name_plural = _('News')

    objects = get_manager('news')


class RegionsForAdmin(page_models.Page):
    class Meta:
        proxy = True
        verbose_name = _('Regions')
        verbose_name_plural = _('Regions')

    objects = get_manager('regions')


class ClientFeedbacksForAdmin(page_models.Page):
    class Meta:
        proxy = True
        verbose_name = _('Client feedbacks')
        verbose_name_plural = _('Client feedbacks')

    objects = get_manager('client-feedbacks')
