from django import template
from django.db.models import Sum

register = template.Library()

@register.filter
def sum_votes(solutions):
    return solutions.aggregate(total_votes=Sum('vote_set__value'))['total_votes']
