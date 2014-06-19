from markdown import Markdown


def markdown_parse(text):
    md = Markdown(extensions=["codehilite"])
    html = md.convert(text)
    return html
