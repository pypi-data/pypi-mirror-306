#!/usr/bin/env python3
"""
Tests for tray.py.

Run with <filename.py> -v.

See:
https://docs.python.org/3/library/unittest.html#assert-methods
"""

import hashlib
import io
import itertools
import math
import os
import unittest
import sys

import interface
import tray

# required here: <string>.removeprefix()
assert sys.version_info >= (3, 9), 'Python 3.9 or later requried'

assert tuple(
    # remove alpha/beta suffix from version: 1.1a0 becomes 1.1
    int(''.join(itertools.takewhile(lambda v: v.isdigit(), x)))
    for x in interface.__version__.split('.')
) >= (1, 1), (
    'ds20kdb 1.1 or newer required '
    f'(found {interface.__version__})'
)


###############################################################################
# expected responses
###############################################################################


RAW_RESPONSES = {
    '9346429_22_green_tray_05.txt:sipm': {
        1: {
            'column': 10, 'row': 5,
            'line': 'sipm_01, 10,  5  # [SILICONRESIDUE, PASS]',
            'keywords': [14, 2], 'lot_number': 9346429, 'wafer_number': 22
        },
        2: {
            'column': 12, 'row': 15,
            'line': 'sipm_02, 12, 15',
            'keywords': None, 'lot_number': 9346429, 'wafer_number': 22
        },
        3: {
            'column': 13, 'row': 15,
            'line': 'sipm_03, 13, 15',
            'keywords': None, 'lot_number': 9346429, 'wafer_number': 22
        },
        4: {
            'column': 14, 'row': 15,
            'line': 'sipm_04, 14, 15',
            'keywords': None, 'lot_number': 9346429, 'wafer_number': 22
        },
        5: {
            'column': 15, 'row': 15,
            'line': 'sipm_05, 15, 15',
            'keywords': None, 'lot_number': 9346429, 'wafer_number': 22
        },
        6: {
            'column': 16, 'row': 15,
            'line': 'sipm_06, 16, 15',
            'keywords': None, 'lot_number': 9346429, 'wafer_number': 22
        },
        7: {
            'column': 3, 'row': 14,
            'line': 'sipm_07,  3, 14  # [SILICONRESIDUE, PASS]',
            'keywords': [14, 2], 'lot_number': 9346429, 'wafer_number': 22
        },
        8: {
            'column': 4, 'row': 14,
            'line': 'sipm_08,  4, 14  # [SILICONRESIDUE, PASS]',
            'keywords': [14, 2], 'lot_number': 9346429, 'wafer_number': 22
        },
        9: {
            'column': 5, 'row': 14,
            'line': 'sipm_09,  5, 14  # [SILICONRESIDUE, PASS]',
            'keywords': [14, 2], 'lot_number': 9346429, 'wafer_number': 22
        },
        10: {
            'column': 6, 'row': 14,
            'line': 'sipm_10,  6, 14  # [SILICONRESIDUE, PASS]',
            'keywords': [14, 2], 'lot_number': 9346429, 'wafer_number': 22
        },
        11: {
            'column': 7, 'row': 14,
            'line': 'sipm_11,  7, 14  # [SILICONRESIDUE, PASS]',
            'keywords': [14, 2], 'lot_number': 9346429, 'wafer_number': 22
        },
        12: {
            'column': 8, 'row': 14,
            'line': 'sipm_12,  8, 14  # [SILICONRESIDUE, PASS]',
            'keywords': [14, 2], 'lot_number': 9346429, 'wafer_number': 22
        },
        13: {
            'column': 9, 'row': 14,
            'line': 'sipm_13,  9, 14',
            'keywords': None, 'lot_number': 9346429, 'wafer_number': 22
        },
        14: {
            'column': 11, 'row': 5,
            'line': 'sipm_14, 11,  5  # [SILICONRESIDUE, PASS]',
            'keywords': [14, 2], 'lot_number': 9346429, 'wafer_number': 22
        },
        15: {
            'column': 11, 'row': 14,
            'line': 'sipm_15, 11, 14  # [VERTRAILFLAW, EM, PASS]',
            'keywords': [15, 6, 2], 'lot_number': 9346429, 'wafer_number': 22
        },
        16: {
            'column': 12, 'row': 14,
            'line': 'sipm_16, 12, 14',
            'keywords': None, 'lot_number': 9346429, 'wafer_number': 22
        },
        17: {
            'column': 13, 'row': 14,
            'line': 'sipm_17, 13, 14',
            'keywords': None, 'lot_number': 9346429, 'wafer_number': 22
        },
        18: {
            'column': 14, 'row': 14,
            'line': 'sipm_18, 14, 14',
            'keywords': None, 'lot_number': 9346429, 'wafer_number': 22
        },
        19: {
            'column': 15, 'row': 14,
            'line': 'sipm_19, 15, 14',
            'keywords': None, 'lot_number': 9346429, 'wafer_number': 22
        },
        20: {
            'column': 3, 'row': 13,
            'line': 'sipm_20,  3, 13',
            'keywords': None, 'lot_number': 9346429, 'wafer_number': 22
        },
        21: {
            'column': 4, 'row': 13,
            'line': 'sipm_21,  4, 13  # [SILICONRESIDUE, PASS]',
            'keywords': [14, 2], 'lot_number': 9346429, 'wafer_number': 22
        },
        22: {
            'column': 5, 'row': 13,
            'line': 'sipm_22,  5, 13  # [SILICONRESIDUE, PASS]',
            'keywords': [14, 2], 'lot_number': 9346429, 'wafer_number': 22
        },
        23: {
            'column': 6, 'row': 13,
            'line': 'sipm_23,  6, 13  # [SILICONRESIDUE, PASS]',
            'keywords': [14, 2], 'lot_number': 9346429, 'wafer_number': 22
        },
        24: {
            'column': 8, 'row': 13,
            'line': 'sipm_24,  8, 13  # [SILICONRESIDUE, PASS]',
            'keywords': [14, 2], 'lot_number': 9346429, 'wafer_number': 22
        },
    },
    'no_default_wafer.txt:sipm': {
        7: {
            'column': 10, 'row': 10,
            'line': 'sipm_07, 10, 10, 9323959, 8',
            'keywords': None, 'lot_number': 9323959, 'wafer_number': 8
        },
    },
    'no_default_wafer.txt:import_errors': [
        'default wafer lot and/or number missing: required by SiPM 6'
    ],
    'mixed_sipm_representations.txt:sipm': {
        6: {
            'column': 16, 'row': 15,
            'line': 'sipm_06, 16, 15',
            'keywords': None, 'lot_number': 9262109, 'wafer_number': 12
        },
        7: {
            'column': 10, 'row': 10,
            'line': 'sipm_07, 10, 10, 9323959, 8',
            'keywords': None, 'lot_number': 9323959, 'wafer_number': 8
        },
    },
    'mixed_sipm_representations_leading_zero_options:sipm': {
        6: {
            'column': 16, 'row': 15,
            'line': 'sipm_6, 16, 15',
            'keywords': None, 'lot_number': 9262109, 'wafer_number': 12
        },
        7: {
            'column': 10, 'row': 10,
            'line': 'sipm_00000007, 10, 10, 9323959, 8',
            'keywords': None, 'lot_number': 9323959, 'wafer_number': 8
        },
    }
}


###############################################################################
# TESTS | test.py, general
###############################################################################


class TestUtilities(unittest.TestCase):
    """
    test.py
    """

    def test_import_from_file(self):
        """
        Check file import from various test tray files.
        """
        # standard tray file as generated by ds20k_gen_tray_files_gui
        trf = tray.Tray(
            os.path.join('test_files', '9346429_22_green_tray_05.txt')
        )
        self.assertEqual(trf.sipms, RAW_RESPONSES['9346429_22_green_tray_05.txt:sipm'])

        # missing default wafer information, and a SiPM present that needs it
        trf = tray.Tray(os.path.join('test_files', 'no_default_wafer.txt'))
        self.assertEqual(trf.sipms, RAW_RESPONSES['no_default_wafer.txt:sipm'])
        self.assertEqual(
            trf.import_errors, RAW_RESPONSES['no_default_wafer.txt:import_errors']
        )

        # A SiPM definition that is complete, and one that requires default
        # wafer info.
        trf = tray.Tray(
            os.path.join('test_files', 'mixed_sipm_representations.txt')
        )
        self.assertEqual(
            trf.sipms, RAW_RESPONSES['mixed_sipm_representations.txt:sipm']
        )

        # out-of-order default wafer definition
        # the response should be the same as the above
        trf = tray.Tray(
            os.path.join('test_files', 'mixed_sipm_representations_ooo.txt')
        )
        self.assertEqual(
            trf.sipms, RAW_RESPONSES['mixed_sipm_representations.txt:sipm']
        )

        # no leading zeroes and excessive leading zero padding for sipm idents
        # the line section will be different, everything else will be the same
        trf = tray.Tray(
            os.path.join(
                'test_files', 'mixed_sipm_representations_leading_zero_options.txt'
            )
        )
        self.assertEqual(
            trf.sipms, RAW_RESPONSES[
                'mixed_sipm_representations_leading_zero_options:sipm'
            ]
        )

    def test_export_to_file(self):
        """
        Check file export.
        """
        # import known good file into memory, obtain hash of its exported file
        known_good_tray = tray.Tray(
            os.path.join('test_files', '9346429_22_green_tray_05.txt')
        )
        with io.StringIO() as output:
            known_good_tray.export_to_file(output)
            output.seek(0)
            known_good_tray_hash = hashlib.sha256(output.read().encode()).hexdigest()

        # compare hash to that of a previously exported file
        outfile = os.path.join('test_files', '9346429_22_green_tray_05_export.txt')
        with open(outfile, 'r', encoding='utf-8') as f:
            reference_export_hash = hashlib.sha256(f.read().encode()).hexdigest()

        self.assertEqual(known_good_tray_hash, reference_export_hash)

    def test_sipm_key(self):
        """
        Test SiPM line identification.
        """
        challenge_response = {
            # valid
            'sipm_1': ('sipm_1', 1),
            'sipm_01': ('sipm_1', 1),
            'sipm_24': ('sipm_24', 24),
            # invalid
            'sipm_0': ('sipm_0', None),
            'sipm_25': ('sipm_25', None),
            'sipm23': (None, None),
            '': (None, None),
            1: (None, None),
            math.inf: (None, None),
            math.nan: (None, None),
            None: (None, None),
        }
        for chal, resp in challenge_response.items():
            self.assertEqual(tray.sipm_key(chal), resp)


###############################################################################
if __name__ == '__main__':
    unittest.main()
