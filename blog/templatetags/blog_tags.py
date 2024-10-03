from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


farsi_nums = {
    '0': '۰',
    '1': '۱',
    '2': '۲',
    '3': '۳',
    '4': '۴',
    '5': '۵',
    '6': '۶',
    '7': '۷',
    '8': '۸',
    '9': '۹'
}


@register.filter
def nospace(value):
    return mark_safe(value.replace(" ", '&#8204;'))


@register.filter
def farsi_num(value):
    str_num = str(value)
    for num in str_num:
        if farsi_nums.get(num):
            str_num = str_num.replace(num, farsi_nums[num])
    return str_num


@register.filter
def generate_id(id):
    new_id = (id * 10) - (id * 3)
    print(new_id)
    return new_id
