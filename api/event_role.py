class EventRole:
    id = None
    name = None
    description = None
    row_status = None

    @staticmethod
    def from_dict(dict):
        role = EventRole()
        role.id = dict["Id"]
        role.name = dict["Name"]
        role.description = dict["Description"]
        role.row_status = dict["RowStatus"]
        return role