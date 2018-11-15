class Address:
    id = None
    address_line_1 = None   
    address_line_2 = None
    address_line_3 = None
    county = None
    postcode = None

    @staticmethod
    def from_dict(dict):
        a = Address()
        a.id = dict["Id"]
        a.address_line_1 = dict["AddressLine1"]
        a.address_line_2 = dict["AddressLine2"]
        a.address_line_3 = dict["AddressLine3"]
        a.county = dict["County"]
        a.postcode = dict["Postcode"]
        return a