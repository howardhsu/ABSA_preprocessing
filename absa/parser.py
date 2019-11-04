import xml.etree.ElementTree as ET
import nltk

from .config import polar_idx

def tokenize_text(raw_text, opins):
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
    lb=[0]*len(tokens)

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
                lb[token_idx] = 1
                tag_on = True
            elif ix==opin[2]: #to
                assert pt == 0
                tag_on = False   
            elif tag_on and pt==0 and c!=' ':
                lb[token_idx] = 2
            if c==' ' or ord(c)==160: # skip spaces.
                pass
            elif tokens[token_idx][pt:pt+2]=='``' or tokens[token_idx][pt:pt+2]=="''":
                pt+=2
            else:
                pt+=1
    return tokens, lb


def parse_ae_SemEval14(fn):
    root=ET.parse(fn).getroot()
    corpus = []
    for sents in root.iter("sentences"):
        for sent in sents.iter("sentence"):
            opins=set()
            for opin in sent.iter('aspectTerm'):
                if int(opin.attrib['from'] )!=int(opin.attrib['to'] ) and opin.attrib['term']!="NULL":
                    opins.add((opin.attrib['term'], int(opin.attrib['from']), int(opin.attrib['to'])) )
            tokens, lb = tokenize_text(sent.find('text').text, opins)       
            corpus.append({"id": sent.attrib['id'], 
                        "tokens": tokens, 
                        "labels": lb})
    return corpus, None

def parse_ae_SemEval1516(fn):
    root=ET.parse(fn).getroot()
    corpus = []
    for review in root.iter("Review"):
        for sent in review.iter("sentence"):
            opins=set()
            for opin in sent.iter('Opinion'):
                if int(opin.attrib['from'] )!=int(opin.attrib['to'] ) and opin.attrib['target']!="NULL":
                    opins.add((opin.attrib['target'], int(opin.attrib['from']), int(opin.attrib['to'])) )
            tokens, lb = tokenize_text(sent.find('text').text, opins)       
            corpus.append({"id": sent.attrib['id'], 
                        "tokens": tokens, 
                        "labels": lb})
    return corpus, None


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
    return corpus, None

def parse_asc_SemEval1516(fn):
    root=ET.parse(fn).getroot()
    corpus = []
    for review in root.iter("Review"):
        for sent in review.iter("sentence"):
            for ix, opin in enumerate(sent.iter('Opinion')):
                if opin.attrib['polarity'] in polar_idx \
                    and int(opin.attrib['from'] )!=int(opin.attrib['to'] ) and opin.attrib['target']!="NULL":
                    corpus.append({"id": sent.attrib['id']+"_"+str(ix), 
                                    "sentence": sent.find('text').text, 
                                    "term": opin.attrib['target'], 
                                    "polarity": opin.attrib['polarity'] })
    return corpus, None


def parse_acsc_SemEval14(fn):
    root=ET.parse(fn).getroot()
    cat2id={}
    for opin in root.iter('aspectCategory'):
        if opin.attrib['polarity'] in polar_idx:
            cat_tag=opin.attrib['category'] 
            if cat_tag not in cat2id:
                cat2id[cat_tag]=len(cat2id)
    print("# of labels", len(cat2id) )
    corpus = []
    for sents in root.iter("sentences"):
        for sent in sents.iter("sentence"):
            cat2polarity = {}
            for opin in sent.iter('aspectCategory'):
                if opin.attrib['polarity'] in polar_idx:
                    cat2polarity[opin.attrib['category']] = opin.attrib['polarity'] 

            corpus.append({"id": sent.attrib['id'], 
                           "sentence": sent.find('text').text, 
                           "cat2polarity": cat2polarity}
                         )
            
    return corpus, {'cat2id': cat2id}

def parse_acsc_SemEval1516(fn):
    root=ET.parse(fn).getroot()
    cat2id={}
    for opin in root.iter('Opinion'):
        if opin.attrib['polarity'] in polar_idx:
            cat_tag=opin.attrib['category'] 
            if cat_tag not in cat2id:
                cat2id[cat_tag]=len(cat2id)
    print("# of labels", len(cat2id) )
    corpus = []
    for review in root.iter("Review"):
        for sent in review.iter("sentence"):
            cat2polarity = {}
            for opin in sent.iter('Opinion'):
                if opin.attrib['polarity'] in polar_idx:
                    cat2polarity[opin.attrib['category']] = opin.attrib['polarity'] 

            corpus.append({"id": sent.attrib['id'], 
                           "sentence": sent.find('text').text, 
                           "cat2polarity": cat2polarity}
                         )

    return corpus, {'cat2id': cat2id}

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
    'acsc': {
        '14': parse_acsc_SemEval14,
        '15': parse_acsc_SemEval1516,
        '16': parse_acsc_SemEval1516
    }
}