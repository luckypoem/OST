def is_follower(user, blog):
    if user in blog.followers.all():
        return True
    return False
