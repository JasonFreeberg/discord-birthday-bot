
import datetime 


def create_message(name: str, birthdate: datetime.datetime):
    formatted_birthday = birthdate.strftime('%B %d')
    new_age = int((datetime.datetime.today() - birthdate).days / 365)

    return f'{name} is turning {new_age} in two weeks on {formatted_birthday}.'