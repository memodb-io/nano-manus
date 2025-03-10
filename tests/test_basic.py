import pytest
from nano_manus.types import BaseAgent


def test_init():
    with pytest.raises(TypeError):
        BaseAgent()
