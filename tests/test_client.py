"""The client against a stubbed connection: no network."""

import pytest
from stub import stubbed

from socialapihq import SocialAPI, SocialAPIError

PROFILE = {
    "data": {
        "id": "15948",
        "username": "nike",
        "displayName": "Nike",
        "url": "https://www.tiktok.com/@nike",
        "verified": True,
        "private": False,
        "followers": 9440721,
        "ext": {"secUid": "MS4wLjABAAAA", "seller": False, "likesPublic": False},
    }
}


def test_sends_the_query_and_the_key_and_answers_the_model():
    client, requests = stubbed(200, PROFILE)
    profile = client.tiktok.profile(handle="nike").data
    assert profile.username == "nike"
    assert profile.private is False
    assert profile.followers == 9440721
    method, url, headers = requests[0]
    assert (method, url) == ("GET", "https://api.socialapi.sh/v1/tiktok/profile?handle=nike")
    assert headers["Authorization"] == "Bearer sapi_test"


def test_names_parameters_in_python():
    client, requests = stubbed(200, PROFILE)
    client.tiktok.profile(sec_uid="MS4w", max_age=0)
    assert requests[0][1] == "https://api.socialapi.sh/v1/tiktok/profile?secUid=MS4w&maxAge=0"


def test_takes_another_base_url():
    client, requests = stubbed(200, {"balance": 2500}, base_url="http://localhost:8787/")
    assert client.account.get_credits().balance == 2500
    assert requests[0][1] == "http://localhost:8787/v1/credits"


def test_turns_a_refusal_into_a_social_api_error():
    client, _ = stubbed(
        404,
        {"error": "No TikTok account matches this handle.", "code": "NOT_FOUND"},
        {"x-request-id": "req_1"},
    )
    with pytest.raises(SocialAPIError) as caught:
        client.tiktok.profile(handle="nobody")
    error = caught.value
    assert (error.status, error.code, error.request_id) == (404, "NOT_FOUND", "req_1")
    assert str(error) == "No TikTok account matches this handle."


def test_says_when_to_retry():
    client, _ = stubbed(429, {"error": "Too many requests.", "code": "RATE_LIMITED"}, {"retry-after": "7"})
    with pytest.raises(SocialAPIError) as caught:
        client.account.get_credits()
    assert (caught.value.status, caught.value.code, caught.value.retry_after) == (429, "RATE_LIMITED", 7)


def test_reads_the_key_from_the_environment(monkeypatch):
    monkeypatch.setenv("SOCIALAPI_API_KEY", "sapi_env")
    assert SocialAPI()._client.configuration.access_token == "sapi_env"  # noqa: SLF001


def test_refuses_to_start_without_a_key(monkeypatch):
    monkeypatch.delenv("SOCIALAPI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="API key"):
        SocialAPI()
