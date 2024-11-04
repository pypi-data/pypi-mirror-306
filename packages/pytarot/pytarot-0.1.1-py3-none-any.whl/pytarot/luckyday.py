import random

def get_lucky_day():

    months = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
        5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
        9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }

    month_num = random.randint(1, 12)
    month = months[month_num]

    if month_num in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    elif month_num in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    else:  
        day = random.randint(1, 28)

    output = f"Your lucky day is: {month}/{day}"
    return output
