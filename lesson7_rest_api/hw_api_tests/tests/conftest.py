import pytest

def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="https://ya.ru", help="url для проверки")
    parser.addoption("--status_code", action="store", default="200", help="ожидаемый статус-код")