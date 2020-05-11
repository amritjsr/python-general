'''
This Program is to findout Firday The 13th
'''
import calendar
import sys
from colorama import Fore, Style
#### Veriable Declaration Start
myCalendar = calendar.TextCalendar(calendar.SUNDAY)
myCalendarObj = calendar.Calendar(firstweekday=6)
found = False
weekdays = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
#### Veriable Declaration End
def month_has_13(monthDatesObj):
    found = False
    for i_date in monthDatesObj:
        if i_date.day == 13 and i_date.weekday() == 4:
            found = True
            break
    return found


def printMonth(monthInText,found = False):

    if found == True:
        length = len(monthInText);
        ctr = 0
        while ctr < length:
            if monthInText[ctr] == '1' and monthInText[ctr + 1] == '3':
                print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}13{Style.RESET_ALL}{Fore.RESET}", end='')
                ctr += 2
                continue
            print(monthInText[ctr], end='')
            ctr += 1

    if found == False:
        print(monthInText)
menu_message = """
  Please Enter Your Choice.
  ----------------------------
    1. Find out if any month has Friday-13th ( Input -> Year,Month)
    2. Find out if any year has Friday-13th ( Input -> Year)
    3. Find out given date is Friday-13th ( Input -> dd-mm-yyyy )
"""
print(menu_message)
try:
    choice = int(input("Waiting For your Choice ..... "))
except ValueError as e:
    print(f"{Fore.LIGHTRED_EX}WRONG Input!!!!!!{Fore.RESET}\nPlease Enter the choice in INTEGER-(1/2/3) .... Rerun the program .... Bye Bye")
if choice == 1:
    year = int(input("Enter Year : "))
    month = int(input("Enter Month : "))
    monthdatesObj = myCalendarObj.itermonthdates(year, month)
    found = month_has_13(monthdatesObj)
    monthInText = myCalendar.formatmonth(theyear=year, themonth=month)
    if found == True:
        print("Yes, You  Find It!!!!!!!!!! ............ lucky!!!!!!")
        printMonth(monthInText, found)
    elif found == False:
        print("Given Month isn't so Unlucky!!!!!!")
        printMonth(monthInText, found)

elif choice == 2:
    year = int(input("Enter Year : "))
    found = False
    for month in range(1,13):
        monthdatesObj = myCalendarObj.itermonthdates(year, month)
        found = month_has_13(monthdatesObj)
        if found == True:
            monthInText = myCalendar.formatmonth(theyear=year, themonth=month)
            printMonth(monthInText, found)
elif choice == 3:
    date = input("Enter your Date as ( dd-mm-yyyy ) : ")
    dateList = str(date).split('-')
    try:
        day = int(dateList[0])
        month = int(dateList[1])
        year = int(dateList[2])
    except ValueError:
        print("Wrong Date Input !!!!!!! Try Again as dd-mm-yyyy ..... ")
    if day == 13:
        monthDatesObj = myCalendarObj.itermonthdates(year, month)
        found = month_has_13(monthDatesObj)
        if found == True :
            print("Yes, Ur date is Friday the 13th")
            monthInText = myCalendar.formatmonth(theyear=year, themonth=month)
            printMonth(monthInText, found)
        else:
            print("Nop, It's not Friday the 13th .....")
    else:
        print("Are looking for any Friday the 13th, then give us some date of 13th ..... Bye...")
else:
    print(f"{Fore.LIGHTRED_EX}WRONG Input!!!!!!{Fore.RESET}\nPlease Enter the choice in INTEGER-(1/2/3) .... Rerun the program .... Bye Bye")