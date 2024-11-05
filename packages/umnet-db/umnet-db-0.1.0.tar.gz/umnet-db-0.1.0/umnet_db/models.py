# pylint: disable=too-many-ancestors, missing-class-docstring, too-few-public-methods
from ipaddress import ip_address, ip_network, ip_interface
from netaddr import EUI
from datetime import timedelta, datetime
from typing import Optional
from json import dumps

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import ForeignKey
import sqlalchemy.types as types

from sqlalchemy.dialects import postgresql
from sqlalchemy import String, Interval, ARRAY, DateTime


class DBLookupError(Exception):
    def __init__(self, query, table):
        super().__init__(f"Could not find {query} in {table.__name__} table")


#### sqlalchemy column types that map python ipaddress objects
### to string columns
class IPAddressType(types.TypeDecorator):
    impl = postgresql.INET
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return str(value) if value else None

    def process_result_value(self, value, dialect):
        return ip_address(value) if value else None


class IPNetworkType(types.TypeDecorator):
    impl = postgresql.INET
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return str(value) if value else None

    def process_result_value(self, value, dialect):
        return ip_network(value) if value else None


class IPInterfaceType(types.TypeDecorator):
    impl = postgresql.INET
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return str(value) if value else None

    def process_result_value(self, value, dialect):
        return ip_interface(value) if value else None

#### SQLalchemy table models ####
class Base(DeclarativeBase):
    def as_dict(self):
        """
        Return rows as dict
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_json(self):
        """
        Return rows as json
        """
        return dumps(self.as_dict())


class Device(Base):
    __tablename__ = "device"

    name: Mapped[str] = mapped_column(primary_key=True)
    ip: Mapped[ip_address] = mapped_column(IPAddressType, unique=True)
    version: Mapped[Optional[str]]
    vendor: Mapped[Optional[str]]
    model: Mapped[Optional[str]] = mapped_column(String(40))
    serial: Mapped[Optional[str]]

    def __repr__(self):
        return f"Device(name={self.name}, ip={self.ip})"


class Neighbor(Base):
    __tablename__ = "neighbor"

    device: Mapped[str] = mapped_column(ForeignKey("device.name"), primary_key=True)
    port: Mapped[str] = mapped_column(primary_key=True)
    remote_device: Mapped[str]
    remote_port: Mapped[str]

    def __repr__(self):
        return f"Neighbor(device={self.device}, port={self.port})"


class ARP(Base):
    __tablename__ = "arp"

    device: Mapped[str] = mapped_column(ForeignKey("device.name"), primary_key=True)
    interface: Mapped[str] = mapped_column(String(20), primary_key=True)
    ip: Mapped[ip_address] = mapped_column(IPAddressType, primary_key=True)
    mac: Mapped[EUI] = mapped_column(postgresql.MACADDR, primary_key=True)
    first_seen: Mapped[datetime] = mapped_column(DateTime)
    last_seen: Mapped[datetime] = mapped_column(DateTime)


class IPInterface(Base):
    __tablename__ = "ip_interface"

    device: Mapped[str] = mapped_column(ForeignKey("device.name"), primary_key=True)
    ip_address: Mapped[ip_interface] = mapped_column(IPInterfaceType, primary_key=True)
    interface: Mapped[str] = mapped_column(String(20), primary_key=True)
    description: Mapped[str]
    mtu: Mapped[int]
    admin_up: Mapped[bool]
    oper_up: Mapped[bool]
    vrf: Mapped[Optional[str]]

    def __repr__(self):
        return f"IPInterface(device={self.device}, interface={self.interface})"


class Route(Base):
    """
    Device route tables. Note that we mean *active* routes (the FIB).
    In reality pulling the FIB directly off a device is not
    straightforward, and helpful information like protocol and age are not present.
    As a result, this data is actually populated via "show ip route vrf all" (cisco),
    "show route active-path" (junos), "show routing route" (panos)
    """

    __tablename__ = "route"

    device: Mapped[str] = mapped_column(ForeignKey("device.name"), primary_key=True)
    vrf: Mapped[str] = mapped_column(primary_key=True)
    prefix: Mapped[ip_network] = mapped_column(IPNetworkType, primary_key=True)
    nh_interface: Mapped[str] = mapped_column(primary_key=True)
    learned_from: Mapped[str] = mapped_column(primary_key=True)

    protocol: Mapped[str]
    age: Mapped[Optional[timedelta]] = mapped_column(Interval)

    nh_ip: Mapped[Optional[ip_address]] = mapped_column(IPAddressType)
    mpls_label: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    vxlan_vni: Mapped[Optional[int]]
    vxlan_endpoint: Mapped[Optional[ip_address]] = mapped_column(IPAddressType)

    def __repr__(self):
        return f"Route(device={self.device}, vrf={self.vrf}, prefix={self.prefix})"


class VNI(Base):
    __tablename__ = "vni"

    device: Mapped[str] = mapped_column(ForeignKey("device.name"), primary_key=True)
    vni: Mapped[str] = mapped_column(primary_key=True)
    vrf: Mapped[Optional[str]]
    vlan_id: Mapped[Optional[int]]

    def __repr__(self):
        return f"VNI(device={self.device}, vni={self.vni})"


class MPLS(Base):
    """
    MPLS forwarding tables.
    Note that for aggregate labels the "nh_interface" is actually the
    VRF name!
    """

    __tablename__ = "mpls"

    device: Mapped[str] = mapped_column(ForeignKey("device.name"), primary_key=True)
    in_label: Mapped[int] = mapped_column(primary_key=True)
    out_label: Mapped[list[str]] = mapped_column(ARRAY(String))
    nh_interface: Mapped[str] = mapped_column(primary_key=True)
    aggregate: Mapped[bool]

    fec: Mapped[Optional[ip_network]] = mapped_column(IPNetworkType)
    nh_ip: Mapped[Optional[ip_address]] = mapped_column(IPAddressType)
    rd: Mapped[Optional[str]]

    def __repr__(self):
        return f"MPLS(device={self.device}, in_label={self.in_label})"
