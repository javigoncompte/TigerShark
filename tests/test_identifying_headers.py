import datetime
import os
import unittest

from tigershark.facade.common import IdentifyingHeaders
from tigershark.parsers import IdentifyingParser


class TestIdentifyingHeaders(unittest.TestCase):

    def parse_file(self, name):
        with open(os.path.join('tests', name)) as f:
            parsed = IdentifyingParser.unmarshall(
                f.read().strip(), ignoreExtra=True)
        return IdentifyingHeaders(parsed)

    def test_5010_details(self):
        facade = self.parse_file('5010-835-example-1.txt')

        control = facade.facades[0].interchange_control

        self.assertEqual(control.authorization_information_qualifier, '00')
        self.assertEqual(control.authorization_information, '          ')

        self.assertEqual(control.security_information_qualifier, '00')
        self.assertEqual(control.security_information, '          ')

        self.assertEqual(control.interchange_sender_id_qualifier, 'ZZ')
        self.assertEqual(control.interchange_sender_id, '5010TEST       ')

        self.assertEqual(control.interchange_receiver_id_qualifier, 'ZZ')
        self.assertEqual(control.interchange_receiver_id, '835RECVR       ')

        self.assertEqual(control.interchange_date, datetime.date(2011, 9, 30))
        self.assertEqual(control.interchange_time, datetime.time(11, 5))

        self.assertEqual(control.interchange_control_standards_id, '^')
        self.assertEqual(control.interchange_control_version_number, '00501')
        self.assertEqual(control.interchange_control_number, '000004592')

        self.assertEqual(control.acknowledgement_requested, '0')
        self.assertEqual(control.test_indicator, 'T')
        self.assertEqual(control.subelement_separator, '|')