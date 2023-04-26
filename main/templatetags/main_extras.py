from django import template

register = template.Library()

@register.filter(name='split')
@template.defaultfilters.stringfilter
def split(value, arg):
    return value.split(arg)[:-1]