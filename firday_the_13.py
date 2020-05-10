'''
This Program is to findout Firday The 13th
'''
import calendar
import sys
from colorama import Fore
#### Veriable Declaration Start
myCalendar = calendar.TextCalendar(calendar.SUNDAY)
myCalendarObj = calendar.Calendar(firstweekday=6)
weekdays = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
#### Veriable Declaration End
# for I in myCalendarObj.itermonthdates(2020,5):
#
#     print(type(I), I.day, I.year, I.today(),I.isoweekday(), type(I.weekday()))
# print(myCalendar.formatmonth(2020, 5))
# sys.exit()

# print(myCalendar.formatmonth(1999, 5)) #### PRINTING CALENDAR MAY-1999
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
    found = False
    for i_date in monthdatesObj:
        if i_date.month != month:
            continue
        if i_date.day == 13 and i_date.weekday() == 4:
            print("Yes!!!!! You got the Friday The 13th .....")
            output = myCalendar.formatmonth(theyear=year, themonth=month)
            length = len(output); ctr = 0
            while ctr < length:
                if output[ctr] == '1' and output[ctr+1] == '3':
                    print(f"{Fore.LIGHTRED_EX}13{Fore.RESET}",end='')
                    ctr += 2
                    continue
                print(output[ctr], end='')
                ctr += 1
            found = True
            break
    if found == False:
        print("Given Month isn't so Unlucky!!!!!!")
elif choice == 2:
    year = int(input("Enter Year : "))
    print(myCalendar.formatyear(year))
elif choice == 3:
    date = input("Enter your Date as ( dd-mm-yyyy ) : ")
    print(date)
else:
    print(f"{Fore.LIGHTRED_EX}WRONG Input!!!!!!{Fore.RESET}\nPlease Enter the choice in INTEGER-(1/2/3) .... Rerun the program .... Bye Bye")