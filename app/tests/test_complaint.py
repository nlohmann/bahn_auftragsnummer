# coding=utf-8

########################################################################
# Licensed under the MIT License <http://opensource.org/licenses/MIT>. #
# Copyright (c) 2017 Niels Lohmann <http://nlohmann.me>.               #
########################################################################

from unittest import TestCase
import os.path
from app.Complaint import Complaint


class TestComplaint(TestCase):
    def test_empty(self):
        c = Complaint()
        f = c.create_pdf()
        self.assertTrue(os.path.isfile(f))
