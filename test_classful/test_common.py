from flask import Flask
from .view_classes import BasicView, IndexView
from nose.tools import eq_

app = Flask("common")
BasicView.register(app)
IndexView.register(app)

client = app.test_client()


def test_index():
    resp = client.get("/basic/")
    eq_(b"Index", resp.data)


def test_get():
    resp = client.get("/basic/1234/")
    eq_(resp.status_code, 404)
    eq_(b"Get 1234", resp.data)
    resp = client.get("/basic/1234")
    eq_(resp.status_code, 308)


def test_put():
    resp = client.put("/basic/1234/")
    eq_(resp.status_code, 403)
    eq_(resp.headers['say'], 'hello')
    eq_(b"Put 1234", resp.data)
    resp = client.put("/basic/1234")
    eq_(resp.status_code, 308)


def test_patch():
    resp = client.patch("/basic/1234/")
    eq_(b"Patch 1234", resp.data)
    resp = client.patch("/basic/1234")
    eq_(resp.status_code, 308)


def test_post():
    resp = client.post("/basic/")
    eq_(b"Post", resp.data)
    resp = client.post("/basic")
    eq_(resp.status_code, 308)


def test_delete():
    resp = client.delete("/basic/1234/")
    eq_(b"Delete 1234", resp.data)
    resp = client.delete("/basic/1234")
    eq_(resp.status_code, 308)


def test_custom_method():
    resp = client.get("/basic/custom_method/")
    eq_(b"Custom Method", resp.data)
    resp = client.get("/basic/custom_method")
    eq_(resp.status_code, 308)


def test_custom_method_with_params():
    resp = client.get("/basic/custom_method_with_params/1234/abcd/")
    eq_(b"Custom Method 1234 abcd", resp.data)
    resp = client.get("/basic/custom_method_with_params/1234/abcd")
    eq_(resp.status_code, 308)


def test_routed_method():
    resp = client.get("/basic/routed/")
    eq_(b"Routed Method", resp.data)
    resp = client.get("/basic/routed")
    eq_(resp.status_code, 308)


def test_multi_routed_method():
    resp = client.get("/basic/route1/")
    eq_(b"Multi Routed Method", resp.data)
    resp = client.get("/basic/route1")
    eq_(resp.status_code, 308)

    resp = client.get("/basic/route2/")
    eq_(b"Multi Routed Method", resp.data)
    resp = client.get("/basic/route2")
    eq_(resp.status_code, 308)


def test_no_slash():
    resp = client.get("/basic/noslash")
    eq_(b"No Slash Method", resp.data)
    resp = client.get("/basic/noslash/") # matches get(id)
    eq_(b"Get noslash", resp.data)


def test_index_view_index():
    resp = client.get("/")
    eq_(b"Index", resp.data)
    resp = client.get("")
    eq_(resp.status_code, 308)


def test_custom_http_method():
    resp = client.post("/basic/route3/")
    eq_(b"Custom HTTP Method", resp.data)
    resp = client.post("/basic/route3")
    eq_(resp.status_code, 308)


def test_docstrings():
    proxy_func = app.view_functions["BasicView:index"]
    eq_(proxy_func.__doc__, BasicView.index.__doc__)
