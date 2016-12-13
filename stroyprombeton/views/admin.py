from django.db.models import ObjectDoesNotExist

from generic_admin import views as admin_views

from stroyprombeton.models import Product, Category


def category_name_strategy(product, related_model_entity, related_model_value):
    try:
        new_category = type(related_model_entity).objects.get(name=related_model_value)
    except ObjectDoesNotExist:
        raise ValueError('Category with name={} does not exist.'.format(related_model_value))
    product.category = new_category


class GenericTableEditor:
    model = Product
    relation_field_names = ['category', 'page']

    excluded_related_model_fields = {
        'page': [
            'content', 'related_model_name', 'date_published', 'stroyprombeton_category',
            'stroyprombeton_product', 'parent', 'children', 'images', 'type', 'id', 'slug',
            'name'
        ],
    }

    included_related_model_fields = {
        'category': [
            'name'
        ],
    }

    excluded_model_fields = [
        'category', 'page', 'property', 'property_id', 'page_id', 'category_id', 'id'
    ]

    field_controller = admin_views.TableEditorFieldsControlMixin(
        Product,
        relation_field_names=relation_field_names,
        excluded_model_fields=excluded_model_fields,
        included_related_model_fields=included_related_model_fields,
        excluded_related_model_fields=excluded_related_model_fields
    )


class TableEditorAPI(GenericTableEditor, admin_views.TableEditorAPI):
    pattern_to_update_related_model = {
        'category': {
            'name': category_name_strategy
        }
    }


class TableEditor(GenericTableEditor, admin_views.TableEditor):
    pass


class Tree(admin_views.Tree):
    model = Category


class RedirectToProduct(admin_views.RedirectToProductPage):
    model = Product
    admin_page_product_urlconf = 'admin:stroyprombeton_productpage_change'
    site_page_product_urlconf = 'product'
