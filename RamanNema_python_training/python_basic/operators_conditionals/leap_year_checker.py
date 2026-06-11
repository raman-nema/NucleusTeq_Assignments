# Program to check whether a year is a leap year.

def check_leap_year(year):
    # Checking leap year condition
    if year % 4 == 0 and year % 100 != 0:
        print("Leap Year")
    elif year % 400 == 0:
        print("Leap Year")
    else:
        print("Not a Leap Year")


year = int(input("Enter a year: "))
check_leap_year(year)