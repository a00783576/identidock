#!/usr/bin/env python
import unittest
import identidock

class TestCase(unittest.TestCase):
    """ This is one of potentially many TestCases """

    def setUp(self):
        app = identidock.create_app()
        app.debug = True
        self.app = app.test_client()

    def test_get_mainpage(self):
        page = self.app.post("/", data=dict(name="Arturo Blogs"))
        assert page.status_code == 200
        assert 'Hello' in str(page.data)
        assert '' in str(page.data)

    def test_html_escaping(self):
        page = self.app.post("/", data=dict(name='"><b>TEST</b><!--'))
        assert'<b>'not in str(page.data)

    def test_route_hello_world(self):
        page = self.app.get("/hello")
        # print(dir(res), res.status_code)
        assert page.status_code == 200
        assert b"Hello World" in page.data

    def test_route_foo(self):
        page = self.app.get("/foo/12345")
        assert page.status_code == 200
        assert b"12345" in page.data

if __name__ == '__main__':
    unittest.main()
