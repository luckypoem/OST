from bs4 import BeautifulSoup
import re


def wrap_plain(posts):
    for post in posts:
        plain = BeautifulSoup(post.content).get_text()
        post.plain = re.sub(r'\n+', '\n\n', plain)  # Collapse multi-lines


def wrap_tags(post):
    """Wrap Taggit tags of a post with blog information"""
    tags = []
    for tag in post.tags.all():
        t = {
            'slug': tag.slug,
            'blog': post.blog.slug,
        }
        tags.append(t)
    post.wrapped_tags = tags
