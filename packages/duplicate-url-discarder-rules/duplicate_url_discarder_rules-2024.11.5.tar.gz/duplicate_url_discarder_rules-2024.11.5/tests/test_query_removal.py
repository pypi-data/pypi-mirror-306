from duplicate_url_discarder.processors import QueryRemovalProcessor
from duplicate_url_discarder.url_canonicalizer import UrlCanonicalizer

from duplicate_url_discarder_rules import RULE_PATHS


def test_query_removal_product_rules():
    assert RULE_PATHS is not None
    rule_path = [
        path for path in RULE_PATHS if path.endswith("queryRemoval/product.json")
    ]
    assert len(rule_path) == 1

    canonicalizer = UrlCanonicalizer(rule_path)

    assert len(canonicalizer.processors) > 0
    assert isinstance(list(canonicalizer.processors.values())[0], QueryRemovalProcessor)
    assert (
        canonicalizer.process_url("https://marksandspencer.com?pid=1&foo=2#frag")
        == "https://marksandspencer.com?foo=2#frag"
    )
    assert (
        canonicalizer.process_url("https://example.com?pid=1&foo=2#frag")
        == "https://example.com?pid=1&foo=2#frag"
    )


def test_query_removal_article_rules():
    assert RULE_PATHS is not None
    rule_path = [
        path for path in RULE_PATHS if path.endswith("queryRemoval/article.json")
    ]
    assert len(rule_path) == 1

    canonicalizer = UrlCanonicalizer(rule_path)

    assert len(canonicalizer.processors) > 0
    assert isinstance(list(canonicalizer.processors.values())[0], QueryRemovalProcessor)
    assert (
        canonicalizer.process_url("https://bbc.com?ICID=1&foo=2&utm_medium=bar#frag")
        == "https://bbc.com?foo=2#frag"
    )
    assert (
        canonicalizer.process_url(
            "https://example.com?ICID=1&foo=2&utm_medium=bar#frag"
        )
        == "https://example.com?ICID=1&foo=2&utm_medium=bar#frag"
    )


def test_query_removal_utm_rules():
    assert RULE_PATHS is not None
    rule_path = [path for path in RULE_PATHS if path.endswith("queryRemoval/utm.json")]
    assert len(rule_path) == 1

    canonicalizer = UrlCanonicalizer(rule_path)

    assert len(canonicalizer.processors) == 1
    assert isinstance(list(canonicalizer.processors.values())[0], QueryRemovalProcessor)
    assert (
        canonicalizer.process_url("https://example.com?foo=1&utm_medium=2#frag")
        == "https://example.com?foo=1#frag"
    )
