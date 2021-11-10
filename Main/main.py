from Tools import *


def compute_data(file_name: str) -> List[Tuple]:
    """compute data, change the csv file
    """
    data = Data({''}, {''}, {''}, {1}, {''}, {''})
    sth = Data.clean_data(data, r'..\data\vsnl.csv')  # get list of person object
    match_data = Data.match_data(data, sth)  # get matching data
    match_couples = Data.pick_something(data, match_data)  # get match couples
    clean_data = Data(*Data.create_tag(data, sth))  # create an legitimate data object with tags
    clean_data.write_csv(match_couples, sth, file_name)  # write new csv files
    return match_couples


def main(file_name: str, lst_file_name: str):
    """check with last month file, and compute new data
    """
    done = True
    while done:
        new_lst = compute_data(file_name)
        old_lst = read_last_month_file(lst_file_name)
        if not check_duplicate_couple(new_lst, old_lst):
            done = False


compute_data(f'pair couples.csv')
main('new pair couple.csv', 'pair couples.csv')

