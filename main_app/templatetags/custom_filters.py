from django import template
from django.db.models import Sum

register = template.Library()

@register.filter(name='duration_format')
def duration_format(duration):
    seconds = int(duration / 1000) % 60
    minutes = int(duration / 1000 // 60) % 60
    hours = int(duration / 1000 // 3600)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

@register.filter(name='aggregate_duration')
def aggregate_duration_filter(queryset):
    total_duration = queryset.aggregate(total_duration=Sum('duration'))['total_duration']
    return total_duration if total_duration else 0

