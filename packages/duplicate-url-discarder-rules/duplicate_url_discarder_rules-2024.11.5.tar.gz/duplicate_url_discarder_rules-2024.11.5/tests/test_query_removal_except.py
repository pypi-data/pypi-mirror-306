from duplicate_url_discarder.processors import QueryRemovalExceptProcessor
from duplicate_url_discarder.url_canonicalizer import UrlCanonicalizer

from duplicate_url_discarder_rules import RULE_PATHS


def test_query_removal_except_product_rules():
    assert RULE_PATHS is not None
    rule_path = [
        path for path in RULE_PATHS if path.endswith("queryRemovalExcept/product.json")
    ]
    assert len(rule_path) == 1

    canonicalizer = UrlCanonicalizer(rule_path)

    assert len(canonicalizer.processors) == 1
    assert isinstance(
        list(canonicalizer.processors.values())[0], QueryRemovalExceptProcessor
    )

    domains = [
        "ae",
        "ca",
        "cn",
        "co.jp",
        "co.uk",
        "com.au",
        "com.br",
        "com.mx",
        "com.sg",
        "com.tr",
        "com",
        "de",
        "es",
        "fr",
        "in",
        "it",
        "nl",
        "pt",
        "sa",
        "se",
    ]

    for domain in domains:
        assert (
            canonicalizer.process_url(
                f"https://www.amazon.{domain}/some-text/dp/ASIN?p=1&q=2#frag"
            )
            == f"https://www.amazon.{domain}/some-text/dp/ASIN#frag"
        )
        assert (
            canonicalizer.process_url(
                f"https://www.amazon.{domain}/dp/ASIN?p=1&q=2#frag"
            )
            == f"https://www.amazon.{domain}/dp/ASIN#frag"
        )
