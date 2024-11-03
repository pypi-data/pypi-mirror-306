import pytest
from pysnmp.proto.rfc1902 import OctetString
from pysnmp.smi import builder, view
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType

mibBuilder = builder.MibBuilder()
mibBuilder.add_mib_sources(builder.DirMibSource("/opt/pysnmp_mibs"))
mibBuilder.load_modules("SNMPv2-MIB", "SNMP-FRAMEWORK-MIB", "SNMP-COMMUNITY-MIB", "PYSNMP-USM-MIB")
mibView = view.MibViewController(mibBuilder)


def test_255t():

    # Construct the ObjectIdentity for pysnmpUsmSecretUserName
    pysnmpUsmSecretUserName_oid = ObjectIdentity('PYSNMP-USM-MIB', 'pysnmpUsmSecretUserName')

    # Construct the ObjectType for pysnmpUsmSecretUserName
    pysnmpUsmSecretUserName_obj = ObjectType(pysnmpUsmSecretUserName_oid, 'lex')

    assert pysnmpUsmSecretUserName_obj.resolve_with_mib(mibView).prettyPrint() == 'PYSNMP-USM-MIB::pysnmpUsmSecretUserName = lex'
