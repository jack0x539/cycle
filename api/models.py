from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    line1 = Column(String(256))
    line2 = Column(String(256))
    line3 = Column(String(256))
    county = Column(String(256))
    postcode = Column(String(256))

class EventRole(Base):
    __tablename__ = "event_role"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(256), nullable=False, unique=True) 
    description = Column(String(512))

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(64), nullable=False, unique=True)
    forename = Column(String(128))
    surname = Column(String(128))
    dob = Column(Date)
    email_address = Column(String(512))

    address_id = Column(Integer, ForeignKey("address.id"))
    address = relationship("Address", backref=backref("user_address", uselist=False))

    default_event_role = relationship("EventRole", backref=backref("event_role", uselist=False))
    default_event_role_id = Column(Integer, ForeignKey("event_role.id"))

class ChargeType(Base):
    __tablename__ = "charge_type"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(256), nullable=False, unique=True) 
    description = Column(String(512))

class WeatherCondition(Base):
    __tablename__ = "weather_condition"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(256), nullable=False, unique=True) 
    description = Column(String(512))

class EventType(Base):
    __tablename__ = "event_type"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(256), nullable=False, unique=True) 
    description = Column(String(512))

    default_charge_type_id = Column(Integer, ForeignKey("charge_type.id"))
    default_charge_type = relationship("ChargeType", backref=backref("charge_type", uselist=False))

class EventLocation(Base):
    __tablename__ = "event_location"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(256), nullable=False, unique=True) 
    description = Column(String(512))
    contact_name = Column(String(512))
    contact_email_address = Column(String(512))
    contact_telephone1 = Column(String(64))
    contact_telephone2 = Column(String(64))

    address_id = Column(Integer, ForeignKey("address.id"))
    address = relationship("Address", backref=backref("event_address", uselist=False))

class Partnership(Base):
    __tablename__ = "partnership"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(256), nullable=False, unique=True) 
    description = Column(String(512))