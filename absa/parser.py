import xml.etree.ElementTree as ET
import nltk

def tokenize_text(raw_text, opins, label_map):
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

# TODO: make these into configs, too
LABEL_SET = {    
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

def parse_ae_SemEval14(fn, label_set = "BIO"):
    root=ET.parse(fn).getroot()
    corpus = []
    for sents in root.iter("sentences"):
        for sent in sents.iter("sentence"):
            opins=set()
            for opin in sent.iter('aspectTerm'):
                if int(opin.attrib['from'] )!=int(opin.attrib['to'] ) and opin.attrib['term']!="NULL":
                    opins.add((opin.attrib['term'], int(opin.attrib['from']), int(opin.attrib['to']), opin.attrib['polarity']) )
            tokens, lb = tokenize_text(sent.find('text').text, opins, LABEL_SET[label_set]["label_map"])
            corpus.append({"id": sent.attrib['id'], 
                        "tokens": tokens, 
                        "labels": lb})
    return corpus, {"label_list": LABEL_SET[label_set]["label_list"]}

def parse_ae_SemEval1516(fn, label_set = "BIO"):
    root=ET.parse(fn).getroot()
    corpus = []
    for review in root.iter("Review"):
        for sent in review.iter("sentence"):
            opins=set()
            for opin in sent.iter('Opinion'):
                if int(opin.attrib['from'] )!=int(opin.attrib['to'] ) and opin.attrib['target']!="NULL":
                    opins.add((opin.attrib['target'], int(opin.attrib['from']), int(opin.attrib['to']), opin.attrib['polarity']) )
            tokens, lb = tokenize_text(sent.find('text').text, opins, LABEL_SET[label_set]["label_map"])       
            corpus.append({"id": sent.attrib['id'], 
                        "tokens": tokens, 
                        "labels": lb})
    return corpus, {"label_list": LABEL_SET[label_set]["label_list"]}


polar_idx={'positive': 0, 'negative': 1, 'neutral': 2}

idx_polar={0: 'positive', 1: 'negative', 2: 'neutral'}

def parse_asc_SemEval14(fn):
    root=ET.parse(fn).getroot()
    corpus=[]
    for sents in root.iter("sentences"):
        for sent in sents.iter("sentence"):
            for ix, opin in enumerate(sent.iter('aspectTerm')):
                if opin.attrib['polarity'] in polar_idx \
                    and int(opin.attrib['from'] )!=int(opin.attrib['to'] ) and opin.attrib['term']!="NULL":
                    corpus.append({"id": sent.attrib['id']+"_"+str(ix), 
                                "sentence": sent.find('text').text, 
                                "term": opin.attrib['term'], 
                                "polarity": opin.attrib['polarity'] })
    return corpus, {"label_list": ["positive", "negative", "neutral"]}

def parse_asc_SemEval1516(fn):
    """we remove aspects with two or more different polarities: annotation disagreement"""
    root=ET.parse(fn).getroot()
    corpus = []
    for review in root.iter("Review"):
        for sent in review.iter("sentence"):
            target2polarity = {}
            forbid = []
            for ix, opin in enumerate(sent.iter('Opinion')):
                if opin.attrib['polarity'] in polar_idx:
                    if opin.attrib['target'] in target2polarity and target2polarity[opin.attrib['target']] != opin.attrib['polarity']:
                        forbid.append(opin.attrib['target'])
                    target2polarity[opin.attrib['target']] = opin.attrib['polarity']
                    
            for ix, opin in enumerate(sent.iter('Opinion')):
                if opin.attrib['target'] not in forbid:
                    corpus.append({"id": sent.attrib['id']+"_"+str(ix), 
                                    "sentence": sent.find('text').text, 
                                    "term": opin.attrib['target'], 
                                    "polarity": opin.attrib['polarity']})
    return corpus, {"label_list": ["positive", "negative", "neutral"]}


def parse_e2e_SemEval14(fn, label_set = "PNNO"):
    root=ET.parse(fn).getroot()
    corpus = []
    for sents in root.iter("sentences"):
        for sent in sents.iter("sentence"):
            opins=set()
            for opin in sent.iter('aspectTerm'):
                if int(opin.attrib['from'] )!=int(opin.attrib['to'] ) and opin.attrib['term']!="NULL":
                    opins.add((opin.attrib['term'], int(opin.attrib['from']), int(opin.attrib['to']), opin.attrib['polarity']) )
            tokens, lb = tokenize_text(sent.find('text').text, opins, LABEL_SET[label_set]["label_map"])       
            corpus.append({"id": sent.attrib['id'], 
                        "tokens": tokens, 
                        "labels": lb})
    return corpus, {"label_list": LABEL_SET[label_set]["label_list"]}


def parse_e2e_SemEval1516(fn, label_set = "PNNO"):
    """we remove aspects with two or more different polarities: annotation disagreement"""
    root=ET.parse(fn).getroot()
    corpus = []
    for review in root.iter("Review"):
        for sent in review.iter("sentence"):
            opins=set()
            for opin in sent.iter('Opinion'):
                if int(opin.attrib['from'] )!=int(opin.attrib['to'] ) and opin.attrib['target']!="NULL":
                    opins.add((opin.attrib['target'], int(opin.attrib['from']), int(opin.attrib['to']), opin.attrib['polarity']) )
            tokens, lb = tokenize_text(sent.find('text').text, opins, LABEL_SET[label_set]["label_map"])       
            corpus.append({"id": sent.attrib['id'], 
                        "tokens": tokens, 
                        "labels": lb})
    return corpus, {"label_list": LABEL_SET[label_set]["label_list"]}


parser_config={
    'ae': {
        '14': parse_ae_SemEval14,
        '15': parse_ae_SemEval1516,
        '16': parse_ae_SemEval1516
    },
    'asc': {
        '14': parse_asc_SemEval14,
        '15': parse_asc_SemEval1516,
        '16': parse_asc_SemEval1516
    },
    'e2e': {
        '14': parse_e2e_SemEval14,
        '15': parse_e2e_SemEval1516,
        '16': parse_e2e_SemEval1516
    },
}