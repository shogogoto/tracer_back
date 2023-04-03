import pytest
from . import path as P


def test_convert():
    assert P.convert(None)     == ""
    assert P.convert(1)        == "1"
    assert P.convert((1,3))    == "1..3"
    assert P.convert((None,5)) == "..5"
    assert P.convert((5,None)) == "5.."
    assert P.convert((5,))     == "5.."
    with pytest.raises(TypeError):
        P.convert((1,2,3))
    with pytest.raises(TypeError):
        P.convert(())
