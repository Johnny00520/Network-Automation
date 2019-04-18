#!/bin/env python
from ncclient import manager
import sys, os, warnings
warnings.simplefilter("ignore", DeprecationWarning)
from lxml import etree


CREATE_INTERFACE_IP = """
    <interface-configurations xmlns="http://cisco.com/yang/Cisco-IOS-XR-ifmgr-cfg">
        <hostname>Lab9XR</hostname>
        <interface-configuration>
            <active>act</active>
            <interface-name>Loopback1</interface-name>
            <interface-virtual></interface-virtual>
            <ipv4-network xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
            <addresses>
                <primary>
                    <address>10.11.12.13</address>
                    <netmask>255.255.255.255</netmask>
                </primary>
            </addresses>
            </ipv4-network>
        </interface-configuration>
    </interface-configurations>
"""
CONFIG_DATA_ACCESSLIST= """
    <rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <edit-config>
        <target><candidate/></target>
        <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <ipv4-acl-and-prefix-list xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-acl-cfg"  xc:operation=”merge”>
            <accesses>
                <access>
                    <access-list-name>acess-server1</access-list-name>
                    <access-list-entries>
                        <access-list-entry>
                        <sequence-number>10</sequence-number>
                        <grant>permit</grant>
                        <source-network>
                            <source-address>198.51.100.2</source-address>
                            <source-wild-card-bits>0.0.0.255</source-wild-card-bits>
                        </source-network>
                        </access-list-entry>
                        <access-list-entry>
                        <sequence-number>20</sequence-number>
                        <grant>deny</grant>
                        <source-network>
                        <source-address>0.0.0.0</source-address>
                        <source-wild-card-bits>255.255.255.255</source-wild-card-bits>
                        </source-network>
                        </access-list-entry>
                        </access-list-entries>
                        </access>
                    </accesses>
                </ipv4-acl-and-prefix-list>
            </config>
        </edit-config>
   </rpc>
"""

CONFIG_DATA_INTERFACE = """
    <control-plane xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-lib-mpp-cfg">
        <management-plane-protection>
            <inband>
                <interface-selection>
                    <interfaces>
                        <interface>
                        <interface-name>GigabitEthernet0/0/0/0</interface-name>
                        <all-protocols>
                        <access-group>10</access-group>
                        <access-group>20</access-group>
                        </all-protocols>
                        </interface>
                    </interfaces>
                </interface-selection>
            </inband>
        </management-plane-protection>
    </control-plane>
"""


def create_config(conn):
    try:
	    conn.edit_config(CREATE_INTERFACE_IP)
        #conn.commit()

    except Exception:
        print("Exception occurs while creating interface")

def main():
    try:
        with manager.connect(
            host="198.51.100.10",
            port=830,
            username="lab",
            password="lab",
            hostkey_verify=False,
            allow_agent=False,
            look_for_keys=False,
            device_params={'name':'iosxr'},
            ) as conn_manager:

            #c=conn_manager.get_config(source='running').data_xml
            #print(c)
            conn_manager.edit_config(CONFIG_DATA_ACCESSLIST)
            conn_manager.edit_config(CREATE_INTERFACE_IP)
            conn_manager.edit_config(CONFIG_DATA_INTERFACE)
            conn_manager.commit()

            output_data = conn_manager.get_config(source="running",filter=('subtree',etree.Element("Configuration")))
            print(output_data)

    except Exception:
        print("Something Wrong")
        pass

if __name__ == "__main__":
	main()
