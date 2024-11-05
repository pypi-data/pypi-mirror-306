from conftest import vcr_c  # noqa

from whitebit_httpx_client import WhiteBITClient


@vcr_c.use_cassette("fee/test_get_fee.yaml")
def test_get_fee(white_bit_client: WhiteBITClient):
    fee = white_bit_client.get_fee_data()
    assert isinstance(fee, dict)
    assert len(fee) > 100


@vcr_c.use_cassette("fee/test_get_fee.yaml")
async def test_async_get_fee(white_bit_client: WhiteBITClient):
    fee = await white_bit_client.async_get_fee_data()
    assert isinstance(fee, dict)
    assert len(fee) > 100
