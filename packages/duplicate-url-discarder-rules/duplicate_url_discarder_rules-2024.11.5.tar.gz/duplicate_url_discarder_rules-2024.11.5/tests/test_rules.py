import json

from url_matcher import Patterns

from duplicate_url_discarder_rules import (
    RULE_PATHS,
    RULE_PATHS_ARTICLE,
    RULE_PATHS_COMMON,
    RULE_PATHS_PRODUCT,
)


def test_rule_validity():
    assert RULE_PATHS is not None
    for path in RULE_PATHS:
        try:
            with open(path, "r") as f:
                raw_text = f.read()
                data = json.loads(raw_text)
        except Exception as e:
            raise ValueError(f"Something went wrong when reading '{path}': {str(e)}.")

        assert isinstance(
            data, list
        ), f"The rules should be a list: '{path}'. Got {type(data)}."

        for rule in data:
            order = rule.get("order")
            assert order is not None, path
            assert isinstance(order, int), path

            url_pattern = rule.get("urlPattern")
            assert isinstance(url_pattern, dict), path
            assert isinstance(url_pattern["include"], list), path
            assert Patterns(url_pattern)

            assert rule.get("processor"), path
            assert isinstance(rule.get("processor"), str), path

            if "args" in rule:
                assert isinstance(rule["args"], (list, tuple))

        assert (
            json.dumps(data, indent=2, sort_keys=True) == raw_text.rstrip()
        ), f"Check {path} for formatting issue"


def test_rules_concat():
    assert RULE_PATHS is not None
    all_rules = RULE_PATHS_COMMON + RULE_PATHS_ARTICLE + RULE_PATHS_PRODUCT
    assert isinstance(all_rules, list)
    for path in all_rules:
        assert isinstance(path, str)
    assert set(all_rules) == set(RULE_PATHS)
