import pytest
from nano_manus.worker.type import BaseWorker


def test_init():
    with pytest.raises(TypeError):
        BaseWorker()
