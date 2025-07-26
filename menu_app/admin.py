from django.contrib import admin
from .models import MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'menu_name', 'url', 'named_url', 'parent', 'position']
    list_filter = ['menu_name']
    list_editable = ['position']
    search_fields = ['name', 'menu_name']

admin.site.register(MenuItem, MenuItemAdmin)

# menu_app/templatetags/menu_tags.py
from django import template
from django.urls import resolve, Resolver404
from .models import MenuItem

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
                tree.append({
                    'item': item,
                    'children': children,
                    'is_active': item.get_url() == current_url or item.named_url == getattr(resolved, 'url_name', '')
                })
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
        return False

    mark_active_path(menu_tree)
    return {'menu_tree': menu_tree}