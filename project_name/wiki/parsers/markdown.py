from markdown import Markdown


def parse(text):
    md = Markdown(extensions=["codehilite"])
    html = md.convert(text)
    return html
