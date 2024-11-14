import pandas as pd
import pytest

from virtualize_nex_gddp_cmip6.inventory import get_inventory, get_uris


@pytest.mark.parametrize("version,expected", [("1.0", 116129), ("1.1", 36165), ("1.2", 9288)])
def test_get_inventory(version, expected):
    df = get_inventory(version=version)
    assert isinstance(df, pd.DataFrame)
    assert len(df == expected)


def test_uris():
    df = get_uris()
    assert isinstance(df, pd.DataFrame)
    assert len(df == 116129)
