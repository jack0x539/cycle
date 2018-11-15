class User:
    id = None
    username = None
    forename = None
    surname = None
    email_address = None
    dob = None
    primary_event_role = None
    address = None

    @staticmethod
    def from_dict(dict):
        user = User()
        user.id = dict["Id"]
        user.username = dict["Username"]
        user.forename = dict["Forename"]
        user.surname = dict["Surname"]
        user.email_address = dict["EmailAddress"]
        user.dob = dict["DOB"]
        user.primary_event_role = dict["PrimaryEventRoleId"]
        user.address = dict["AddressId"]
        return user