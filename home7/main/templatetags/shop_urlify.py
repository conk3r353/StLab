from django import template

register = template.Library()


@register.filter(name='shop_urlify')
def shop_urlify(shop):
    return f'/shop/{shop.id}'
