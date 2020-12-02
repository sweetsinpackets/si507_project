class shooting_record:
    '''
    incident_id : int
    incident_date : str
    state : str
    city_or_county : str
    address : str
    killed : int
    injured : int
    '''
    def __init__(self, incident_id:str=None, incident_date:str=None, state:str=None, city_or_county:str=None, address:str=None, killed:str=None, injured:str=None, init_list:list=None):
        if init_list:
            # initialize from list
            self.incident_id = int(init_list[0])
            self.incident_date = init_list[1] if init_list[1] not in ["", None] else None
            self.state = init_list[2] if init_list[2] not in ["", None] else None
            self.city_or_county = init_list[3] if init_list[3] not in ["", None] else None
            self.address = init_list[4] if init_list[4] not in ["", None] else None
            self.killed = int(init_list[5]) if init_list[5] not in ["", None] else None
            self.injured = int(init_list[6]) if init_list[6] not in ["", None] else None
        else:
            # automatically do format transfer
            self.incident_id = int(incident_id) if incident_id not in ["", None] else None
            self.incident_date = incident_date if incident_date not in ["", None] else None
            self.state = state if state not in ["", None] else None
            self.city_or_county = city_or_county if city_or_county not in ["", None] else None
            self.address = address if address not in ["", None] else None
            self.killed = int(killed) if killed not in ["", None] else None
            self.injured = int(injured) if injured not in ["", None] else None
        

    def __str__(self):
        output = "Accident " + str(self.incident_id)
        if self.incident_date:
            output += " on " + self.incident_date
        if self.city_or_county and self.state:
            output += " in " + self.city_or_county + ", " + self.state
        elif self.city_or_county or self.state:
            output += " in "
            output += self.city_or_county if self.city_or_county else ""
            output += self.state if self.state else ""
        if self.address:
            output += " (" + self.address + ")"
        if self.killed or self.injured:
            output += " causes"
            if self.killed:
                output += " " + str(self.killed) + " death"
            if self.killed and self.injured:
                output += " and"
            if self.injured:
                output += " " + str(self.injured) + " injure"
        return output + ". "
    



# transformed from a init_list to a modified list
def transform(init_list:list)->dict:
    res = {}
    res["Incident ID"] = int(init_list[0])
    res["Incident Date"] = init_list[1] if init_list[1] not in ["", None] else None
    res["State"] = init_list[2] if init_list[2] not in ["", None] else None
    res["City or County"] = init_list[3] if init_list[3] not in ["", None] else None
    res["Address"] = init_list[4] if init_list[4] not in ["", None] else None
    res["# Killed"] = int(init_list[5]) if init_list[5] not in ["", None] else None
    res["# Injured"] = int(init_list[6]) if init_list[6] not in ["", None] else None
    return res


# transformed to a string
def record_to_string(row)->str:
    output = "Accident " + str(row["Incident ID"])
    if row["Incident Date"]:
        output += " on " + row["Incident Date"]
    if row["City or County"] and row["State"]:
        output += " in " + row["City or County"] + ", " + row["State"]
    elif row["City or County"] or row["State"]:
        output += " in "
        output += row["City or County"] if row["City or County"] else ""
        output += row["State"] if row["State"] else ""
    if row["Address"]:
        output += " (" + row["Address"] + ")"
    if row["# Killed"] or row["# Injured"]:
        output += " causes"
        if row["# Killed"]:
            output += " " + str(row["# Killed"]) + " death"
        if row["# Killed"] and row["# Injured"]:
            output += " and"
        if row["# Injured"]:
            output += " " + str(row["# Injured"]) + " injure"
    return output + ". "
    