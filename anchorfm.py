from datetime import datetime
from urllib.request import urlopen
from slugify import slugify
from lxml import html
import os
import podcastparser


class AnchorFmFetcher:

    @staticmethod
    def metadata_generator(feed_url: str) -> dict:
        """
        Generate metadata from the podcast feed.

        Args:
            feed_url (str): The URL of the podcast feed.

        Returns:
            dict: Dictionary containing the metadata.
        """
        try:
            feed = podcastparser.parse(feed_url, urlopen(feed_url))
            metadata = {
                'title': feed['title'],
                'author': feed['itunes_author'],
                'language': feed.get('language', 'tr')
            }
        except Exception as e:
            print(f"Error generating metadata: {str(e)}")
            metadata = {}
        return metadata

    @staticmethod
    def podcast_fetcher(feed_url: str) -> list:
        """
        Fetch podcast episodes from the feed.

        Args:
            feed_url (str): The URL of the podcast feed.

        Returns:
            list: List of dictionaries representing the podcast episodes.
        """
        posts = []
        try:
            for podcast in podcastparser.parse(feed_url, urlopen(feed_url))['episodes']:
                post = {
                    'title': podcast['title'],
                    'published': datetime.fromtimestamp(int(podcast['published'])).strftime('%Y-%m-%d'),
                    'slug': slugify(podcast['title']),
                    'content': podcast['description_html'],
                    'audio': podcast['enclosures'][0]['url'],
                    'cover_image': podcast.get('episode_art_url', '')
                }
                posts.append(post)
        except Exception as e:
            print(f"Error fetching podcast episodes: {str(e)}")
        return posts

    @staticmethod
    def post_generator(metadata: dict, post: dict, content_path: str) -> bool:
        """
        Generate a post file from a template.

        Args:
            metadata (dict): Dictionary containing the metadata.
            post (dict): Dictionary representing a podcast episode.

        Returns:
            bool: True if the post file was successfully generated, False otherwise.
        """
        try:
            with open("templates/markdown-template.txt", "rt") as fin:
                contents = fin.read()
                title = post['title'].replace('"', '').replace('“', '').replace('”', '')
                content = str(html.fromstring(post['content']).text_content()).replace('’', '')
                new_post = contents.replace('_TITLE_', title)\
                                  .replace('_DATE_', post['published'])\
                                  .replace('_SLUG_', post['slug'])\
                                  .replace('_AUTHOR_', metadata['author'])\
                                  .replace('_CONTENT_', content)\
                                  .replace('_EPCOVER_', post['cover_image'])\
                                  .replace('_AUDIO_URL_', post['audio'])
                if not os.path.exists(f'{content_path}'):
                    os.makedirs(f'{content_path}')
                with open(f"{content_path}{post['slug']}.md", "wt") as fout:
                    fout.write(new_post)
            return True
        except Exception as e:
            print(f"Error generating post file: {str(e)}")
            return False
