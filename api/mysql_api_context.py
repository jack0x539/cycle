import mysql.connector
from api import User, EventRole, Address

class MySqlApiContext:
    username = None
    password = None
    database = None
    hostname = None

    last_error = None
    erred = False

    def clear_error(self):
        self.last_error = None
        self.erred = False

    def set_error(self, error):
        self.last_error = error
        self.erred = True

    def __init__(self, hostname, database, username, password):
        self.username = username
        self.password = password
        self.database = database
        self.hostname = hostname
    
    def connect(self):
        return mysql.connector.connect(
            host = self.hostname,
            user = self.username,
            passwd = self.password,
            database = self.database)
    
    class ApiCursor:
        context = None
        connection = None
        cursor = None

        def __init__(self, context):
            self.context = context

        def __enter__(self):
            self.connection = self.context.connect()
            self.cursor = self.connection.cursor(dictionary=True)
            return self

        def __exit__(self, type, value, traceback):
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

    #begin user
    def get_user(self, id, error_if_not_found = True):
        return self.get(id, "vwUsers", User.from_dict, error_if_not_found)

    def get_users(self, error_if_not_found=False):
        return self.get_all("vwUsers", User.from_dict, error_if_not_found)

    def create_user(self, username, forename, surname, email_address, dob):
        self.clear_error()

        try:
            with self.ApiCursor(self) as ac:
                ac.cursor.execute("INSERT INTO Users (Username, Forename, Surname, EmailAddress, DOB) VALUES (%s, %s, %s, %s, %s)", (username, forename, surname, email_address, dob))
                id = ac.cursor.lastrowid
                ac.connection.commit()
                if id:
                    user = self.get_user(id)
                    if user:
                        return user
                    else:
                        self.set_error("created user with ID {}, but failed to requery - {}".format(id, self.last_error))
                        return None

                self.set_error("failed to create user")
                return None
        except Exception as e:
            self.set_error(str(e))
            return None
    
    def update_user(self, id, username, forename, surname, email_address, dob, primary_role_id):
        params = {
            "Username": username,
            "Forename": forename,
            "Surname": surname,
            "EmailAddress": email_address,
            "DOB": dob,
            "PrimaryEventRoleId": primary_role_id
        }

        return self.update(id, "Users", User.from_dict, params)
    #end user

    #begin generic
    def get(self, id, table, parser, error_if_not_found = True):
        self.clear_error()

        try:
            with self.ApiCursor(self) as ac:
                ac.cursor.execute("SELECT * FROM {} WHERE Id = %s".format(table), (id,))
                rs = ac.cursor.fetchone()
                if rs:
                    return parser(rs)
                else:
                    if error_if_not_found:
                        self.set_error("not found")
                    return None
        except Exception as e:
            self.set_error("get {} failed; {}".format(table, str(e)))
            return None
    
    def get_all(self, table, parser, error_if_not_found = True):
        self.clear_error()

        try:
            with self.ApiCursor(self) as ac:
                ac.cursor.execute("SELECT * FROM {}".format(table))
                rs = ac.cursor.fetchall()   
                roles = [parser(row) for row in rs]

                if not roles and error_if_not_found:
                    self.set_error("not one {} found.".format(table))

                return roles
        except Exception as e:
            self.set_error(str(e))
            return None

    def update(self, id, table, parser, params):
        self.clear_error()

        param_names = ", ".join(["{} = %s".format(p) for p in params])
        query = "UPDATE {} SET {} WHERE Id = %s".format(table, param_names)

        param_values_list = list(params.values())
        param_values_list.append(id)

        try:
            with self.ApiCursor(self) as ac:
                ac.cursor.execute(query, param_values_list)
                ac.connection.commit()
                updated = self.get(id, table, parser)
                if updated:
                    return updated
                else:
                    self.set_error("updated item ({}) with ID {}, but failed to requery - {}".format(table, id, self.last_error))
                    return None
                return None
        except Exception as e:
            self.set_error("failed to update item ({}); {}".format(table, str(e)))
            return None
    #end generic

    #begin address
    def get_address(self, id, error_if_not_found=True):
        return self.get(id, "vwAddresses", Address.from_dict, error_if_not_found)

    def update_address(self, id, address1, address2, address3, county, postcode):
        params = {
            "Address1": address1,
            "Address2": address2,
            "Address3": address3,
            "County": county,
            "Postcode": postcode
        }

        return self.update(id, "Address", Address.from_dict, params)

    def create_user_address(self, user_id, address1, address2, address3, county, postcode):
        self.clear_error()

        try:
            with self.ApiCursor(self) as ac:
                ac.cursor.execute("INSERT INTO Addresses (Id, Address1, Address2, Address3, County, Postcode VALUES (%s, %s, %s, %s, %s)", (address1, address2, address3, county, postcode))
                id = ac.cursor.lastrowid
                ac.connection.commit()
                if id:
                    address = self.get_address(id)
                    if address:
                        return address
                    else:
                        self.set_error("created address with ID {}, but failed to requery - {}".format(id, api.last_error))
                        return None
                
                self.set_error("failed to create address")
                return None
        except Exception as e:
            self.set_error(str(e))
            return None

    #end address

    #begin event role
    def get_event_role(self, id, error_if_not_found = True):
        return self.get(id, "EventRoles", EventRole.from_dict, error_if_not_found)

    def create_event_role(self, name, description):
        self.clear_error()

        try:
            with self.ApiCursor(self) as ac:
                ac.cursor.execute("INSERT INTO EventRoles (Name, Description) VALUES (%s, %s)", (name, description))
                id = ac.cursor.lastrowid
                ac.connection.commit()
                if id:
                    role = self.get_event_role(id)
                    if role:
                        return role
                    else:
                        self.set_error("created event role with ID {}, but failed to requery - {}".format(id, self.last_error))
                        return None

                self.set_error("failed to create event role")
                return None
        except Exception as e:
            self.set_error(str(e))
            return None
    
    def update_event_role(self, id, name, description):
        return self.update(id, "EventRoles", EventRole.from_dict, {"Name":name, "Description":description})

    def get_event_roles(self, error_if_not_found = True):
        return self.get_all("vwEventRoles", EventRole.from_dict, error_if_not_found)

    def delete_event_role(self, id):
        self.clear_error()

        try:
            with self.ApiCursor(self) as ac:
                ac.cursor.execute("UPDATE EventRoles SET RowStatus = 1 WHERE Id = %s", (id,))
                return ac.cursor.rowcount == 1
        except Exception as e:
            self.set_error(str(e))
            return False

    #end event role

    def install(self):
        self.clear_error()
        
        sql = None
        with open("install.sql", "r") as reader:
            sql = reader.read()

        try:
            with self.ApiCursor(self) as ac:
                ac.cursor.execute(sql, multi=True)
        except Exception as e:
            self.set_error(str(e))
