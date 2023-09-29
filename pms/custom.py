from django import template
register = template.Library()


@register.filter
def convertint(str_w):
    try:
        a = int(str_w)
    except Exception as e:
        a = 0
    return a

    # return int(str_w)



@register.filter
def index(num, i):
    index_number = i-1
    return num[index_number]



@register.filter
def floatconvert(num):
    try:
        a = float(num)
    except Exception as e:
        a = 0.0
    return a    
#     return float(num)
    
    
@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 



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

