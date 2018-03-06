grammar="""
S -> NP VP | VP NP |NP VP CC S | EX VP |
VP -> V NP | RB |V NP PP | V | V PP | V VP | V ADJP | V S | null
ADJP -> RB ADJP|RB JJ PP | RB JJ |RB JJ S | JJ CC ADJP | JJ
PP -> P NP PP| TO NP PP | P NP | TO VP | P VP
NP -> Det N NP | Det N | Det N PP | CNP |N NP | N | Det JJ NP |N NP | N VP | JJ NP 
CNP -> N CC N
V -> 'VBD'|'VBZ'|'WRB'|'VB' |'VBP' |'VBN' | 'VBG' | 'MD' | 'DT'
RB -> 'RB' | 'RBR' | 'RBS' 
Det -> 'DT' | 'WDT' 
N -> 'NN'|'NNP' | 'WP$' |'WP' |'PRP$' |'PRP' | 'JJ' | 'WP' | 'NNS' | null
P -> 'PP' |'IN' | 'RP' | null
EX -> 'EX'
TO -> 'TO'
CC -> 'CC'
JJ -> 'JJ' | 'JJS' | 'CD'
"""