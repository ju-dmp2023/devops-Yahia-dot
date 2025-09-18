from test.web.test_base import WebBase
from test.web.pages.login_page import LoginPage
from test.web.pages.calculator_page import CalculatorPage
from playwright.sync_api import expect
import pytest

class TestWeb(WebBase):
    def test_login(self):
        LoginPage(self.page).login(username="admin", password="test1234")
        expect(CalculatorPage(self.page).element("username")).to_have_text("admin")
        