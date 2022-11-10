from django import template
register = template.Library()
@register.filter(name="slice")
def split1(value,l):
  print(str(value))
  print(str(value)[int(l)])
  return str(str(value)[int(l)])