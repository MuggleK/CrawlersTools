import distance


def similarity1(s1, s2):
    """
    get similarity of two strings
    :param s1:
    :param s2:
    :return:
    """
    if not s1 or not s2:
        return 0
    edit_distance = distance.levenshtein(s1, s2)
    similarity_score = 1 - edit_distance / (len(s1) + len(s2))
    return similarity_score


def similarity2(s1, s2):
    """
    get similarity of two strings
    :param s1:
    :param s2:
    :return:
    """
    if not s1 or not s2:
        return 0
    s1_set = set(list(s1))
    s2_set = set(list(s2))
    intersection = s1_set.intersection(s2_set)
    union = s2_set.union(s1_set)
    return len(intersection) / len(union)


def similarity(s1, s2):
    """
    get similarity of two strings
    :param s1:
    :param s2:
    :return:
    """
    return similarity2(s1, s2)


def get_longest_common_sub_string(str1: str, str2: str) -> str:
    """
    get longest common string
    :param str1:
    :param str2:
    :return:
    """
    if not all([str1, str2]):
        return ''
    matrix = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]
    max_length = 0
    start_position = 0
    for index_of_str1 in range(1, len(str1) + 1):
        for index_of_str2 in range(1, len(str2) + 1):
            if str1[index_of_str1 - 1] == str2[index_of_str2 - 1]:
                matrix[index_of_str1][index_of_str2] = matrix[index_of_str1 - 1][index_of_str2 - 1] + 1
                if matrix[index_of_str1][index_of_str2] > max_length:
                    max_length = matrix[index_of_str1][index_of_str2]
                    start_position = index_of_str1 - max_length
            else:
                matrix[index_of_str1][index_of_str2] = 0
    return str1[start_position: start_position + max_length]


if __name__ == '__main__':
    s1 = 'hello'
    s2 = 'world'
    print(similarity(s1, s2))
