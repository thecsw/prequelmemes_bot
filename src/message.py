"""
Defines messages
"""

MESSAGE = """
**Hello there!**

The line "*%CITATION%*" is from **"%MOVIE%"**.

The ~~fun~~ line begins at %START% and finishes at %END%.

This line has been referenced %NUMBER% time(s).
"""

def modify_message(quote, movie, start, end, times):
    """
    Modifies the message
    """
    return MESSAGE.\
        replace("%CITATION%", quote).\
        replace("%START%", start).\
        replace("%END%", end).\
        replace("%MOVIE%", movie).\
        replace("%NUMBER%", str(times))
