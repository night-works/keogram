from keogram import coverage_method


def test_coverage():
    value = coverage_method()
    assert value == 10
