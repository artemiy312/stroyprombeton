from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from stroyprombeton import views

catalog_urls = [
    url(r'^$', views.CategoryTree.as_view(), name='category_tree'),
    url(r'^categories/(?P<category_id>[0-9]+)/$', views.CategoryPage.as_view(), name='category'),
    url(r'^products/(?P<product_id>[0-9]+)/$', views.ProductPage.as_view(), name='product'),
]

ecommerce_urls = [
    url(r'^cart-add/$', views.AddToCart.as_view(), name='cart_add'),
    url(r'^cart-change/$', views.ChangeCount.as_view(), name='cart_set_count'),
    url(r'^cart-flush/$', views.FlushCart.as_view(), name='cart_flush'),
    url(r'^cart-remove/$', views.RemoveFromCart.as_view(), name='cart_remove'),
    url(r'^order/$', views.OrderPage.as_view(), name='order_page'),
]

search_urls = [
    url(r'^$', views.Search.as_view(), name='search'),
    url(r'^autocomplete/$', views.Autocomplete.as_view(), name='autocomplete'),
]

urlpatterns = [
    url(r'^$', views.IndexPage.as_view(), name='index'),
    url(r'^drawing-success/', views.OrderDrawingSuccess.as_view(), name='order_drawing_success'),
    url(r'^gbi/', include(catalog_urls)),
    url(r'^fetch-products/$', views.fetch_products, name='fetch_products'),
    url(r'^order-drawing/', views.OrderDrawing.as_view(), name='order_drawing'),
    url(r'^order-price/', views.OrderPrice.as_view(), name='order_price'),
    url(r'^page/', include('pages.urls')),
    url(r'^price-success/', views.OrderPriceSuccess.as_view(), name='order_price_success'),
    url(r'^regions/^([\w-]+)/$', views.RegionFlatPage.as_view(), name='region_flat_page'),
    url(r'^search/', include(search_urls)),
    url(r'^shop/', include(ecommerce_urls)),
    url(r'^shop/', include('ecommerce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
