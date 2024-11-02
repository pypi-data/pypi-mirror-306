# input is the age of the user, output the age in decades and years
# for example : for Age= 202 , it is 20 decades and 2 years old

def age_calculator(Age) :
   #Age=int(input('what is your age : '))
   decade= int(Age/10)
   years= Age%10

   print('your age is :',decade,'decades and',years,'years')

