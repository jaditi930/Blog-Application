from django import template
register = template.Library()
@register.filter(name='slice')
def split1(value,l):
  return str(value)[int(l)]