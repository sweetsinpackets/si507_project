from class_definition import record_to_string

# return a selection dict, {count: key}
def print_mainpage(d:dict)->dict:
    count = 1
    selection_dict = {}
    print("======================================")
    print("All reports available are: ")
    print("======================================")
    for i in d.keys():
        print(str(count) + ":  " + str(i))
        selection_dict[count] = i
        count += 1
    print("======================================")
    print("")
    return selection_dict


def print_records(df)->None:
    count = 1
    # if contains no records
    if len(df) == 0:
        print("No record is found! ")
    elif len(df) <= 10:
        print("======================================")
        print("The records found are: ")
        print("======================================")
        for _index, row in df.iterrows():
            print(str(count) + ":  " + record_to_string(row))
            count += 1
        print("======================================")
    else:
        print("======================================")
        print("The top 10 records found are: ")
        print("======================================")        
        for _index, row in df[:10].iterrows():
            print(str(count) + ":  " + record_to_string(row))
            count += 1
        print("......")
        print("======================================")

    print("")
    return

