from django import template
from django.db.models import Sum

register = template.Library()

@register.filter(name='duration_format')
def duration_format(duration):
    minutes = int(duration / 1000 // 60)
    seconds = int(duration / 1000 % 60)
    return f"{minutes}:{seconds:02d}"

@register.filter(name='aggregate_duration')
def aggregate_duration_filter(queryset):
    total_duration = queryset.aggregate(total_duration=Sum('duration'))['total_duration']
    return total_duration if total_duration else 0

