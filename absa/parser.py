import xml.etree.ElementTree as ET

from .config import polar_idx

def parse_acsc_SemEval16(fn):
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
            
    return corpus, cat2id

parser_config={
    'acsc': {
        '16': parse_acsc_SemEval16
    }
}