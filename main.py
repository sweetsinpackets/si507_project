import pandas as pd
from data_fetch import crawl_main_page, crawl_report_page
from api_call import plot_cases
from print_functions import print_mainpage, print_records


state_abbr_dict = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}


# if the input is a valid state name or state abbr, return the state name, else return None
def check_state_input(name:str):
    if name.title() in state_abbr_dict.values():
        return name.title()
    if name.upper() in state_abbr_dict.keys():
        return state_abbr_dict[name.upper()]
    
    return None




# the execute part
if __name__ == '__main__':
    base_url = "https://www.gunviolencearchive.org/reports"

    try:
        report_dict = crawl_main_page(base_url)
    except:
        print("Can't request GVA page, the page is protected to be only accessible in US. Please check PROXY settings in data_fetch.py and come back!")
        exit()
    
    # define the loop function after selection of a report
    def report_func(url:str)->None:
        try:
            df = crawl_report_page(url)
        except:
            print("Can't crawl the report pages, there might be a problem. Might check your proxy issue or the website.")
            exit()
        
        # print the list
        print_records(df)

        # ask whether to plot
        while True:
            input_str = input("Enter a state name to see records in a state, or \"back\" to back to report selections, or \"exit\" to exit: ")
            # exit
            if input_str.lower() == "exit":
                exit()
            # back to main page
            if input_str.lower() == "back":
                return
            # invalid input
            state_name = check_state_input(input_str)
            if state_name == None:
                print("Invalid input! ")
                continue

            # handle valid input
            # filter
            state_df = df[df["State"] == state_name]
            # print the record
            print_records(state_df)

            # if have no record, definitely don't plot, directly enter loop again
            if len(state_df) == 0:
                continue
                
            # ask whether to print
            while True:
                plot_select = input("Do you want to plot? (y/n): ")
                if plot_select.lower() == "exit":
                    exit()
                if plot_select.lower() not in ["y", "n", "yes", "no"]:
                    print("Invalid input! ")
                    continue
                else:
                    if plot_select.lower() in ["y", "yes"]:
                        try:
                            plot_cases(state_df)
                            print("Generating plot in html...")
                            break
                        except:
                            print("Plot Error! Might because the API request has exceeded the limit.")
                            exit()
                    # if no, continue to ask state
                    print("")
                    break

            # after handling one state selection, ask again
            continue

        return


    # start the main execution
    while True:
        selection_dict = print_mainpage(report_dict)
        
        while True:
            input_str = input("Select a report you want by index or enter \"exit\" to exit the program: ")
            if input_str.lower() == "exit":
                exit()
            
            if input_str.isdigit() and int(input_str) in range(1, len(report_dict.keys()) + 1):
                report_link = report_dict[selection_dict[int(input_str)]]
                report_func(report_link)
                break

            print("Invalid input! ")
            continue
