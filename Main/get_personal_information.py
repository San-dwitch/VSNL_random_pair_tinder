from Tools import *


def get_personal_info(lst: List[str], lst_person: List[Person]) -> List[str]:
    """get personal information from name
    :parameter: lst: List of names
    :return: list of personal information
    """
    personal_info = []
    for name in lst:
        for person in lst_person:
            if person.name == name:
                personal_info.append(person.email)
                break
    return personal_info
