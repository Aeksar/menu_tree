from django import template
from django.urls import resolve, Resolver404
from ..models import MenuItem

register = template.Library()

@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    try:
        current_url = context['request'].path
        resolved = resolve(current_url)
    except (KeyError, Resolver404):
        current_url = ''
        resolved = None

    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent').order_by('position')
    
    def build_tree(items, parent=None):
        tree = []
        for item in items:
            if item.parent_id == (parent.id if parent else None):
                children = build_tree(items, item)
                node = {
                    'item': item,
                    'children': children,
                    'is_active': item.get_url() == current_url or item.named_url == getattr(resolved, 'url_name', '')
                }
                tree.append(node)
        return tree

    menu_tree = build_tree(menu_items)
    
    def mark_active_path(tree):
        for node in tree:
            node['show_children'] = False
            if node['is_active']:
                node['show_children'] = True
                return True
            if mark_active_path(node['children']):
                node['show_children'] = True
                return True

    mark_active_path(menu_tree)
    from pprint import pprint
    pprint(menu_tree)
    return {'menu_tree': menu_tree}