from datetime import date

def days_until(target: date) -> int:
    return (target - date.today()).days
