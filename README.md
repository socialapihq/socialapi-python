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

### Bluesky

| Method | Description |
| --- | --- |
| `bluesky.batch_posts()` | Up to 25 posts at once |
| `bluesky.batch_profiles()` | Up to 25 accounts at once |
| `bluesky.feed()` | A feed with its description and likes |
| `bluesky.feed_posts()` | A feed's posts |
| `bluesky.hashtag_posts()` | A hashtag's posts |
| `bluesky.list()` | A list with its purpose and member count |
| `bluesky.list_members()` | A list's accounts |
| `bluesky.list_posts()` | The posts of a list's accounts |
| `bluesky.post()` | One post with its likes |
| `bluesky.post_comments()` | A post's replies |
| `bluesky.post_likes()` | The accounts that liked a post |
| `bluesky.post_quotes()` | The posts quoting a post |
| `bluesky.post_reposts()` | The accounts that reposted a post |
| `bluesky.profile()` | An account with its follower and post counts |
| `bluesky.profile_feeds()` | The feeds an account made |
| `bluesky.profile_followers()` | The accounts following an account |
| `bluesky.profile_following()` | The accounts an account follows |
| `bluesky.profile_lists()` | The lists an account made |
| `bluesky.profile_media()` | An account's posts with images or video |
| `bluesky.profile_posts()` | An account's posts and reposts |
| `bluesky.profile_replies()` | An account's posts with its replies |
| `bluesky.profile_starter_packs()` | The starter packs an account made |
| `bluesky.profile_videos()` | An account's posts with video |
| `bluesky.search()` | Posts matching a query |
| `bluesky.search_feeds()` | Feeds matching a query |
| `bluesky.search_starter_packs()` | Starter packs matching a query |
| `bluesky.search_users()` | Accounts matching a query |
| `bluesky.starter_pack()` | A starter pack with its accounts' list and feeds |
| `bluesky.trending()` | The posts of Bluesky's Discover feed |
| `bluesky.trending_topics()` | The topics trending now |

### Douyin

| Method | Description |
| --- | --- |
| `douyin.hashtag()` | A hashtag with its views |
| `douyin.live()` | A live room |
| `douyin.playlist_posts()` | A series' posts |
| `douyin.post()` | One post with its likes |
| `douyin.post_comment_replies()` | A comment's replies |
| `douyin.post_comments()` | A post's comments |
| `douyin.post_related()` | Posts like a post |
| `douyin.profile()` | An account with its followers |
| `douyin.profile_playlists()` | An account's series |
| `douyin.profile_posts()` | An account's latest posts |
| `douyin.search_suggestions()` | What Douyin's search box suggests for a query |
| `douyin.sound()` | A sound with the number of posts using it |
| `douyin.sound_posts()` | Posts using a sound |
| `douyin.trending()` | Douyin's hot search list |
| `douyin.trending_posts()` | Recommended posts |

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

### Kick

| Method | Description |
| --- | --- |
| `kick.category()` | A category with its viewers and followers |
| `kick.category_clips()` | A category's clips |
| `kick.category_lives()` | A category's live broadcasts |
| `kick.live()` | Whether a channel is live |
| `kick.post()` | One video or clip with its views and a link to play it |
| `kick.post_comments()` | A video's chat replay |
| `kick.post_transcript()` | A video's or clip's captions as text |
| `kick.profile()` | A channel with its follower count and links |
| `kick.profile_clips()` | A channel's clips |
| `kick.profile_posts()` | A channel's videos |
| `kick.search_categories()` | Categories matching a search |
| `kick.search_lives()` | Live broadcasts matching a search |
| `kick.search_users()` | Channels matching a search |
| `kick.trending()` | The live broadcasts most watched now |
| `kick.trending_categories()` | The categories most watched now |
| `kick.trending_clips()` | The site's most viewed clips |

### LinkedIn

| Method | Description |
| --- | --- |
| `linkedin.ad()` | One ad with who paid for it and its reach |
| `linkedin.ads_search()` | Ads from LinkedIn's Ad Library |
| `linkedin.article()` | An article with its text |
| `linkedin.company()` | A company's page with its followers and employees |
| `linkedin.company_jobs()` | A company's open jobs |
| `linkedin.company_posts()` | A company's posts |
| `linkedin.job()` | One job posting with its description |
| `linkedin.post()` | One post with its reactions and comments |
| `linkedin.post_comments()` | A post's first comments |
| `linkedin.post_transcript()` | A post's video's captions as text |
| `linkedin.profile()` | A member's public profile with its followers |
| `linkedin.profile_articles()` | A member's articles |
| `linkedin.profile_posts()` | A member's latest posts |
| `linkedin.search_jobs()` | Job postings for a search |
| `linkedin.search_users()` | Members with a first and last name |

### Pinterest

| Method | Description |
| --- | --- |
| `pinterest.board()` | A board with its pin and follower counts |
| `pinterest.board_posts()` | A board's pins |
| `pinterest.board_section_posts()` | A board section's pins |
| `pinterest.board_sections()` | A board's sections with their pin counts |
| `pinterest.post()` | One pin with its saves |
| `pinterest.post_comment_replies()` | A comment's replies |
| `pinterest.post_comments()` | A pin's comments |
| `pinterest.profile()` | A profile with its follower and pin counts |
| `pinterest.profile_boards()` | An account's boards |
| `pinterest.profile_posts()` | The pins an account created |
| `pinterest.search()` | Pins matching a query |
| `pinterest.search_boards()` | Boards matching a query |
| `pinterest.search_suggestions()` | What the search box suggests for a few letters |
| `pinterest.search_users()` | Accounts matching a query |
| `pinterest.search_videos()` | Video pins matching a query |
| `pinterest.topic()` | A topic's Ideas page with its followers and searches |
| `pinterest.topic_posts()` | A topic's top pins |
| `pinterest.trending()` | What a country searches for on Pinterest Trends |
| `pinterest.url()` | How many times a web page was saved to Pinterest |

### Reddit

| Method | Description |
| --- | --- |
| `reddit.post()` | One post with its score |
| `reddit.post_comment_replies()` | A comment's replies |
| `reddit.post_comments()` | A post's comments with their replies |
| `reddit.post_transcript()` | A video post's captions as text |
| `reddit.profile()` | A profile with its karma and trophies |
| `reddit.profile_comments()` | An account's comments |
| `reddit.profile_posts()` | An account's posts |
| `reddit.search()` | Posts matching a query across Reddit |
| `reddit.search_comments()` | Comments matching a query across Reddit |
| `reddit.search_media()` | Image and video posts matching a query |
| `reddit.search_subreddits()` | Communities matching a query |
| `reddit.search_users()` | Accounts matching a name |
| `reddit.subreddit()` | A community with its members |
| `reddit.subreddit_posts()` | A community's posts |
| `reddit.subreddit_search()` | Posts in one community matching a query |
| `reddit.trending()` | What is hot on Reddit now |
| `reddit.trending_searches()` | The searches Reddit shows as trending now |

### Telegram

| Method | Description |
| --- | --- |
| `telegram.invite()` | What an invite link opens |
| `telegram.post()` | One channel post or group message |
| `telegram.post_comments()` | A post's comments |
| `telegram.profile()` | A channel |
| `telegram.profile_posts()` | A channel's posts |
| `telegram.profile_search()` | A search inside a channel |

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

### Twitch

| Method | Description |
| --- | --- |
| `twitch.batch_live()` | Up to 100 channels' live status at once |
| `twitch.batch_profiles()` | Up to 50 channels at once |
| `twitch.category()` | A category with its viewers |
| `twitch.category_clips()` | A category's clips |
| `twitch.category_lives()` | A category's live channels |
| `twitch.category_posts()` | A category's videos |
| `twitch.live()` | Whether a channel is live |
| `twitch.post()` | One video or clip with its views and a link to play it |
| `twitch.post_comments()` | A video's chat replay |
| `twitch.profile()` | A channel with its follower count and links |
| `twitch.profile_clips()` | A channel's clips |
| `twitch.profile_posts()` | A channel's videos |
| `twitch.profile_schedule()` | A channel's coming broadcasts |
| `twitch.search()` | Videos matching a query |
| `twitch.search_categories()` | Categories matching a query |
| `twitch.search_lives()` | Live channels matching a query |
| `twitch.search_suggestions()` | What the search box suggests for a few letters |
| `twitch.search_users()` | Channels matching a query |
| `twitch.trending()` | The live channels most watched now |
| `twitch.trending_categories()` | The categories most watched now |

### X

| Method | Description |
| --- | --- |
| `x.community()` | A community with its members |
| `x.community_posts()` | A community's top posts |
| `x.live()` | A live video broadcast |
| `x.post()` | One post with its views |
| `x.post_comments()` | The top replies to a post |
| `x.post_transcript()` | A video post's captions as text |
| `x.profile()` | An account with its follower and post counts |
| `x.profile_highlights()` | The posts an account highlighted |
| `x.profile_posts()` | An account's posts and reposts |
| `x.profile_similar()` | Accounts like one |
| `x.space()` | A Space with its hosts |
| `x.trending()` | The topics trending in a country |
| `x.trending_posts()` | The posts trending on X today |

### YouTube

| Method | Description |
| --- | --- |
| `youtube.batch_posts()` | Up to 50 videos at once |
| `youtube.batch_profiles()` | Up to 20 channels at once |
| `youtube.batch_transcripts()` | Up to 20 videos' captions at once |
| `youtube.community()` | One community post with its likes and images |
| `youtube.hashtag()` | A hashtag with its video and channel counts |
| `youtube.hashtag_posts()` | A hashtag's videos or Shorts |
| `youtube.playlist()` | A playlist with its owner and video count |
| `youtube.playlist_posts()` | A playlist's videos in order |
| `youtube.post()` | One video or Short with its views |
| `youtube.post_comment_replies()` | A comment's replies |
| `youtube.post_comments()` | A video's comments |
| `youtube.post_related()` | The videos YouTube suggests beside one |
| `youtube.post_transcript()` | A video's captions as text |
| `youtube.profile()` | A channel with its subscribers |
| `youtube.profile_community()` | A channel's community posts |
| `youtube.profile_lives()` | A channel's live streams |
| `youtube.profile_playlists()` | A channel's playlists |
| `youtube.profile_podcasts()` | A channel's podcasts |
| `youtube.profile_posts()` | A channel's videos |
| `youtube.profile_search()` | A search within one channel's videos |
| `youtube.profile_shorts()` | A channel's Shorts |
| `youtube.search()` | Videos matching a query |
| `youtube.search_channels()` | Channels matching a query |
| `youtube.search_playlists()` | Playlists matching a query |
| `youtube.search_suggestions()` | What the search box suggests for a few letters |
| `youtube.trending()` | What is trending in a country |

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
