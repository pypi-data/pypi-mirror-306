from pprint import pprint
import json


def lookup_lists(list1, list2, match_check=lambda x, y: x == y):  # left outer join
    result = []
    for iter1 in list1:
        matching_iter2 = None
        for iter2 in list2:
            if match_check(iter1, iter2):
                matching_iter2 = iter2
                break
        result.append({'base': iter1, 'lookup': matching_iter2})
    return result


def compare_lists(list1, list2, equal_check=lambda x, y: x == y):
    result = {
        'matched': [],
        '+': [],
        '-': []
    }
    for iter1 in list1:
        is_iter1_found_in_iter2 = False
        for iter2 in list2:
            if equal_check(iter1, iter2):
                is_iter1_found_in_iter2 = True
                break
        if is_iter1_found_in_iter2:
            result['matched'].append(iter1)
        else:
            result['+'].append(iter1)
    for iter2 in list2:
        is_iter2_found_in_iter1 = False
        for iter1 in list1:
            if equal_check(iter1, iter2):
                is_iter2_found_in_iter1 = True
                break
        if not is_iter2_found_in_iter1:
            result['-'].append(iter2)
    return result
