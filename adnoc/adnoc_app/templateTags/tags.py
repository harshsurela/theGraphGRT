# import template
from django import template
import datetime


register = template.Library()

@register.filter(name='totalDaysTillToday')
def totalDaysTillToday(value):
    if isinstance(value, datetime.datetime):
        value = value.date()
    finalAns=(datetime.date.today()-value).days
    print(finalAns)
    if finalAns<=0:
        finalAns=1
    return finalAns