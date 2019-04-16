from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import ManyToManyField

from generic_admin import models as admin_models, mixins, filters as rf_filters

from stroyprombeton import models as stb_models
from stroyprombeton.admin import filters, inlines
from stroyprombeton.forms import AdminWidgetsForm


class CustomPageAdmin(admin_models.CustomPageAdmin):

    form = AdminWidgetsForm
    inlines = [inlines.ImageInline]


class FlatPageAdmin(admin_models.FlatPageAdmin):

    form = AdminWidgetsForm
    inlines = [inlines.ImageInline]
    list_filter = [
        'is_active',
        rf_filters.HasContent,
        rf_filters.HasImages,
        filters.ParentFilter,
    ]


class ProductPageAdmin(admin_models.ProductPageAdmin):

    form = AdminWidgetsForm
    category_page_model = stb_models.CategoryPage
    inlines = [inlines.ProductInline, inlines.ImageInline]
    list_filter = [
        'is_active',
        rf_filters.HasContent,
        rf_filters.HasImages,
    ]
    list_display = ['model_id', 'name', 'custom_parent', 'links', 'is_active']

    def get_queryset(self, request):
        qs = super(admin_models.ProductPageAdmin, self).get_queryset(request)
        return self.add_reference_to_field_on_related_model(qs, _product_id='id')


class CategoryPageAdmin(admin_models.CategoryPageAdmin):

    form = AdminWidgetsForm
    inlines = [inlines.CategoryInline, inlines.ImageInline]
    list_filter = [
        'is_active',
        rf_filters.HasContent,
        rf_filters.HasImages,
        filters.SpecificationFilter,
    ]


class OrderAdmin(mixins.PermissionsControl):

    add = True
    inlines = [inlines.PositionInline]
    list_display = ['email', 'phone', 'name', 'company', 'address', 'city', 'paid']
    search_fields = ['email', 'phone', 'name', 'company']
    list_display_links = ['email']


class OptionAdmin(mixins.PermissionsControl):

    add = True
    list_filter = [
        # @todo #433:30m Determine relevance of CharacteristicsEqualityFilter.
        #  Either drop in case of obsoleteness or integrate with new Option model.
        rf_filters.PriceRange,
        # CharacteristicsEqualityFilter,
    ]
    list_display = ['name', 'id', 'code', 'mark', 'price', 'in_stock', 'is_popular']

    formfield_overrides = {
        ManyToManyField: {
            'widget': FilteredSelectMultiple(verbose_name='Tags', is_stacked=False)
        },
    }