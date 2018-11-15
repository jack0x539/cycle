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
        self.clear_error()

        try:
            with self.ApiCursor(self) as ac:
                ac.cursor.execute("SELECT * FROM Users WHERE Id = %s", (id,))
                rs = ac.cursor.fetchone()
                if rs:
                    return User.from_dict(rs)
                else:
                    if error_if_not_found:
                        self.set_error("not found")
                    return None
        except Exception as e:
            self.set_error("get_user failed; {}".format(str(e)))
            return None

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
    
    def update_user(self, id, username, forename, surname, email_address, dob):
        self.clear_error()

        try:
            with self.ApiCursor(self) as ac:
                ac.cursor.execute("UPDATE Users SET Username = %s, Forename = %s, Surname = %s, EmailAddress = %s, DOB = %s WHERE Id = %s", (username, forename, surname, email_address, dob, id))
                ac.connection.commit()
                user = self.get_user(id)
                if user:
                    return user
                else:
                    self.set_error("updated user with ID {}, but failed to requery - {}".format(id, self.last_error))
                    return None
                return None
        except Exception as e:
            self.set_error("failed to update user; {}".format(str(e)))
            return None

    def get_users(self):
        self.clear_error()

        try:
            with self.ApiCursor(self) as ac:
                ac.cursor.execute("SELECT * FROM Users")
                rs = ac.cursor.fetchall()
                users = [User.from_dict(row) for row in rs]
                return users
        except Exception as e:
            self.set_error(str(e))
            return None
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
                ac.cursor.execute("SELECT * FROM {} WHERE RowStatus = 0".format(table))
                rs = ac.cursor.fetchall()   
                roles = [parser(row) for row in rs]

                if not roles and error_if_not_found:
                    self.set_error("not one {} found.".format(table))

                return roles
        except Exception as e:
            self.set_error(str(e))
            return None
    #end generic

    #begin address
    def get_address(self, id, error_if_not_found=True):
        return self.get(id, "Addresses", Address.from_dict, error_if_not_found)
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
        self.clear_error()

        try:
            with self.ApiCursor(self) as ac:
                ac.cursor.execute("UPDATE EventRoles SET Name = %s, Description = %s WHERE Id = %s", (name, description, id))
                ac.connection.commit()
                role = self.get_event_role(id)
                if role:
                    return role
                else:
                    self.set_error("updated event role with ID {}, but failed to requery - {}".format(id, self.last_error))
                    return None
                return None
        except Exception as e:
            self.set_error("failed to update event role; {}".format(str(e)))
            return None

    def get_event_roles(self, error_if_not_found = True):
        return self.get_all("EventRoles", EventRole.from_dict, error_if_not_found)

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
