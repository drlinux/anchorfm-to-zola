from config import feed_url, content_path
from anchorfm import AnchorFmFetcher

a = AnchorFmFetcher()
metadata = a.metadata_generator(feed_url)
posts = a.podcast_fetcher(feed_url)

for post in posts:
    a.post_generator(metadata=metadata, post=post, content_path=content_path)
print('Done')
