import statistics
import csv
from typing import Dict, List, Set, Tuple
import re
import random
import pandas as pd
import numpy as np


class Person:
    """Represent a person
    """

    def __init__(self, name: str, age: int, department: str, target: Set[str], relationship: str, idea_group: int,
                 living_city: str, hobby: Set[str], email: str) -> None:
        """initialize a person
        :parameter name, age, department, target, relationship, idea group, living city, email
        """
        self.name = name
        self.age = age
        self.department = department
        self.target = target
        self.relationship = relationship
        self.idea_group = idea_group
        self.living_city = living_city
        self.hobby = hobby
        self.email = email


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


class Data:
    """Represent the data
    """

    def __init__(self, department: Set[str], target: Set[str], relationship: Set[str], idea_group: Set[int],
                 living_city: Set[str], hobby: Set[str]):
        """initialize the data
        :parameter: department, target, relationship, idea_group, living_city, hobby
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
                    hobby,
                    person['email']
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
        """return random couple matching
        :parameter lst_match: dictionary with key as name and value as dict[name : match point]
        :return list of tuple of matching people
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
                        potential_match = [name for name in copy_match_dct if copy_match_dct[name] > 5]
                        if not potential_match:  # in case of someone not matching anybody
                            match_person = random.choice([name for name in lst_person_name if name != person])
                        else:
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

    def create_tag(self, lst_person: List[Person]) -> Tuple:
        """create tag of all information types
        :parameter: lst_person: List of person object
        :return: tuple of tags
        """
        tag_department = set([person.department for person in lst_person])
        tag_target = set([target for person in lst_person for target in person.target])
        tag_relationship = set([target for person in lst_person for target in person.relationship])
        tag_idea_group = set([person.idea_group for person in lst_person])
        tag_living_city = set([person.living_city for person in lst_person])
        tag_hobby = set([target for person in lst_person for target in person.hobby])

        return tag_department, tag_target, tag_relationship, tag_idea_group, tag_living_city, tag_hobby

    def write_csv(self, lst_couple: List[Tuple[str, str]], lst_person: List[Person], file_name: str) -> None:
        """write csv file from the list of couple
        :parameter: lst_couple: list of tuple of 2 names
                    lst_person: list of person objects
                    file_name: the file name to export to
        :returns: a csv or excel file in directory
        """
        first_column = [x[0] for x in lst_couple]
        first_column_email = get_personal_info(first_column, lst_person)
        second_column = [x[1] for x in lst_couple]
        second_column_email = get_personal_info(second_column, lst_person)
        # create a dataframe for matching couples
        frame = pd.DataFrame({
            'First person': first_column,
            'Second person': second_column,
            'First person email': first_column_email,
            'Second person email': second_column_email
        })
        frame.to_csv(r'C:\Users\PC\PycharmProjects\VSNL_random_pair_tinder\data\{}'.format(file_name))


def check_duplicate_couple(lst_tuple_1: List[Tuple[str, str]], lst_tuple_2: List[Tuple[str, str]]) -> List[Tuple]:
    """check and print the couple that the same with last month
    """
    error_couple = []
    for tpl in lst_tuple_1:
        if tpl in lst_tuple_2:
            error_couple.append(tpl)
        if (tpl[1], tpl[0]) in lst_tuple_2:
            error_couple.append(tpl)
    return error_couple


def read_last_month_file(file_name: str) -> List[Tuple]:
    """read the file from last month and return a list of tuple
    :parameter: path: path to the file name
    :return: list of tuple of 2 names
    """
    with open(r'C:\Users\PC\PycharmProjects\VSNL_random_pair_tinder\data\{}'.format(file_name)) as f:
        dt = csv.DictReader(f)
        lst_couple = [(person['First person'], person['Second person']) for person in dt]
        return lst_couple






