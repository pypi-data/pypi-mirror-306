import pytest
from pysnmp.proto.rfc1902 import OctetString
from pysnmp.smi import builder, compiler, view
from pysnmp.smi.error import MibNotFoundError
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType


def test_module_not_loaded():

    try:
        mibBuilder = builder.MibBuilder()
        mibBuilder.add_mib_sources(builder.DirMibSource("/opt/pysnmp_mibs"))
        compiler.add_mib_compiler(mibBuilder, sources=[
            'https://mibs.pysnmp.com/asn1/@mib@',
        ], ifAvailable=False)
        
        mibBuilder.load_modules("SNMPv2-MIB", "SNMP-FRAMEWORK-MIB", "SNMP-COMMUNITY-MIB", "WS-CC-STATS-MIB")
        mibView = view.MibViewController(mibBuilder)

        oid, label, suffix = mibView.get_node_name(("wsCcStatsRadio",), "'WS-CC-STATS-MIB")
        assert oid == (1, 3, 6, 1, 4, 1, 14179, 2, 3, 1, 1, 1)
    except Exception as e:
        assert isinstance(e, MibNotFoundError)
