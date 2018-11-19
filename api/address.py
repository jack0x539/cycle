class Address:
    id = None
    address_line_1 = None   
    address_line_2 = None
    address_line_3 = None
    county = None
    postcode = None
    row_status = None

    @staticmethod
    def from_dict(dict):
        a = Address()
        a.id = dict["Id"]
        a.address_line_1 = dict["Address1"]
        a.address_line_2 = dict["Address2"]
        a.address_line_3 = dict["Address3"]
        a.county = dict["County"]
        a.postcode = dict["Postcode"]
        a.row_status = dict["RowStatus"]
        return a