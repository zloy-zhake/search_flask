import pickle
from typing import Literal, Tuple, Union

import fasttext
import Levenshtein
import numpy as np
from scipy import spatial

from .utils import get_model_absolute_path

SIMILARITY_THRESHOLD = 0.8


def is_similar_levenstein(str1: str, str2: str) -> Tuple[bool, float]:
    """[summary] TODO

    Arguments:
        str1 {str} -- [description]
        str2 {str} -- [description]
    Returns:
        Tuple[bool, float] -- [description]
    """
    ratio = Levenshtein.ratio(str1, str2)

    if ratio < SIMILARITY_THRESHOLD:
        return (False, ratio)
    else:
        return (True, ratio)


with open(
    file=get_model_absolute_path(model_path="ft_str_46K.pkl"), mode="rb"
) as f:
    ft_dict = pickle.load(file=f)


def get_fasttext_word_vec(word: str) -> np.array:
    if word in ft_dict:
        vec_str = ft_dict[word].split()
        vec_to_return = [float(val) for val in vec_str]
        return np.array(vec_to_return, dtype=np.float16)
    else:
        return np.zeros(shape=(300), dtype=np.float16)


def get_fasttext_text_vec(text: str) -> np.array:
    text_tok = fasttext.tokenize(text=text)
    text_word_vecs = [get_fasttext_word_vec(token) for token in text_tok]
    word_vec_sum = np.sum(a=text_word_vecs, axis=0)
    return word_vec_sum / len(text_word_vecs)


def is_similar_fasttext(str1: str, str2: str) -> Tuple[bool, float]:
    str1_vec = get_fasttext_text_vec(text=str1)
    str2_vec = get_fasttext_text_vec(text=str2)

    # Сделать fallback на левенштейна если пришли только нули
    if np.all(str1_vec == 0) or np.all(str2_vec == 0):
        return is_similar_levenstein(str1, str2)

    similarity = 1 - spatial.distance.cosine(str1_vec, str2_vec)

    if similarity < SIMILARITY_THRESHOLD:
        return (False, similarity)
    else:
        return (True, similarity)


def is_similar(
    str1: str,
    str2: str,
    method: Union[Literal["levenshtein"], Literal["fasttext"]] = "fasttext",
) -> Tuple[bool, float]:
    """[summary] TODO

    Arguments:
        str1 {str} -- [description]
        str2 {str} -- [description]
        method {Union[Literal[} -- [description]
    Returns:
        Tuple[bool, float] -- [description] sim_score
    """
    if method == "levenshtein":
        return is_similar_levenstein(str1=str1, str2=str2)
    elif method == "fasttext":
        return is_similar_fasttext(str1=str1, str2=str2)
    else:
        return (False, 0.0)


if __name__ == "__main__":
    # print(
    #     'str1="qwertyuiop nsldjfvnsldf dfkjvnskldfn", '
    #     'str2="qwertyuiop nsldjfvnsldf dfkjvnskldfn sdfkjvn, ldfjnvlsjd"'
    # )
    # print(
    #     "similarity:",
    #     is_similar(
    #         str1="qwertyuiop nsldjfvnsldf dfkjvnskldfn",
    #         str2="qwertyuiop nsldjfvnsldf dfkjvnskldfn sdfkjvn, ldfjnvlsjd",
    #         method="levenshtein",
    #     ),
    # )
    # print()
    # print('str1="qwertyuiop", str2="qwerthjkl"')
    # print(
    #     "similarity:",
    #     is_similar(str1="qwertyuiop", str2="qwerthjkl", method="levenshtein"),
    # )
    # print()
    # print('str1="qwertyuiop", str2="qwertyuikl"')
    # print(
    #     "similarity:",
    #     is_similar(str1="qwertyuiop", str2="qwertyuikl", method="levenshtein"),
    # )
    # print()
    # print('str1="qwertyuiop", str2="qwertyuiop"')
    # print(
    #     "similarity:",
    #     is_similar(str1="qwertyuiop", str2="qwertyuiop", method="levenshtein"),
    # )

    # ============================================================

    # str1="qwertyuiop", str2="asdfghjkl"
    # similarity: (False, 0.0)

    # str1="qwertyuiop", str2="qwerthjkl"
    # similarity: (False, 0.5263157894736842)

    # str1="qwertyuiop", str2="qwertyuikl"
    # similarity: (True, 0.8)

    # str1="qwertyuiop", str2="qwertyuiop"
    # similarity: (True, 1.0)

    # ============================================================

    print(
        'str1="асыру жөнінде жұмыспен", '
        'str2="асыру жөнінде жұмыспен онда, қатысушылар"'
    )
    print(
        "similarity:",
        is_similar(
            str1="асыру жөнінде жұмыспен",
            str2="асыру жөнінде жұмыспен онда, қатысушылар",
            method="fasttext",
        ),
    )
    print()
    print('str1="qwertyuiop", str2="qwerthjkl"')
    print(
        "similarity:",
        is_similar(str1="qwertyuiop", str2="qwerthjkl", method="fasttext"),
    )
    print()
    print('str1="qwertyuiop", str2="qwertyuikl"')
    print(
        "similarity:",
        is_similar(str1="qwertyuiop", str2="qwertyuikl", method="fasttext"),
    )
    print()
    print('str1="qwertyuiop", str2="qwertyuiop"')
    print(
        "similarity:",
        is_similar(str1="qwertyuiop", str2="qwertyuiop", method="fasttext"),
    )
