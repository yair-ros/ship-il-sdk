from ship_il_sdk.models.shipments import LabelResponse
from ship_il_sdk.token_manager import TokenManager


def test_label_response_decodes_bytes():
    label = LabelResponse(
        MediaType="application/pdf",
        FileByteArray="aGVsbG8=",
        FileName="label.pdf",
    )

    assert label.file_bytes() == b"hello"


def test_token_manager_refreshes_before_hard_expiry():
    tokens = TokenManager(refresh_margin=60)
    tokens.set_token("secret", ttl=30)

    assert tokens.is_expired() is True
