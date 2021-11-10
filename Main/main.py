from Tools import *

data = Data({''}, {''}, {''}, {1}, {''}, {''})
sth = Data.clean_data(data, r'..\data\vsnl.csv')
match_data = Data.match_data(data, sth)  # get matching data
match_couples = Data.pick_something(data, match_data)  # get match couples
clean_data = Data(*Data.create_tag(data, sth))  # create an legitimate data object with tags
clean_data.write_csv(match_couples, sth)  # write new csv files
print(match_couples)
print(clean_data.tag_relationship)
