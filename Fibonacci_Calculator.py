import decimal
import sys
sys.get_int_max_str_digits()
sys.set_int_max_str_digits(100000000)
usr_input=int(input('Please enter the nth number of the fibonacci sequence: '))
def formulaFibWithDecimal(n):
    decimal.getcontext().prec = 300000

    root_5= decimal.Decimal(5).sqrt()
    phi=((1+root_5)/2)

    a=((phi**n)-((-phi)**-n))/root_5

    return round(a)
print(int(formulaFibWithDecimal(usr_input)))
input()
