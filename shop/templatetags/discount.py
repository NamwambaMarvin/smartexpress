from django import template

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
            return round(f*100, 2)
    except: pass
    return '0.0'