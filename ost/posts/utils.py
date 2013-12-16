from bs4 import BeautifulSoup


def wrap_plain(posts):
    for post in posts:
        post.plain = BeautifulSoup(post.content).get_text()


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
