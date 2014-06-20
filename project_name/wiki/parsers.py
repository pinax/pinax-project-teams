import creole

from creole.html_emitter import HtmlEmitter


def creole_parse(text):
    return HtmlEmitter(creole.Parser(text).parse()).emit()


def creole_wikiword_parse(text):
    rules = creole.Rules(wiki_words=True)
    return HtmlEmitter(creole.Parser(text, rules).parse()).emit()
