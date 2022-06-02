from django import template
import math
register = template.Library()

@register.filter(name='btos')
def bytesToSize(bytes):
    if bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB")
    i = int(math.floor(math.log(bytes, 1024)))
    p = math.pow(1024, i)
    s = round(bytes / p, 2)
    return "%s %s" % (s, size_name[i])


@register.filter(name='stoi')
def stoi(value):
    print(value)
    return int(value)

@register.filter(name='twelve_hour')
def twelve_hour_format(datetime):
    meridiem_abv = ('AM', 'PM')
    hour = datetime.hour
    minute = datetime.minute
    
    if minute == 60:
        hour+= 1
        minute = 0
    
    if hour < 12:
        meridiem = meridiem_abv[0]
    else:
        hour = hour - 12
        meridiem = meridiem_abv[1]
        
    return "%r:%r %s" %(hour, minute, meridiem)

@register.filter(name='date_format')
def date_format(datetime):
    return datetime.date().isoformat()
    