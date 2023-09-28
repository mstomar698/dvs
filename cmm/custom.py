from django import template
register = template.Library()


@register.filter
def convertint(str_w):
    return int(str_w)


@register.filter
def convertstr(str_w):
    return str(str_w)



@register.filter
def index(num, i):
    index_number = i-1
    return num[index_number]



@register.filter
def floatconvert(num):
    return float(num)
    




@register.filter
def length(lis):
    return len(lis)

@register.filter(name='dict_key')
def dict_item(dictionary, i):
    a = dictionary[i]
    return a


@register.filter
def to_or(value):
    return value.replace("/"," or ")

@register.filter
def get_2d_0(value):
    return int(value[0])

@register.filter
def get_2d_1(value):
    return value[1]





@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 