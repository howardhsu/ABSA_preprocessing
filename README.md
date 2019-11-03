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
