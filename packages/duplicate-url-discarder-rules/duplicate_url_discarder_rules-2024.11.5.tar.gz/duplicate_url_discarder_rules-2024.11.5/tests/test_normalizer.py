from duplicate_url_discarder.processors import NormalizerProcessor
from duplicate_url_discarder.url_canonicalizer import UrlCanonicalizer

from duplicate_url_discarder_rules import RULE_PATHS


def test_normalizer_main_rules():
    assert RULE_PATHS is not None
    rule_path = [path for path in RULE_PATHS if path.endswith("normalizer/main.json")]
    assert len(rule_path) == 1

    canonicalizer = UrlCanonicalizer(rule_path)

    assert len(canonicalizer.processors) == 1
    assert isinstance(list(canonicalizer.processors.values())[0], NormalizerProcessor)

    assert (
        canonicalizer.process_url("https://www.example.com/some-text/dp/ASIN/?p=1#frag")
        == "https://example.com/some-text/dp/ASIN?p=1#frag"
    )
