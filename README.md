# ABSA_preprocessing
A simple library to preprocess ABSA (Aspect-base Sentiment Analysis) related tasks from SemEval datasets.  
Note that many existing papers may use different preprocessing methods, which obviously make comparison of different methods harder. We don't aim to build a univeral preprocessing method because there's no universal way as different models require different preprocessing, such as tokenization, capitalization, how many validation data is used etc. So we would rather treat preprocessing as one part of a method and this preprocessing code is just ONE way to convert xml data into model friendly inputs.

### Source
We mostly focus on 3 datasets from SemEval ([SemEval 2014](http://alt.qcri.org/semeval2014/task4/), [SemEval 2015](http://alt.qcri.org/semeval2015/task12/), [SemEval 2016](http://alt.qcri.org/semeval2016/task5/) ) on two (2) domains (laptop and restaurant).

### Tasks

We focus on 4 tasks in aspect-based sentiment analysis: aspect extraction (AE) and aspect sentiment classification (ASC), aspect category classification (ACC) and aspect catgory sentiment classification(ACSC).

AE: given a review sentence ("The retina display is great."), find aspects("retina display");

ASC: given an aspect ("retina display") and a review sentence ("The retina display is great."), detect the polarity of that aspect (positive).

ACC: given a sentence, find aspect category in that sentence.

ACSC: given a sentence, find polarities corresponding to each aspect category.

#### Aspect Extraction (AE)

| Dataset     | Laptop | Restaurant |
|-------------|--------|------------|
| SemEval2014 |   y    |     y      |
| SemEval2015 |        |     y      |
| SemEval2016 |        |     y      |

#### Aspect Sentiment Classification (ASC)

| Dataset     | Laptop | Restaurant |
|-------------|--------|------------|
| SemEval2014 |   y    |     y      |
| SemEval2015 |        |     y      |
| SemEval2016 |        |     y      |

#### Aspect Category Classification (ACC)

| Dataset     | Laptop | Restaurant |
|-------------|--------|------------|
| SemEval2014 |        |     y      |
| SemEval2015 |   y    |     y      |
| SemEval2016 |   y    |     y      |


#### Aspect Category Sentiment Classification (ACSC)

| Dataset     | Laptop | Restaurant |
|-------------|--------|------------|
| SemEval2014 |        |     y      |
| SemEval2015 |   y    |     y      |
| SemEval2016 |   y    |     y      |

### Citation
If you find this rep to be useful, please cite the following paper.
```
@inproceedings{xu-etal-2019-bert,
    title = "{BERT} Post-Training for Review Reading Comprehension and Aspect-based Sentiment Analysis",
    author = "Xu, Hu  and
      Liu, Bing  and
      Shu, Lei  and
      Yu, Philip",
    booktitle = "Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)",
    month = jun,
    year = "2019",
    address = "Minneapolis, Minnesota",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/N19-1242",
    doi = "10.18653/v1/N19-1242",
    pages = "2324--2335",
    abstract = "Question-answering plays an important role in e-commerce as it allows potential customers to actively seek crucial information about products or services to help their purchase decision making. Inspired by the recent success of machine reading comprehension (MRC) on formal documents, this paper explores the potential of turning customer reviews into a large source of knowledge that can be exploited to answer user questions. We call this problem Review Reading Comprehension (RRC). To the best of our knowledge, no existing work has been done on RRC. In this work, we first build an RRC dataset called ReviewRC based on a popular benchmark for aspect-based sentiment analysis. Since ReviewRC has limited training examples for RRC (and also for aspect-based sentiment analysis), we then explore a novel post-training approach on the popular language model BERT to enhance the performance of fine-tuning of BERT for RRC. To show the generality of the approach, the proposed post-training is also applied to some other review-based tasks such as aspect extraction and aspect sentiment classification in aspect-based sentiment analysis. Experimental results demonstrate that the proposed post-training is highly effective.",
}
```
