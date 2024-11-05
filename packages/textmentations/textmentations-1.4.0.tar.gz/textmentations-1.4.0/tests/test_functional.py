from unittest.mock import patch

import pytest
from deep_translator.exceptions import TooManyRequests

import textmentations.augmentations.generation.functional as fg
import textmentations.augmentations.modification.functional as fm
from tests.utils import contains_mask_token
from textmentations.augmentations.generation.transforms import _albert_model, _albert_tokenizer
from textmentations.augmentations.utils import split_text_into_sentences


def test_back_translate():
    text = "나는 목이 말라서 물을 마셨다."
    from_lang = "ko"
    to_lang = "en"
    augmented_text = fg.back_translate(text, from_lang, to_lang)
    assert augmented_text != text


def test_back_translate_too_many_requests():
    text = "나는 목이 말라서 물을 마셨다."
    from_lang = "ko"
    to_lang = "en"
    with patch("textmentations.augmentations.generation.functional._get_translator") as mock_get_translator:
        mock_translator = mock_get_translator.return_value
        mock_translator.translate.side_effect = TooManyRequests
        augmented_text = fg.back_translate(text, from_lang, to_lang)
        assert augmented_text == text


@pytest.mark.parametrize(
    ["deletion_prob", "min_words_per_sentence", "expected_text"],
    [
        (0.0, 0.5, "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."),
        (False, 1, "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."),
        (1.0, 0.0, ""),
        (1.0, 1.0, "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."),
        (1.0, 0, ""),
        (True, 3, "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."),
    ],
)
def test_delete_words(deletion_prob, min_words_per_sentence, expected_text):
    text = "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."
    augmented_text = fm.delete_words(text, deletion_prob, min_words_per_sentence)
    assert augmented_text == expected_text


@pytest.mark.parametrize(
    ["deletion_prob", "min_sentences", "expected_text"],
    [
        (0.0, 0.5, "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."),
        (False, 1, "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."),
        (1.0, 0.0, ""),
        (1.0, 1.0, "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."),
        (1.0, 0, ""),
        (True, 3, "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."),
    ],
)
def test_delete_sentences(deletion_prob, min_sentences, expected_text):
    text = "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."
    augmented_text = fm.delete_sentences(text, deletion_prob, min_sentences)
    assert augmented_text == expected_text


def test_insert_contextual_words():
    text = "나는 목이 말라서 물을 마셨다."
    model = _albert_model
    tokenizer = _albert_tokenizer
    insertion_prob = 1.0
    top_k = 5
    device = "cpu"
    augmented_text = fg.insert_contextual_words(text, model, tokenizer, insertion_prob, top_k, device)
    assert augmented_text != text
    assert not contains_mask_token(augmented_text)


@pytest.mark.parametrize(["input_text", "is_same"], [("text_with_synonyms", False), ("text_without_synonyms", True)])
def test_insert_synonyms(input_text, is_same, request):
    text = request.getfixturevalue(input_text)
    insertion_prob = 1.0
    n_times = 1
    augmented_text = fm.insert_synonyms(text, insertion_prob, n_times)
    assert (augmented_text == text) == is_same


def test_insert_punctuation(text_without_synonyms):
    insertion_prob = 1.0
    punctuation = (";",)
    augmented_text = fm.insert_punctuation(text_without_synonyms, insertion_prob, punctuation)
    expected_text = "; 짜장면을 ; 맛있게 ; 먹었다 ;. ; 짬뽕도 ; 맛있게 ; 먹었다 ;. ; 짬짜면도 ; 먹고 ; 싶었다 ;."
    assert augmented_text == expected_text


def test_iterative_mask_fill(text):
    original_sentences = split_text_into_sentences(text)
    model = _albert_model
    tokenizer = _albert_tokenizer
    top_k = 5
    device = "cpu"
    augmented_text = fg.iterative_mask_fill(text, model, tokenizer, top_k, device)
    augmented_sentences = split_text_into_sentences(augmented_text)
    assert sum([augmented != original for augmented, original in zip(augmented_sentences, original_sentences)]) == 1
    assert not contains_mask_token(augmented_text)


def test_replace_contextual_words():
    text = "나는 목이 말라서 물을 마셨다."
    model = _albert_model
    tokenizer = _albert_tokenizer
    masking_prob = 1.0
    top_k = 5
    device = "cpu"
    augmented_text = fg.replace_contextual_words(text, model, tokenizer, masking_prob, top_k, device)
    assert augmented_text != text
    assert not contains_mask_token(augmented_text)


@pytest.mark.parametrize(["input_text", "is_same"], [("text_with_synonyms", False), ("text_without_synonyms", True)])
def test_replace_synonyms(input_text, is_same, request):
    text = request.getfixturevalue(input_text)
    replacement_prob = 1.0
    augmented_text = fm.replace_synonyms(text, replacement_prob)
    assert (augmented_text == text) == is_same


def test_swap_words(text):
    original_sentences = split_text_into_sentences(text)
    alpha = 0.01
    augmented_text = fm.swap_words(text, alpha)
    augmented_sentences = split_text_into_sentences(augmented_text)
    assert sum([augmented != original for augmented, original in zip(augmented_sentences, original_sentences)]) == 1


def test_swap_sentences(text):
    original_sentences = split_text_into_sentences(text)
    n = len(original_sentences)
    assert n >= 2
    n_times = 1
    augmented_text = fm.swap_sentences(text, n_times)
    augmented_sentences = split_text_into_sentences(augmented_text)
    assert sum([augmented != original for augmented, original in zip(augmented_sentences, original_sentences)]) == 2
