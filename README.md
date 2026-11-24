# SocialAPI for Python

[![PyPI](https://img.shields.io/pypi/v/socialapihq.svg)](https://pypi.org/project/socialapihq/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

The official Python SDK for [SocialAPI](https://socialapi.sh): public social media data from TikTok, Instagram, Threads and Facebook, in one schema. Profiles, posts, comments, transcripts, searches and trends, with one API key.

Python 3.10+. [Docs](https://socialapi.sh/docs)

## Install

```sh
pip install socialapihq
```

## Use

Create an API key in the [dashboard](https://app.socialapi.sh). Every account gets 100 free credits.

```python
import os

from socialapihq import SocialAPI

client = SocialAPI(api_key=os.environ["SOCIALAPI_API_KEY"])

profile = client.tiktok.profile(handle="nike").data
print(profile.display_name, profile.followers)

page = client.instagram.profile_posts(handle="natgeo")
for post in page.data:
    print(post.url, post.stats.likes)
```

Each network is an attribute (`client.tiktok`, `client.instagram`, `client.threads`, `client.facebook`), each endpoint a method named after its path: `/v1/tiktok/post/comment/replies` is `client.tiktok.post_comment_replies()`. A method takes the endpoint's query parameters as keyword arguments, in snake case (`secUid` is `sec_uid`), and answers its body as a typed model: `.data` for one item, `.data` and `.pagination` for a list. Models are Pydantic: `.model_dump()` gives a dict, `.to_json()` the JSON.

`api_key` defaults to the `SOCIALAPI_API_KEY` environment variable.

### Pages

A list answers `pagination.next_cursor` while `pagination.has_more` is true. Pass it as `cursor`:

```python
cursor = None
while True:
    page = client.tiktok.profile_posts(handle="nike", cursor=cursor)
    for post in page.data:
        print(post.id)
    if not page.pagination.has_more:
        break
    cursor = page.pagination.next_cursor
```

Each page costs credits like any call; a cached answer is free.

### Errors

A refusal raises a `SocialAPIError`. Refusals cost no credits.

```python
from socialapihq import SocialAPIError

try:
    client.instagram.profile(handle="no-such-account")
except SocialAPIError as error:
    print(error.status, error.code, error.message)  # 404 NOT_FOUND …
```

`code` is stable to branch on: `NOT_FOUND`, `PRIVATE`, `INVALID_REQUEST`, `INSUFFICIENT_CREDITS`, `RATE_LIMITED` (with `retry_after`), `UPSTREAM_UNAVAILABLE`, `ENDPOINT_UNAVAILABLE`. Each error carries the `request_id` to quote to support.

### Options

```python
SocialAPI(
    api_key="sapi_…",
    base_url="https://api.socialapi.sh",  # the default
    timeout=30,  # seconds to wait for each answer
)
```

Use it as a context manager (`with SocialAPI() as client:`) to close its connections at the end. The generated API classes (`TikTokApi`, `InstagramApi`…), their `…_with_http_info` methods (the status and headers too, such as `X-Credits-Charged`) and every model are exported too.

## Endpoints

<!-- BEGIN GENERATED API REFERENCE -->

### Facebook

| Method | Endpoint | What it returns |
| --- | --- | --- |
| `client.facebook.event()` | `GET /v1/facebook/event` | An event: name, description, when, where, its host, how many are going, its tickets' link. 1 credit. |
| `client.facebook.events()` | `GET /v1/facebook/events` | A city's upcoming events, 12 a page. 1 credit a page. |
| `client.facebook.events_search()` | `GET /v1/facebook/events/search` | Events matching a query: two short pages, all Facebook shows a visitor. 1 credit a page. |
| `client.facebook.marketplace_item()` | `GET /v1/facebook/marketplace/item` | One Marketplace listing: title, description, price, condition, place, seller. 1 credit. |
| `client.facebook.marketplace_search()` | `GET /v1/facebook/marketplace/search` | Marketplace listings for a query around a point: title, price, place, seller, about 14, the first page Facebook shows a visitor. 1 credit. |
| `client.facebook.post()` | `GET /v1/facebook/post` | One post, reel or video: text, author, time, reactions by kind, comment and share counts, its media and the caption tracks it has. 1 credit. |
| `client.facebook.post_comment_replies()` | `GET /v1/facebook/post/comment/replies` | The replies to one comment, about 10 a page, named by its `ext.repliesToken`. 1 credit a page. |
| `client.facebook.post_comments()` | `GET /v1/facebook/post/comments` | A post's comments, most relevant first, with their reactions and how many replies, 10 a page. A comment with replies carries `ext.repliesToken` for `/v1/facebook/post/comment/replies`. 1 credit a page. |
| `client.facebook.post_transcript()` | `GET /v1/facebook/post/transcript` | A video's captions as text with their times: Facebook's own track, in the video's language where it lists one, else a translation (`translated` says so). `404` when the video has none. 5 credits. |
| `client.facebook.profile()` | `GET /v1/facebook/profile` | A page or a public person: name, category, bio, verified, follower count (as Facebook rounds it, "39M"), cover and the intro's lines (address, phone, links). 1 credit. |
| `client.facebook.profile_photos()` | `GET /v1/facebook/profile/photos` | A page's or person's photos, 8 a page. 1 credit a page. |
| `client.facebook.profile_posts()` | `GET /v1/facebook/profile/posts` | A page's or person's posts, newest first, with their reactions by kind, comments, shares and video views: 3 a page, as Facebook pages them. 1 credit a page. |
| `client.facebook.profile_videos()` | `GET /v1/facebook/profile/videos` | A page's videos with their plays and reactions, about 6 a page. Only a Page has one. 1 credit a page. |

### Instagram

| Method | Endpoint | What it returns |
| --- | --- | --- |
| `client.instagram.highlight()` | `GET /v1/instagram/highlight` | A story highlight's stories, each with its media and time. 1 credit. |
| `client.instagram.location()` | `GET /v1/instagram/location` | A place: its name, category, address, phone, coordinates and how many posts are tagged at it. 1 credit. |
| `client.instagram.location_posts()` | `GET /v1/instagram/location/posts` | A place's top posts with their likes, comments and times: the 18 Instagram shows a visitor, no more. 1 credit. |
| `client.instagram.post()` | `GET /v1/instagram/post` | One post or reel: caption, time, author, like and comment counts, its media, the place it was tagged at, the accounts tagged in it and the sound a reel uses. 1 credit. |
| `client.instagram.post_comments()` | `GET /v1/instagram/post/comments` | A post's comments with their likes, about 22 a page. Replies, and how many a comment has, are not shown to a visitor. 1 credit a page. |
| `client.instagram.profile()` | `GET /v1/instagram/profile` | A profile: name, bio and its links, verified, private, follower and following counts. Instagram does not show a visitor the post count, so `posts` is absent. 1 credit. |
| `client.instagram.profile_highlights()` | `GET /v1/instagram/profile/highlights` | An account's story highlights: their titles and covers, the first 10 (all Instagram shows a visitor; the profile's `ext.moreHighlights` says when there are more). 1 credit. |
| `client.instagram.profile_posts()` | `GET /v1/instagram/profile/posts` | An account's posts with their likes, comments, captions and times, newest first, 12 a page. 1 credit a page. |
| `client.instagram.profile_reels()` | `GET /v1/instagram/profile/reels` | An account's reels with their plays, likes and comments, 12 a page. Captions and times are not in this list; read a reel with `/v1/instagram/post`. 1 credit a page. |
| `client.instagram.profile_similar()` | `GET /v1/instagram/profile/similar` | Accounts like this one, as Instagram suggests them: up to 50, without their counts. Some accounts have none. 1 credit. |
| `client.instagram.search()` | `GET /v1/instagram/search` | Posts for a word or hashtag, as Instagram shows a visitor (its popular page): mostly reels with their plays, 12 a page, about 100 in all. Some words have no such page and answer an empty list. 1 credit a page. |
| `client.instagram.sound()` | `GET /v1/instagram/sound` | A sound: a song (title, artist, cover, length) or an account's original audio, and how many reels use it. 1 credit. |
| `client.instagram.sound_posts()` | `GET /v1/instagram/sound/posts` | The reels that use a sound, with their plays, likes, comments and times, 12 a page. 1 credit a page. |
| `client.instagram.trending()` | `GET /v1/instagram/trending` | The reels feed Instagram gives a visitor now, with likes, comments and times, 8 a page. 1 credit a page. |
| `client.instagram.trending_topics()` | `GET /v1/instagram/trending/topics` | The explore page: trending keywords with their post counts, categories, and accounts to look out for, by section. 1 credit. |

### Threads

| Method | Endpoint | What it returns |
| --- | --- | --- |
| `client.threads.post()` | `GET /v1/threads/post` | One thread: text, author, time, like, reply, repost, quote and share counts, media, the post it quotes or answers, a link's preview. Views are not shown to a visitor. 1 credit. |
| `client.threads.post_comments()` | `GET /v1/threads/post/comments` | A thread's replies, top or latest first: the first 15 or so, all Threads shows a visitor (no next page). 1 credit. |
| `client.threads.profile()` | `GET /v1/threads/profile` | A profile: name, bio and its links, its interests, verified, private and the follower count. 1 credit. |
| `client.threads.profile_media()` | `GET /v1/threads/profile/media` | An account's threads with photos or videos, 25 a page. 1 credit a page. |
| `client.threads.profile_posts()` | `GET /v1/threads/profile/posts` | An account's threads with their likes, replies, reposts, quotes and shares, newest first (pinned ones first of all), 25 a page. 1 credit a page. |
| `client.threads.profile_replies()` | `GET /v1/threads/profile/replies` | An account's replies to other threads, each with the post it answers (`ext.replyTo`), 25 a page. 1 credit a page. |
| `client.threads.profile_reposts()` | `GET /v1/threads/profile/reposts` | Other people's threads an account reposted, with when (`ext.repostedAt`). 1 credit a page. |
| `client.threads.search()` | `GET /v1/threads/search` | Threads matching a query, top or latest first: about 30 top or 20 latest, all Threads shows a visitor (no next page). 1 credit. |
| `client.threads.search_users()` | `GET /v1/threads/search/users` | Accounts matching a name: the first 10, without their counts. 1 credit. |
| `client.threads.trending()` | `GET /v1/threads/trending` | The feed Threads gives a visitor now: about 20 threads in all. 1 credit a page. |

### TikTok

| Method | Endpoint | What it returns |
| --- | --- | --- |
| `client.tiktok.collection_posts()` | `GET /v1/tiktok/collection/posts` | The posts of a public saved collection, 30 a page. 1 credit a page. |
| `client.tiktok.hashtag()` | `GET /v1/tiktok/hashtag` | A hashtag: its id, description, and post and view counts. 1 credit. |
| `client.tiktok.hashtag_posts()` | `GET /v1/tiktok/hashtag/posts` | Posts under a hashtag, 30 a page. 1 credit a page. |
| `client.tiktok.live()` | `GET /v1/tiktok/live` | A live room: whether the account is live, and the room's title, viewers and start (by its id, also how many entered and when it ended). Name the account, or the room with `roomId`. 1 credit. |
| `client.tiktok.playlist_posts()` | `GET /v1/tiktok/playlist/posts` | The posts of a playlist, 30 a page. 1 credit a page. |
| `client.tiktok.post()` | `GET /v1/tiktok/post` | One post: caption, author, view, like, comment, share and save counts and the engagement rate, media, sound, hashtags, the text on it, and the captions it has. 1 credit. |
| `client.tiktok.post_comment_replies()` | `GET /v1/tiktok/post/comment/replies` | The replies to one comment, 50 a page. 1 credit a page. |
| `client.tiktok.post_comments()` | `GET /v1/tiktok/post/comments` | A post's top-level comments, 50 a page. 1 credit a page. |
| `client.tiktok.post_related()` | `GET /v1/tiktok/post/related` | Posts TikTok recommends beside one post. 1 credit. |
| `client.tiktok.post_transcript()` | `GET /v1/tiktok/post/transcript` | A post's captions as text with their times: TikTok's own (generated or the author's), in the language asked for when it has it. `404` when the post has none. 5 credits. |
| `client.tiktok.profile()` | `GET /v1/tiktok/profile` | A profile: name, bio, link, verified, private, and exact follower, following, like and post counts. 1 credit. |
| `client.tiktok.profile_followers()` | `GET /v1/tiktok/profile/followers` | An account's followers, newest first, 30 a page. 1 credit a page. |
| `client.tiktok.profile_following()` | `GET /v1/tiktok/profile/following` | The accounts an account follows, when it shows them (`403 PRIVATE` when it hides them). 1 credit a page. |
| `client.tiktok.profile_liked()` | `GET /v1/tiktok/profile/liked` | Posts an account liked, when its likes are public (an empty list when they are not). 1 credit a page. |
| `client.tiktok.profile_playlists()` | `GET /v1/tiktok/profile/playlists` | The playlists an account made. 1 credit a page. |
| `client.tiktok.profile_posts()` | `GET /v1/tiktok/profile/posts` | An account's posts, newest first (pinned ones first of all), 30 a page. 1 credit a page. |
| `client.tiktok.profile_reposts()` | `GET /v1/tiktok/profile/reposts` | Other people's posts an account reposted. 1 credit a page. |
| `client.tiktok.search()` | `GET /v1/tiktok/search` | Posts matching a query, 30 a page. 1 credit a page. |
| `client.tiktok.search_users()` | `GET /v1/tiktok/search/users` | Accounts matching a query. 1 credit a page. |
| `client.tiktok.sound()` | `GET /v1/tiktok/sound` | A sound: title, artist, duration, how many posts use it. 1 credit. |
| `client.tiktok.sound_posts()` | `GET /v1/tiktok/sound/posts` | Posts that use a sound, 30 a page. 1 credit a page. |
| `client.tiktok.trending()` | `GET /v1/tiktok/trending` | What the explore page shows a guest now, for one of its categories (`all` by default): a fresh set of about 30 posts each time. 1 credit. |

### Account

| Method | Endpoint | What it returns |
| --- | --- | --- |
| `client.account.get_credits()` | `GET /v1/credits` | The credits left. Free, and not counted against the rate limit. |

<!-- END GENERATED API REFERENCE -->

## How this SDK is made

The client is generated from the API's OpenAPI document (`https://api.socialapi.sh/openapi.json`) by [OpenAPI Generator](https://openapi-generator.tech) and `scripts/generate_client.py` (`src/socialapihq/client.py`). Each API release regenerates, tests and publishes it. Please open issues here; changes to `src/` are overwritten.

## License

Apache-2.0
