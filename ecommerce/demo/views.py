from django.shortcuts import render
from ecommerce.inventory import models


def home(request):
    return render(request, "index.html")


def category(request):
    data = models.Category.objects.all()

    return render(request, "categories.html", {"data": data})


def product_by_category(request, category):
    data = models.Product.objects.filter(category__name=category).values(
        "id", "name", "slug", "product__store_price",
    )
    # print(data)
    return render(request, "product_by_category.html", {"data": data})


def product_detail(request, slug):
    filter_arguments = []
    from django.db.models import Count
    if request.GET:
        for value in request.GET.values():
            filter_arguments.append(value)
        data = models.ProductInventory.objects.filter(product__slug=slug). \
            filter(attribute_values__attribute_value__in=filter_arguments).annotate(
            num_tags=Count('attribute_values')).filter(num_tags=len(filter_arguments)).values(
            "id", "sku", "product__name", "store_price", "product_inventory__units")
    else:
        data = models.ProductInventory.objects.filter(product__slug=slug). \
            filter(is_default=True).values(
            "id", "sku", "product__name", "store_price", "product_inventory__units")
    print(data)
    y = models.ProductInventory.objects.filter(product__slug=slug).distinct().values(
        "attribute_values__product_attribute__name", "attribute_values__attribute_value")
    z = models.ProductTypeAttributes.objects.filter(product_type__product_type__product__slug=slug).values(
        "product_attribute__name").distinct()
    print(z)

    return render(request, "product_detail.html", {"data": data, "y": y, "z": z})
