# This is an tax calcualor i(Bhupesh) have created .
# It can be used as an executable file using 'python tax_calculator.oy'

def tax_calculator(product_value):
    print('tax calculator is here : ')

    #product_value = float(input('value of the product '))
    tax_amount=product_value * 0.1
    total_amount= product_value+tax_amount
    print('your total amount including tax is :', total_amount)
