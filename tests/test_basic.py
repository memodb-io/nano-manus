import pytest
from angent.types import BaseAgent


def test_init():
    with pytest.raises(TypeError):
        BaseAgent()
