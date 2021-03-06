import datetime
import os
import unittest

from tigershark import X12_4010_X092A1
from tigershark import X12_5010_X221A1
from tigershark.facade.control import ControlHeaders
from tigershark.parsers import parse_control_headers

from tests import TEST_FILE_MAP


class TestControlHeaders(unittest.TestCase):

    def parse_file(self, name):
        with open(os.path.join('tests', name)) as f:
            parsed = parse_control_headers(f.read().strip())
        return ControlHeaders(parsed)

    def test_5010_details(self):
        facade = self.parse_file('5010-835-example-1.txt')

        control = facade.interchange_controls[0]

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

        group = control.functional_groups[0]

        self.assertEqual(group.functional_id_code, 'HP')

        self.assertEqual(group.application_sender_code, '5010TEST')
        self.assertEqual(group.application_receiver_code, '835RECVR')

        self.assertEqual(group.date, datetime.date(2011, 9, 30))
        self.assertEqual(group.time, datetime.time(10, 7, 18))

        self.assertEqual(group.group_control_number, '45920001')

        self.assertEqual(group.responsible_agency_code, 'X')

        self.assertEqual(group.version_indicator_code, '005010X221A1')

        self.assertTrue(group.version_tuple.is_5010)
        self.assertEqual(group.version_tuple, X12_5010_X221A1)

    def test_4010_details(self):
        facade = self.parse_file('271-example.txt')

        control = facade.interchange_controls[0]

        self.assertEqual(control.authorization_information_qualifier, '00')
        self.assertEqual(control.authorization_information, '          ')

        self.assertEqual(control.security_information_qualifier, '00')
        self.assertEqual(control.security_information, '          ')

        self.assertEqual(control.interchange_sender_id_qualifier, 'ZZ')
        self.assertEqual(control.interchange_sender_id, 'ZIRMED         ')

        self.assertEqual(control.interchange_receiver_id_qualifier, 'ZZ')
        self.assertEqual(control.interchange_receiver_id, '12345          ')

        self.assertEqual(control.interchange_date, datetime.date(2012, 6, 5))
        self.assertEqual(control.interchange_time, datetime.time(23, 24))

        self.assertEqual(control.interchange_control_standards_id, 'U')
        self.assertEqual(control.interchange_control_version_number, '00401')
        self.assertEqual(control.interchange_control_number, '000050033')

        self.assertEqual(control.acknowledgement_requested, '1')
        self.assertEqual(control.test_indicator, 'P')
        self.assertEqual(control.subelement_separator, '^')

        group = control.functional_groups[0]

        self.assertEqual(group.functional_id_code, 'HB')

        self.assertEqual(group.application_sender_code, 'ZIRMED')
        self.assertEqual(group.application_receiver_code, '12345')

        self.assertEqual(group.date, datetime.date(2012, 6, 5))
        self.assertEqual(group.time, datetime.time(23, 24))

        self.assertEqual(group.group_control_number, '50025')

        self.assertEqual(group.responsible_agency_code, 'X')

        self.assertEqual(group.version_indicator_code, '004010X092A1')

        self.assertTrue(group.version_tuple.is_4010)
        self.assertEqual(group.version_tuple, X12_4010_X092A1)

    def test_all_parseable(self):
        all_tests = sorted(TEST_FILE_MAP.items())
        for (transaction_set_id, version_tuple), name in all_tests:
            facade = self.parse_file(name)
            control = facade.interchange_controls[0]
            group = control.functional_groups[0]
            self.assertEqual(group.version_tuple, version_tuple)
            transaction_set = group.transaction_sets[0]
            self.assertEqual(transaction_set.transaction_set_identifier_code,
                             transaction_set_id)
            self.assertIs(transaction_set.functional_group, group)
