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
        from api import EventRole, Address

        user = User()
        user.id = dict["Id"]
        user.username = dict["Username"]
        user.forename = dict["Forename"]
        user.surname = dict["Surname"]
        user.email_address = dict["EmailAddress"]
        user.dob = dict["DOB"]

        address_dict = {
            "Id": dict["AddressId"],
             "Address1": dict["Address1"],
             "Address2": dict["Address2"],
             "Address3": dict["Address3"],
             "County": dict["County"],
             "Postcode": dict["Postcode"],
             "RowStatus": 0
        }
        user.address = Address.from_dict(address_dict)

        role_dict = {
            "Id": dict["PrimaryEventRoleId"],
            "Name": dict["PrimaryEventRoleName"],
            "Description": dict["PrimaryEventRoleDescription"],
            "RowStatus": 0
        }
        user.primary_event_role = EventRole.from_dict(role_dict)

        return user