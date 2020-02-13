import django.template
from django.shortcuts import reverse
from ..models import Menu, Item


register = django.template.Library()


def get_url_by_named(url):
    """Простейшее определение named url."""
    try:
        if '/' in url:  # предположим, что в named url не бывает '/'
            return url
        else:
            return reverse(url)
    except Exception:
        return url


@register.inclusion_tag('draw_menu/menu_template.html', takes_context=True)
def draw_menu(context, menu_name):
    """Определяет template tag, выводящий все пункты меню 'menu_name' в древовидной форме."""
    items = Menu.objects.get(name=menu_name).item_set.all().order_by('path')
    current_uri = context["request"].get_full_path()

    result_list = []
    prev_item_level = 1
    _break_level = None

    for current_item in items:

        current_item_url = get_url_by_named(current_item.href)

        # первый уровень вложения выводим, остальное мимо
        if _break_level is not None:
            if _break_level < current_item.level:
                continue
            elif _break_level > current_item.level:
                break

        # составляем список пригодный для фильтра unordered_list
        item_value = f'<a href="{current_item_url}">{current_item.title}</a>'

        if prev_item_level < current_item.level:
            for step in range(current_item.level - prev_item_level):
                item_value = [item_value]
            tmp_list = result_list
            for level in range(prev_item_level):
                tmp_list = tmp_list[-1]
        else:
            tmp_list = result_list
            for level in range(current_item.level):
                tmp_list = tmp_list[-1]
        tmp_list.append(item_value)
        prev_item_level = current_item.level

        # устанавливаем уровень остановки, после активного пункта
        if current_item_url == current_uri:
            _break_level = current_item.level + 1

    return {'menu': result_list}
