from .netcook import checked_cookies

__all__ = ['checked_cookies']

def inject_checked_cookies():
    globals()['checked_cookies'] = checked_cookies

inject_checked_cookies()

