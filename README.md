<p align="center">
  <a href="https://socialapi.sh">
    <img src="https://socialapi.sh/og.png" alt="SocialAPI: public social media data in one schema" width="640">
  </a>
</p>

<p align="center">
  <a href="https://pypi.org/project/socialapihq/"><img src="https://img.shields.io/pypi/v/socialapihq.svg" alt="PyPI version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License"></a>
</p>

<p align="center">
  Official Python SDK for the <a href="https://socialapi.sh">SocialAPI</a>: profiles, posts, comments, transcripts,<br>
  searches and trends from TikTok, Instagram, Threads and Facebook, in one schema. See the <a href="https://socialapi.sh/docs">docs</a> for every endpoint.
</p>

<p align="center">
  Python 3.10+. Typed with Pydantic.
</p>

## Installation

```sh
pip install socialapihq
```

## Usage

Each platform is an attribute of the client and each endpoint a method on it. Create an API key in the [dashboard](https://app.socialapi.sh); it is sent as `Authorization: Bearer sapi_…`, and every account starts with 100 free credits.

```python
import os

from socialapihq import SocialAPI

client = SocialAPI(api_key=os.environ["SOCIALAPI_API_KEY"])

profile = client.tiktok.profile(handle="nike").data
print(profile.display_name, profile.followers)  # Nike 9440793

for post in client.instagram.profile_posts(handle="natgeo").data:
    print(post.url, post.stats.likes)
```

Methods take the endpoint's parameters as keyword arguments in snake case (`secUid` is `sec_uid`) and return typed models: `.data` for one item, `.data` and `.pagination` for a list. Every platform answers with the same field names, and what only one platform has sits under `ext`. `api_key` defaults to the `SOCIALAPI_API_KEY` environment variable.

Models are Pydantic: `.model_dump()` gives a dict, `.to_json()` the JSON.

### Pagination

A list answers `pagination.next_cursor` while `pagination.has_more` is true. Pass it back as `cursor` for the next page:

```python
cursor = None
while True:
    page = client.tiktok.profile_posts(handle="nike", cursor=cursor)
    for post in page.data:
        print(post.id, post.stats.views)
    if not page.pagination.has_more:
        break
    cursor = page.pagination.next_cursor
```

Each page costs credits like any call. A cached answer is free.

### Transcripts

```python
transcript = client.tiktok.post_transcript(
    url="https://www.tiktok.com/@nike/video/7711414040114892045",
).data

print(transcript.language, transcript.text)
for cue in transcript.cues:
    print(cue.start_seconds, cue.text)  # 0.02 Pole or podium?
```

A transcript costs 5 credits and is cached for 30 days.

### Error handling

A refused call raises a `SocialAPIError`. Its `code` is stable to build logic on, and refused calls cost no credits:

```python
from socialapihq import SocialAPIError

try:
    client.instagram.profile(handle="no-such-account")
except SocialAPIError as error:
    print(error.status, error.code, error.message, error.request_id)
    # 404 NOT_FOUND No Instagram account matches this handle. req_…
```

`RATE_LIMITED` errors carry `retry_after` in seconds. See [Errors](https://socialapi.sh/docs/errors) for every code.

### Configuration

```python
client = SocialAPI(
    api_key="sapi_…",
    base_url="https://api.socialapi.sh",  # the default
    timeout=30,  # seconds to wait for each answer
)

with SocialAPI() as client:  # closes its connections at the end
    print(client.account.get_credits().balance)
```

The generated classes (`TikTokApi`, `InstagramApi`…) are exported too. Their `…_with_http_info` methods give the status and headers, such as `X-Credits-Charged`.

## API reference

<!-- BEGIN GENERATED API REFERENCE -->

### Facebook

| Method | Description |
| --- | --- |
| `facebook.event()` | One event |
| `facebook.events()` | A city's upcoming events |
| `facebook.events_search()` | Events matching a query |
| `facebook.marketplace_item()` | One Marketplace listing |
| `facebook.marketplace_search()` | Marketplace listings for a query near a point |
| `facebook.post()` | One post |
| `facebook.post_comment_replies()` | The replies to one comment |
| `facebook.post_comments()` | A post's comments |
| `facebook.post_transcript()` | A video's captions as text with their times |
| `facebook.profile()` | A Page or a public person |
| `facebook.profile_photos()` | A Page's or person's photos |
| `facebook.profile_posts()` | A Page's or person's posts |
| `facebook.profile_videos()` | A Page's videos with their plays |

### Instagram

| Method | Description |
| --- | --- |
| `instagram.highlight()` | A story highlight's stories |
| `instagram.location()` | A place |
| `instagram.location_posts()` | A place's top posts with their likes and comments |
| `instagram.post()` | One post or reel with its counts |
| `instagram.post_comments()` | A post's comments with their likes |
| `instagram.profile()` | A profile with its follower and following counts |
| `instagram.profile_highlights()` | An account's story highlights |
| `instagram.profile_posts()` | An account's posts |
| `instagram.profile_reels()` | An account's reels with their plays |
| `instagram.profile_similar()` | Accounts like this one |
| `instagram.search()` | Popular posts for a word or hashtag |
| `instagram.sound()` | A sound |
| `instagram.sound_posts()` | The reels that use a sound |
| `instagram.trending()` | The reels feed Instagram gives a visitor |
| `instagram.trending_topics()` | The explore page's trending keywords and accounts |

### Threads

| Method | Description |
| --- | --- |
| `threads.post()` | One thread with its counts |
| `threads.post_comments()` | A thread's replies |
| `threads.profile()` | A profile with its follower count |
| `threads.profile_media()` | An account's threads with photos or videos |
| `threads.profile_posts()` | An account's threads |
| `threads.profile_replies()` | An account's replies to other threads |
| `threads.profile_reposts()` | Other people's threads an account reposted |
| `threads.search()` | Threads matching a query |
| `threads.search_users()` | Accounts matching a name |
| `threads.trending()` | The feed Threads gives a visitor now |

### TikTok

| Method | Description |
| --- | --- |
| `tiktok.collection_posts()` | The posts of a public saved collection |
| `tiktok.hashtag()` | A hashtag with its post and view counts |
| `tiktok.hashtag_posts()` | Posts under a hashtag |
| `tiktok.live()` | Whether an account is live |
| `tiktok.playlist_posts()` | The posts of a playlist |
| `tiktok.post()` | One post with its counts |
| `tiktok.post_comment_replies()` | The replies to one comment |
| `tiktok.post_comments()` | A post's top-level comments |
| `tiktok.post_related()` | Posts TikTok recommends beside one post |
| `tiktok.post_transcript()` | A post's captions as text with their times |
| `tiktok.profile()` | A profile with its exact follower and like counts |
| `tiktok.profile_followers()` | An account's followers |
| `tiktok.profile_following()` | The accounts an account follows |
| `tiktok.profile_liked()` | Posts an account liked |
| `tiktok.profile_playlists()` | The playlists an account made |
| `tiktok.profile_posts()` | An account's posts |
| `tiktok.profile_reposts()` | Other people's posts an account reposted |
| `tiktok.search()` | Posts matching a query |
| `tiktok.search_users()` | Accounts matching a query |
| `tiktok.sound()` | A sound |
| `tiktok.sound_posts()` | Posts that use a sound |
| `tiktok.trending()` | What the explore page shows now |

### Account

| Method | Description |
| --- | --- |
| `account.get_credits()` | The credits left in your workspace |

<!-- END GENERATED API REFERENCE -->

Query parameters are keyword arguments of the method, such as `handle="nike", cursor=cursor`. Every endpoint, with its parameters and a real answer, is in the [API Reference](https://socialapi.sh/docs/api-reference).

## Links

- [Documentation](https://socialapi.sh/docs)
- [API Reference](https://socialapi.sh/docs/api-reference)
- [Dashboard](https://app.socialapi.sh)
- [OpenAPI spec](https://api.socialapi.sh/openapi.json)

## License

Apache-2.0
