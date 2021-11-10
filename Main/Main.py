import statistics
import csv
from typing import Dict, List, Set
import re
import random


class Person:
    """Represent a person
    """

    def __init__(self, name: str, age: int, department: str, target: Set[str], relationship: str, idea_group: int,
                 living_city: str, hobby: Set[str]) -> None:
        """initialize a person
        :parameter name, age, department, target, relationship, idea group, living city
        """
        self.name = name
        self.age = age
        self.department = department
        self.target = target
        self.relationship = relationship
        self.idea_group = idea_group
        self.living_city = living_city
        self.hobby = hobby


class Data:
    """Represent the data
    """

    def __init__(self, department: Set[str], target: Set[str], relationship: Set[str], idea_group: Set[int],
                 living_city: Set[str], hobby: Set[str]):
        """initialize the data
        :parameter: department, target, relationship, idea_group, living_city
        """
        self.tag_relationship = relationship
        self.tag_idea_group = idea_group
        self.tag_target = target
        self.tag_living_city = living_city
        self.tag_hobby = hobby
        self.tag_department = department

    def clean_data(self, path: str) -> List[Person]:
        """clean the data
        :parameter path to a file
        :return a list of person object
        """
        lst_person: List[Person] = []
        with open(path) as f:
            dt = csv.DictReader(f)
            for person in dt:
                age = 2021 - int((re.findall('\d{4}', person['Date of birth']))[0])  # compute age
                target = person['Main target'].split(',')  # compute set of main target
                target = set([x.strip() for x in target])
                hobby = person['Hobby'].split(',')  # compute the set of hobby
                hobby = set([x.strip() for x in hobby])
                idea_group = int(person['idea group'])

                # create temporary person
                temp_person = Person(
                    person['Name'],
                    age,
                    person['from department'],
                    target,
                    person['Relationship'],
                    idea_group,
                    person['Living city'],
                    hobby
                )
                lst_person.append(temp_person)

            return lst_person

    def match_data(self, lst_person: List[Person]) -> Dict:
        """create a list of dict with key as a person name and value as person that they highly match
        :parameter lst_person: list of person objects
        :return dict with key as person name, value as dict of person name with matching point
        """
        temp_dct: Dict[str: Dict[str, int]] = {}
        for person in lst_person:
            sub_temp_dct: Dict[str, int] = {}
            for other_person in lst_person:
                temp_match_point: int = 0
                if other_person == person:
                    continue
                else:
                    temp_match_point += len(person.target.intersection(other_person.target))  # main target point:1 each
                    if person.living_city == other_person.living_city:  # living city point: 3
                        temp_match_point += 3
                    temp_match_point += len(person.hobby.intersection(other_person.hobby))  # hobby point: 1 each
                    if abs(person.age - other_person.age) <= 2:  # age point: 1
                        temp_match_point += 1
                sub_temp_dct[other_person.name] = temp_match_point  # assign name of other person to match point
            temp_dct[person.name] = sub_temp_dct  # assign name of person to list match point
        return temp_dct

    def pick_something(self, lst_match: Dict):
        """write a csv file about matching couples
        """
        lst_couples = []
        lst_person_name = [name for name in lst_match]  # lst of person name
        for person, match_dct in lst_match.items():
            if person not in lst_person_name:
                continue
            else:
                copy_match_dct = match_dct.copy()
                done = True
                while done:
                    if copy_match_dct == {}:
                        match_person = 'Phat'
                    else:
                        max_point = max(copy_match_dct.values())
                        potential_match = [name for name in copy_match_dct if copy_match_dct[name] == max_point]
                        match_person = random.choice(potential_match)
                        if match_person in lst_person_name:
                            done = False
                            lst_person_name.remove(match_person)
                            lst_person_name.remove(person)
                        else:
                            copy_match_dct.pop(match_person)
                temp_tuple = (person, match_person)
                lst_couples.append(temp_tuple)
        return lst_couples

concac = Data({}, {}, {}, {}, {}, {})
sth = Data.clean_data(concac, r'..\data\vsnl.csv')
match_data = Data.match_data(concac, sth)
bruh = Data.pick_something(concac, match_data)
print(bruh)








