import re


def match_any_expression(value='', expressions=[]):
    """verifies if the input value matches any of the expressions using re

    Args:
        value (str, optional):
            [string to be tested against the expressions]. Defaults to ''.
        expressions (list, optional):
            [list of patterns (as strings) to test the value]. Defaults to [].
    """
    for expression in expressions:
        if re.match(expression, value):
            return True

    return False


def merge_distinct_tags(tag_list_a=[], tag_list_b=[]):
    """Returns a merge from both inputs, but choosing tag_list_b's tag values
    in case of equal keys

    Args:
        tag_list_a (list, optional): [List of tags]. Defaults to [].
        tag_list_b (list, optional): [List of tags]. Defaults to [].
    """
    tag_list_b_keys = map(lambda tag: tag['Key'], tag_list_b)
    merge = list(tag_list_b)

    for tag in tag_list_a:
        if tag['Key'] not in tag_list_b_keys:
            merge.append(tag)

    return merge
