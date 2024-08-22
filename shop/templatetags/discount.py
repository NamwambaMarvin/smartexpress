from django import template
import random

register = template.Library()

@register.simple_tag
def percentage_discount( price, discount ):
    '''
    Takes in price and discount
    returns percentage discount
    '''
    try:
        price = int( price )
        discount = int( discount )
        if price:
            f = discount / price
            return round(f*100, 1)
    except: pass
    return 0

@register.simple_tag
def vat(price, discount):
    try:
        original_price = int(price) + int(discount)
        return round(0.18*original_price, 1)
    except: pass
    return "Error!"

@register.simple_tag
def price_minus_vat(price, discount):
    try:
        p = price+discount
        m = p-0.18*p
        return round(m, 1)
    except: pass
    return "Error"

@register.simple_tag
def rating():
    return random.randint(250,1000)