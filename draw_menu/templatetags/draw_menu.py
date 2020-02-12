import django.template


register = django.template.Library()


@register.inclusion_tag('draw_menu/menu_template.html')
def draw_menu(menu_name):
    return {'menu_name': menu_name}
