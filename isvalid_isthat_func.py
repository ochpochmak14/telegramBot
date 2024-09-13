import datetime

current_year = datetime.datetime.now().year

def is_validate_string(word: str) -> bool:
    s = "1234567890{[}]'?$^=<>,:.;!_*+()/#%&"
    for char in s:
        if char in word:
            return False
        
    return True


def is_validate_date(date: str) -> bool:
    try:
        year = date[:4]
        if abs(int(current_year) - int(year)) > 100:
            return False
    except Exception:
        return False
    
    return True
    


    