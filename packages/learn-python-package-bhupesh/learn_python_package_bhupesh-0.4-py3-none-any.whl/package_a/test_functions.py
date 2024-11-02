import greet_function
import age_calculator
import tax_calculator
from greet_function import greet
from age_calculator import age_calculator
from tax_calculator import tax_calculator

greet('Bhupesh')
Age=int(input('what is your age : '))
age_calculator(Age)

product_value = float(input('value of the product : '))
tax_calculator(product_value)