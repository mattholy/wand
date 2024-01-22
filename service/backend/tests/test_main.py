# -*- encoding: utf-8 -*-
'''
test_main.py
----
testing


@Time    :   2024/01/22 12:57:51
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from fastapi.testclient import TestClient

from ..app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
