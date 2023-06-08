from django import template

register = template.Library()

@register.filter(name='duration_format')
def duration_format(duration):
    minutes = int(duration / 1000 // 60)
    seconds = int(duration / 1000 % 60)
    return f"{minutes}:{seconds:02d}"