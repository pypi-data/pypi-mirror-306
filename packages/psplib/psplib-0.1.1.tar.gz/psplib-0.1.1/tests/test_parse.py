import pytest

from psplib import parse
from tests.utils import relative


@pytest.mark.parametrize(
    "loc, instance_format",
    [
        ("data/Jall1_1.mm", "psplib"),
        ("data/RG300_1.rcp", "patterson"),
        ("data/MPLIB1_Set1_0.rcmp", "mplib"),
    ],
)
def test_parse(loc, instance_format):
    """
    Checks that the instances are successfully parsed.
    """
    parse(relative(loc), instance_format)
