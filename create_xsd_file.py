import pandas as pd

df = pd.read_csv("cr_md.csv", sep=";", dtype=str, encoding="utf-8")

lines = ""

xmlBegin = '''<?xml version="1.0" encoding="utf-8"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" version="1.0">
    <xsd:element name="BusinessPartner">
        <xsd:annotation>
            <xsd:documentation>Business Partner</xsd:documentation>
        </xsd:annotation>
        <xsd:complexType>
            <xsd:sequence>
                <xsd:element name="BusinessPartner">
                    <xsd:complexType>
                        <xsd:sequence>
'''

xmlEnd = '''           </xsd:sequence>
                    </xsd:complexType>
                </xsd:element>
            </xsd:sequence>
        </xsd:complexType>
    </xsd:element>
</xsd:schema>
'''

for index, row in df.iterrows():
    lines += '''<xsd:element name="{}" minOccurs="0">
                    <xsd:annotation>
                        <xsd:documentation>{}</xsd:documentation>
                    </xsd:annotation>
                    <xsd:simpleType>
                        <xsd:restriction base="xsd:string">
                            <xsd:maxLength value="{}" />
                        </xsd:restriction>
                    </xsd:simpleType>
                </xsd:element>\n'''.format(row["field"], row["descr"], row["len"])

csv = xmlBegin + lines + xmlEnd

with open('cr_stammdaten.xsd', 'w') as f:
    f.write(csv)
