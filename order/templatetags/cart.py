#this is custom filter that can be used to using this function
#every session has its own key that is randomly generated 
from django import template

register=template.Library()

@register.filter(name='cart_quantity')
def cart_quantity(product,cart):
    keys=cart.keys()
    for id in keys:
        if int(id)==product.id:
            return cart.get(id)
    return 0;


@register.filter(name='price_total')
def price_total(product,cart):
    return product.price * cart_quantity(product,cart) 

@register.filter(name='total_cart_price')
def total_cart_price(products,cart):
    sum=0;
    for p in products:#one bye one products are come to this p
        sum +=price_total(p,cart)#one product from p and quantity from the cart are come to price_total
                                 #function and go to price_total function above and perform tasks and return it
                                 # again to the sum variable and finally do the some of all products         

    return sum    
