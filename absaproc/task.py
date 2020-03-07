import xml.etree.ElementTree as ET
import nltk


class Task(object):
    _TAG_DICTS = {
        "14": {
            "review": "sentences",
            "aspect": "term",
            "aspects": "aspectTerm",
        },
        "15_16": {
            "review": "Review",
            "aspect": "target",
            "aspects": "Opinion",
        }
    }

    def __init__(self, taskconfig):
        self.year = taskconfig.fileconfig.year
        self.train_file = taskconfig.fileconfig.train_file
        self.test_file = taskconfig.fileconfig.test_file

        for tag_name in self._TAG_DICTS:
            if self.year in tag_name:
                self.tag_dict = self._TAG_DICTS[tag_name]

    def parseTrain(self):
        return self.parse(self.train_file)

    def parseTest(self):
        return self.parse(self.test_file)

    def parse(self, fn):
        raise NotImplementedError


class SeqLabelingTask(Task):
    _LABEL_SET = {    
        "BIO": {
            "label_map": {
                "O": "O", 
                "B-positive": "B", 
                "B-negative": "B", 
                "B-neutral": "B",
                "B-conflict": "B",
                "I-positive": "I",
                "I-negative": "I",
                "I-neutral": "I",
                "I-conflict": "I",
            },
            "label_list": ["O", "B", "I"]
        },
        "AO": {
            "label_map": {
                "O": "O",
                "B-positive": "A", 
                "B-negative": "A", 
                "B-neutral": "A",
                "B-conflict": "A",
                "I-positive": "A",
                "I-negative": "A",
                "I-neutral": "A",
                "I-conflict": "A",
            },
            "label_list": ["O", "A"]
        },
        "PNNO": {
            "label_map": {
                "O": "O",
                "B-positive": "positive", 
                "B-negative": "negative", 
                "B-neutral": "neutral",
                "B-conflict": "neutral",
                "I-positive": "positive",
                "I-negative": "negative",
                "I-neutral": "neutral",
                "I-conflict": "neutral",
            },
            "label_list": ["O", "positive", "negative", "neutral"]
        }
    }

    def _tokenize_text(self, raw_text, opins, label_map):
        # warning this code this borrowed from the project : https://github.com/howardhsu/DE-CNN
        # the code needs cleaner re-writing.
        text = []
        for ix, c in enumerate(raw_text):
            # assuming that the tokenizer always yields fine-grained tokens for aspects 
            # so tokenizer won't affect the performance of AE.
            for opin in opins:
                if (c=='/' or c=='*' or c=='-' or c=='=') and len(text)>0 and text[-1]!=' ':
                    text.append(' ')
                if ix==int(opin[1] ) and len(text)>0 and text[-1]!=' ':
                    text.append(' ')
                elif ix==int(opin[2] ) and len(text)>0 and text[-1]!=' ' and c!=' ':
                    text.append(' ')
            text.append(c)
            if (c=='/' or c=='*' or c=='-' or c=='=') and text[-1]!=' ':
                text.append(' ')
            
        text="".join(text)
        tokens=nltk.word_tokenize(text)
        lb = [label_map["O"]]*len(tokens)

        for opin in opins: # mark each aspect
            token_idx, pt, tag_on=0, 0, False
            for ix, c in enumerate(raw_text):
                if pt>=len(tokens[token_idx] ):
                    pt=0
                    token_idx+=1
                    if token_idx >= len(tokens):
                        break
                if ix==opin[1]: #from
                    assert pt == 0 and c != ' '
                    lb[token_idx] = label_map["B-" + opin[3]]
                    tag_on = True
                elif ix==opin[2]: #to
                    assert pt == 0
                    tag_on = False
                elif tag_on and pt==0 and c!=' ':
                    lb[token_idx] = label_map["I-" + opin[3]]
                if c==' ' or ord(c)==160: # skip spaces.
                    pass
                elif tokens[token_idx][pt:pt+2]=='``' or tokens[token_idx][pt:pt+2]=="''":
                    pt+=2
                else:
                    pt+=1
        return tokens, lb


class AETask(SeqLabelingTask):
    def __init__(self, taskconfig):
        super().__init__(taskconfig)
        self.label_set = "BIO"

    def parse(self, fn):
        root=ET.parse(fn).getroot()
        corpus = []
        for sents in root.iter(self.tag_dict["review"]):
            for sent in sents.iter("sentence"):
                opins=set()
                for opin in sent.iter(self.tag_dict["aspects"]):
                    if int(opin.attrib['from'] )!=int(opin.attrib['to'] ) and opin.attrib[self.tag_dict["aspect"]]!="NULL":
                        opins.add((opin.attrib[self.tag_dict["aspect"]], int(opin.attrib['from']), int(opin.attrib['to']), opin.attrib['polarity']) )
                tokens, lb = self._tokenize_text(sent.find('text').text, opins, self._LABEL_SET[self.label_set]["label_map"])
                corpus.append({"id": sent.attrib['id'], 
                            "tokens": tokens, 
                            "labels": lb})
        return corpus, {"label_list": self._LABEL_SET[self.label_set]["label_list"]}


class ASCTask(Task):
    polar_idx={'positive': 0, 'negative': 1, 'neutral': 2}
    idx_polar={0: 'positive', 1: 'negative', 2: 'neutral'}

    def _parse14(self, root):
        corpus=[]
        for sents in root.iter("sentences"):
            for sent in sents.iter("sentence"):
                for ix, opin in enumerate(sent.iter('aspectTerm')):
                    if opin.attrib['polarity'] in self.polar_idx \
                        and int(opin.attrib['from'] )!=int(opin.attrib['to'] ) and opin.attrib['term']!="NULL":
                        corpus.append({"id": sent.attrib['id']+"_"+str(ix), 
                                    "sentence": sent.find('text').text, 
                                    "term": opin.attrib['term'], 
                                    "polarity": opin.attrib['polarity'] })
        return corpus

    def _parse1516(self, root):
        """we remove aspects with two or more different polarities: annotation disagreement"""
        corpus = []
        for review in root.iter("Review"):
            for sent in review.iter("sentence"):
                target2polarity = {}
                forbid = []
                for ix, opin in enumerate(sent.iter('Opinion')):
                    if opin.attrib['polarity'] in self.polar_idx:
                        if opin.attrib['target'] in target2polarity and target2polarity[opin.attrib['target']] != opin.attrib['polarity']:
                            forbid.append(opin.attrib['target'])
                        target2polarity[opin.attrib['target']] = opin.attrib['polarity']
                        
                for ix, opin in enumerate(sent.iter('Opinion')):
                    if opin.attrib['target'] not in forbid:
                        corpus.append({"id": sent.attrib['id']+"_"+str(ix), 
                                        "sentence": sent.find('text').text, 
                                        "term": opin.attrib['target'], 
                                        "polarity": opin.attrib['polarity']})
        return corpus

    def parse(self, fn):
        root = ET.parse(fn).getroot()
        corpus = self._parse14(root) if "14" in self.year else self._parse1516(root)        
        return corpus, {"label_list": ["positive", "negative", "neutral"]}


class E2ETask(SeqLabelingTask):
    def __init__(self, taskconfig):
        super().__init__(taskconfig)
        self.label_set = "PNNO"

    def parse(self, fn):
        root=ET.parse(fn).getroot()
        corpus = []
        for sents in root.iter(self.tag_dict["review"]):
            for sent in sents.iter("sentence"):
                opins=set()
                for opin in sent.iter(self.tag_dict["aspects"]):
                    if int(opin.attrib['from'] )!=int(opin.attrib['to'] ) and opin.attrib[self.tag_dict["aspect"]]!="NULL":
                        opins.add((opin.attrib[self.tag_dict["aspect"]], int(opin.attrib['from']), int(opin.attrib['to']), opin.attrib['polarity']) )
                tokens, lb = self._tokenize_text(sent.find('text').text, opins, self._LABEL_SET[self.label_set]["label_map"])       
                corpus.append({"id": sent.attrib['id'], 
                            "tokens": tokens, 
                            "labels": lb})
        return corpus, {"label_list": self._LABEL_SET[self.label_set]["label_list"]}
