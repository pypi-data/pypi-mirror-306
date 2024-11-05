# Textmentations

Textmentations is a Python library for augmenting Korean text.
Inspired by [albumentations](https://github.com/albumentations-team/albumentations).
Textmentations uses the albumentations as a dependency.

## Installation

```
pip install textmentations
```

## A simple example

Textmentations provides text augmentation techniques implemented using the [TextTransform](https://github.com/Jaesu26/textmentations/blob/v1.4.0/textmentations/core/transforms_interface.py#L19),
which inherits from the albumentations [BasicTransform](https://github.com/albumentations-team/albumentations/blob/1.4.14/albumentations/core/transforms_interface.py#L48).

This allows textmentations to reuse the existing functionalities of albumentations.

```python
import textmentations as T

text = "어제 식당에 갔다. 목이 너무 말랐다. 먼저 물 한 잔을 마셨다. 그리고 탕수육을 맛있게 먹었다."
rd = T.RandomDeletion(deletion_prob=0.1, min_words_per_sentence=0.8)
ri = T.RandomInsertion(insertion_prob=0.2, n_times=1)
rs = T.RandomSwap(alpha=1)
sr = T.SynonymReplacement(replacement_prob=0.2)
eda = T.Compose([rd, ri, rs, sr])

print(rd(text=text)["text"])
# 식당에 갔다. 목이 너무 말랐다. 먼저 물 잔을 마셨다. 그리고 탕수육을 맛있게 먹었다.

print(ri(text=text)["text"])
# 어제 최근 식당에 갔다. 목이 너무 말랐다. 먼저 물 한 잔을 마셨다 음료수. 그리고 탕수육을 맛있게 먹었다.

print(rs(text=text)["text"])
# 어제 갔다 식당에. 목이 너무 말랐다. 물 먼저 한 잔을 마셨다. 그리고 탕수육을 맛있게 먹었다..

print(sr(text=text)["text"])
# 과거 식당에 갔다. 목이 너무 말랐다. 먼저 소주 한 잔을 마셨다. 그리고 탕수육을 맛있게 먹었다.

print(eda(text=text)["text"])
# 식당에 어제 과거 갔다. 너무 말랐다. 먼저 상수 한 잔을 마셨다 맹물. 그리고 맛있게 먹었다.
```

## List of augmentations

- [AEDA](https://github.com/Jaesu26/textmentations/blob/v1.4.0/textmentations/augmentations/modification/transforms.py#L13)
- [BackTranslation](https://github.com/Jaesu26/textmentations/blob/v1.4.0/textmentations/augmentations/generation/transforms.py#L21)
- [ContextualInsertion](https://github.com/Jaesu26/textmentations/blob/v1.4.0/textmentations/augmentations/generation/transforms.py#L67)
- [ContextualReplacement](https://github.com/Jaesu26/textmentations/blob/v1.4.0/textmentations/augmentations/generation/transforms.py#L128)
- [IterativeMaskFilling](https://github.com/Jaesu26/textmentations/blob/v1.4.0/textmentations/augmentations/generation/transforms.py#L193)
- [RandomDeletion](https://github.com/Jaesu26/textmentations/blob/v1.4.0/textmentations/augmentations/modification/transforms.py#L105)
- [RandomDeletionSentence](https://github.com/Jaesu26/textmentations/blob/v1.4.0/textmentations/augmentations/modification/transforms.py#L177)
- [RandomInsertion](https://github.com/Jaesu26/textmentations/blob/v1.4.0/textmentations/augmentations/modification/transforms.py#L262)
- [RandomSwap](https://github.com/Jaesu26/textmentations/blob/v1.4.0/textmentations/augmentations/modification/transforms.py#L312)
- [RandomSwapSentence](https://github.com/Jaesu26/textmentations/blob/v1.4.0/textmentations/augmentations/modification/transforms.py#L371)
- [SynonymReplacement](https://github.com/Jaesu26/textmentations/blob/v1.4.0/textmentations/augmentations/modification/transforms.py#L411)

## References

- [AEDA: An Easier Data Augmentation Technique for Text Classification](https://arxiv.org/pdf/2108.13230)
- [Conditional BERT Contextual Augmentation](https://arxiv.org/pdf/1812.06705)
- [Contextual Augmentation: Data Augmentation by Words with Paradigmatic Relations](https://arxiv.org/pdf/1805.06201)
- [EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks](https://arxiv.org/pdf/1901.11196)
- [Iterative Mask Filling: An Effective Text Augmentation Method Using Masked Language Modeling](https://arxiv.org/pdf/2401.01830)
- [Korean Stopwords](https://www.ranks.nl/stopwords/korean)
- [Korean WordNet](http://wordnet.kaist.ac.kr/)
- [albumentations](https://github.com/albumentations-team/albumentations)
- [kykim/albert-kor-base](https://huggingface.co/kykim/albert-kor-base)
