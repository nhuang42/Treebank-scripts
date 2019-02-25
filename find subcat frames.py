"""
http://www.nltk.org/howto/tree.html
### Treebank manual
### http://cs.jhu.edu/~jason/465/hw-parse/treebank-manual.pdf
"""

from nltk.corpus import BracketParseCorpusReader
from nltk import ParentedTree
from nltk.stem import WordNetLemmatizer 
import csv


wnl = WordNetLemmatizer()

def returnStringsInd(string, sentSet):
    j = 0
    for i in sentSet:        
        if string in i:
            print(j)
            j = j+1
            
def joinSent(sent):
    sentStr = ''
    for tag in sent:
        sentStr = sentStr + tag[0] + ' '
    s = sentStr.lower().replace("*pro* ", "")
    return s

def joinLeaves(tree):
    try:
        sentStr = ' '.join(tree.leaves())
    except TypeError:
        sentStr = ''
        for leaves in tree.leaves():
            sentStr = sentStr + leaves[0]
    return sentStr

def joinLeavesIndex(tree, treeIndex):
    try:
        sentStr = ' '.join(tree.leaves())
    except TypeError:
        sentStr = ''
        for leaves in tree.leaves():
            sentStr = sentStr + leaves[0]
        print(treeIndex)
    return sentStr

### file directories
corpus_root = r'C:\Users\znhua\Documents\treebank_3'
file_pattern = r'(.*/)*(.*)\.mrg'

outputfolder = 'C:/Users/znhua/Desktop/'
###


##Penn Treebank: 251827 sentences
#ATIS = 572 sentences
#BROWN = 24243
#SWBD = 177804
#WSJ = 49208

###########################################################
### Verbs whose syntactic environments we are interested in
### Unfortunately, each verb needs to be listed out in all 
### its forms -- bare, past tense, 3rd person singular, gerund
###########################################################
        

verbforms = ["allege", "alleged", "alleges", "alleging", 
"assert", "asserted", "asserts", "asserting", 
"assume", "assumed", "assumes", "assuming", 
"believe", "believed", "believes", "believing", 
"claim", "claimed", "claims", "claiming", 
"conclude", "concluded", "concludes", "concluding", 
"conjecture", "conjectured", "conjectures", "conjecturing", 
"consider", "considered", "considers", "considering", 
"decide", "decided", "decides", "deciding", 
"declare", "declared", "declares", "declaring", 
"deem", "deemed", "deems", "deeming", 
"envisage", "envisaged", "envisages", "envisaging", 
"estimate", "estimated", "estimates", "estimating", 
"expect", "expected", "expects", "expecting", 
"fancy", "fancied", "fancies", "fancying", 
"feel", "felt", "feels", "feeling", 
"figure", "figured", "figures", "figuring", 
"imagine", "imagined", "imagines", "imagining", 
"intimate", "intimated", "intimates", "intimating", 
"judge", "judged", "judges", "judging", 
"maintain", "maintained", "maintains", "maintaining", 
"propose", "proposed", "proposes", "proposing", 
"reckon", "reckoned", "reckons", "reckoning", 
"report", "reported", "reports", "reporting", 
"say", "said", "says", "saying", 
"state", "stated", "states", "stating", 
"suggest", "suggested", "suggests", "suggesting", 
"suppose", "supposed", "supposes", "supposing", 
"suspect", "suspected", "suspects", "suspecting", 
"tell", "told", "tells", "telling", 
"think", "thought", "thinks", "thinking", 

"accept", "accepted", "accepts", "accepting", 
"admit", "admitted", "admits", "admiting", 
"agree", "agreed", "agrees", "agreing", 
"confirm", "confirmed", "confirms", "confirming", 
"deny", "denied", "denies", "denying", 
"verify", "verified", "verifies", "verifying", 

"comment", "commented", "comments", "commenting", 
"convey", "conveyed", "conveys", "conveying", 
"convince", "convinced", "convinces", "convincing", 
"detail", "detailed", "details", "detailing", 
"doubt", "doubted", "doubts", "doubting", 
"emphasize", "emphasized", "emphasizes", "emphasizing", 
"forget", "forgot", "forgets", "forgetting", 
"know", "knew", "knows", "knowing", 
"mention", "mentioned", "mentions", "mentioning", 
"notice", "noticed", "notices", "noticing", 
"point", "pointed", "points", "pointing", 
"realize", "realized", "realizes", "realizing", 
"recall", "recalled", "recalls", "recalling", 
"recognize", "recognized", "recognizes", "recognizing", 
"regret", "regretted", "regrets", "regretting", 
"remember", "remembered", "remembers", "remembering", 
"remind", "reminded", "reminds", "reminding", 

"whisper", "whispered", "whispers", "whispering", 
"shout", "shouted", "shouts", "shouting", 
"yell", "yelled", "yells", "yelling", 
"scream", "screamed", "screams", "screaming", 
"grumble", "grumbled", "grumbles", "grumbling", 
"mutter", "muttered", "mutters", "muttering", 
"lie", "lied", "lies", "lying", 
"mumble", "mumbled", "mumbles", "mumbling", 

"pretend", "pretended", "pretends", "pretending", 
"see", "saw", "sees", "seeing", "seen",
"hear", "heard", "hears", "hearing", 
"announce", "announced", "announces", "announcing", 
"proclaim", "proclaimed", "proclaims", "proclaiming", 
"argue", "argued", "argues", "arguing", 
"concede", "conceded", "concedes", "conceding", 
"utter", "uttered", "utters", "uttering", 
"reveal", "revealed", "reveals", "revealing", 
"insist", "insisted", "insists", "insisting", 
"hope", "hoped", "hopes", "hoping", 
"lie", "lied", "lies", "lying",
"seem","seemed","seems", "seeming",
"sound","sounded", "sounds", "sounding",
"ask","asked", "asks", "asking",

]

###########################################################
### To make it easy to map each verb form to a lemma, I use
### a dictionary. 
### This part of the script is most easily done in Excel
### Formulas can be written to produce this kind of code
###########################################################

verbdict = {
        "allege": "vs-allege","alleged": "vs-allege","alleges": "vs-allege","alleging": "vs-allege",
"assert": "vs-assert","asserted": "vs-assert","asserts": "vs-assert","asserting": "vs-assert",
"assume": "vs-assume","assumed": "vs-assume","assumes": "vs-assume","assuming": "vs-assume",
"believe": "vs-believe","believed": "vs-believe","believes": "vs-believe","believing": "vs-believe",
"claim": "vs-claim","claimed": "vs-claim","claims": "vs-claim","claiming": "vs-claim",
"conclude": "vs-conclude","concluded": "vs-conclude","concludes": "vs-conclude","concluding": "vs-conclude",
"conjecture": "vs-conjecture","conjectured": "vs-conjecture","conjectures": "vs-conjecture","conjecturing": "vs-conjecture",
"consider": "vs-consider","considered": "vs-consider","considers": "vs-consider","considering": "vs-consider",
"decide": "vs-decide","decided": "vs-decide","decides": "vs-decide","deciding": "vs-decide",
"declare": "vs-declare","declared": "vs-declare","declares": "vs-declare","declaring": "vs-declare",
"deem": "vs-deem","deemed": "vs-deem","deems": "vs-deem","deeming": "vs-deem",
"envisage": "vs-envisage","envisaged": "vs-envisage","envisages": "vs-envisage","envisaging": "vs-envisage",
"estimate": "vs-estimate","estimated": "vs-estimate","estimates": "vs-estimate","estimating": "vs-estimate",
"expect": "vs-expect","expected": "vs-expect","expects": "vs-expect","expecting": "vs-expect",
"fancy": "vs-fancy","fancied": "vs-fancy","fancies": "vs-fancy","fancying": "vs-fancy",
"feel": "vs-feel","felt": "vs-feel","feels": "vs-feel","feeling": "vs-feel",
"figure": "vs-figure","figured": "vs-figure","figures": "vs-figure","figuring": "vs-figure",
"imagine": "vs-imagine","imagined": "vs-imagine","imagines": "vs-imagine","imagining": "vs-imagine",
"intimate": "vs-intimate","intimated": "vs-intimate","intimates": "vs-intimate","intimating": "vs-intimate",
"judge": "vs-judge","judged": "vs-judge","judges": "vs-judge","judging": "vs-judge",
"maintain": "vs-maintain","maintained": "vs-maintain","maintains": "vs-maintain","maintaining": "vs-maintain",
"propose": "vs-propose","proposed": "vs-propose","proposes": "vs-propose","proposing": "vs-propose",
"reckon": "vs-reckon","reckoned": "vs-reckon","reckons": "vs-reckon","reckoning": "vs-reckon",
"report": "vs-report","reported": "vs-report","reports": "vs-report","reporting": "vs-report",
"say": "vs-say","said": "vs-say","says": "vs-say","saying": "vs-say",
"state": "vs-state","stated": "vs-state","states": "vs-state","stating": "vs-state",
"suggest": "vs-suggest","suggested": "vs-suggest","suggests": "vs-suggest","suggesting": "vs-suggest",
"suppose": "vs-suppose","supposed": "vs-suppose","supposes": "vs-suppose","supposing": "vs-suppose",
"suspect": "vs-suspect","suspected": "vs-suspect","suspects": "vs-suspect","suspecting": "vs-suspect",
"tell": "vs-tell","told": "vs-tell","tells": "vs-tell","telling": "vs-tell",
"think": "vs-think","thought": "vs-think","thinks": "vs-think","thinking": "vs-think",

"accept": "rs-accept","accepted": "rs-accept","accepts": "rs-accept","accepting": "rs-accept",
"admit": "rs-admit","admitted": "rs-admit","admits": "rs-admit","admiting": "rs-admit",
"agree": "rs-agree","agreed": "rs-agree","agrees": "rs-agree","agreing": "rs-agree",
"confirm": "rs-confirm","confirmed": "rs-confirm","confirms": "rs-confirm","confirming": "rs-confirm",
"deny": "rs-deny","denied": "rs-deny","denies": "rs-deny","denying": "rs-deny",
"verify": "rs-verify","verified": "rs-verify","verifies": "rs-verify","verifying": "rs-verify",



"comment": "ns-comment","commented": "ns-comment","comments": "ns-comment","commenting": "ns-comment",
"convey": "ns-convey","conveyed": "ns-convey","conveys": "ns-convey","conveying": "ns-convey",
"convince": "ns-convince","convinced": "ns-convince","convinces": "ns-convince","convincing": "ns-convince",
"detail": "ns-detail","detailed": "ns-detail","details": "ns-detail","detailing": "ns-detail",
"doubt": "ns-doubt","doubted": "ns-doubt","doubts": "ns-doubt","doubting": "ns-doubt",
"emphasize": "ns-emphasize","emphasized": "ns-emphasize","emphasizes": "ns-emphasize","emphasizing": "ns-emphasize",
"forget": "ns-forget","forgot": "ns-forget","forgets": "ns-forget","forgetting": "ns-forget",
"know": "ns-know","knew": "ns-know","knows": "ns-know","knowing": "ns-know",
"mention": "ns-mention","mentioned": "ns-mention","mentions": "ns-mention","mentioning": "ns-mention",
"notice": "ns-notice","noticed": "ns-notice","notices": "ns-notice","noticing": "ns-notice",
"point": "ns-point out","pointed": "ns-point out","points": "ns-point out","pointing": "ns-point out",
"realize": "ns-realize","realized": "ns-realize","realizes": "ns-realize","realizing": "ns-realize",
"recall": "ns-recall","recalled": "ns-recall","recalls": "ns-recall","recalling": "ns-recall",
"recognize": "ns-recognize","recognized": "ns-recognize","recognizes": "ns-recognize","recognizing": "ns-recognize",
"regret": "ns-regret","regretted": "ns-regret","regrets": "ns-regret","regretting": "ns-regret",
"remember": "ns-remember","remembered": "ns-remember","remembers": "ns-remember","remembering": "ns-remember",
"remind": "ns-remind","reminded": "ns-remind","reminds": "ns-remind","reminding": "ns-remind",

"whisper": "ms-whisper","whispered": "ms-whisper","whispers": "ms-whisper","whispering": "ms-whisper",
"shout": "ms-shout","shouted": "ms-shout","shouts": "ms-shout","shouting": "ms-shout",
"yell": "ms-yell","yelled": "ms-yell","yells": "ms-yell","yelling": "ms-yell",
"scream": "ms-scream","screamed": "ms-scream","screams": "ms-scream","screaming": "ms-scream",
"grumble": "ms-grumble","grumbled": "ms-grumble","grumbles": "ms-grumble","grumbling": "ms-grumble",
"mutter": "ms-mutter","muttered": "ms-mutter","mutters": "ms-mutter","muttering": "ms-mutter",
"mumble": "ms-mumble","mumbled": "ms-mumble","mumbled": "ms-mumble","mumbling": "ms-mumble",

"pretend": "ot-pretend","pretended": "ot-pretend","pretends": "ot-pretend","pretending": "ot-pretend",
"see": "ot-see","saw": "ot-see","sees": "ot-see","seeing": "ot-see", "seen": "ot-see",
"hear": "ot-hear","heard": "ot-hear","hears": "ot-hear","hearing": "ot-hear",
"announce": "ot-announce","announced": "ot-announce","announces": "ot-announce","announcing": "ot-announce",
"proclaim": "ot-proclaim","proclaimed": "ot-proclaim","proclaims": "ot-proclaim","proclaiming": "ot-proclaim",
"argue": "ot-argue","argued": "ot-argue","argues": "ot-argue","arguing": "ot-argue",
"concede": "ot-concede", "conceded": "ot-concede", "concedes": "ot-concede", "conceding": "ot-concede", 
"utter": "ot-utter", "uttered": "ot-utter", "utters": "ot-utter", "uttering": "ot-utter", 
"reveal": "ot-reveal", "revealed": "ot-reveal", "reveals": "ot-reveal", "revealing": "ot-reveal", 
"insist": "ot-insist", "insisted": "ot-insist", "insists": "ot-insist", "insisting": "ot-insist", 
"hope": "ot-hope", "hoped": "ot-hope", "hopes": "ot-hope", "hoping": "ot-hope", 
"lie": "os-lie","lied": "os-lie","lies": "os-lie","lying": "os-lie",
"seem": "os-seem","seemed": "os-seem","seems": "os-seem","seeming": "os-seem",
"sound": "os-sound","sounded": "os-sound","sounds": "os-sound","sounding": "os-sound",
"ask": "os-ask","asked": "os-ask","asks": "os-ask","asking": "os-ask",
     }

ptb = BracketParseCorpusReader(corpus_root, file_pattern, 
                               #encoding='utf-8'
                               encoding='iso-8859-1'
                               )
ptbS = ptb.parsed_sents()

    
def getClauseHead(st):
    clauseHead = ''
    # delete disfluencies at the S level
    for daughter in st:
        if daughter.label() in ['EDITED', 'RS', 'PRN', '-DFL-', 'CONJP', 'ADVP']: # including "not only ..."
            del daughter
    #print(joinLeaves(st), st.label())
    if st[0].label()[:2] == 'WH' and joinLeaves(st[0]).lower() == '0':
        clauseHead = 'whNull'
    i = 0
    while clauseHead == '' and i < min(2, len(st)):
        if (st[i].label()[:2] == 'WH' and joinLeaves(st[i]).lower() != '0'):
            clauseHead = 'q-whOvert'
        i += 1
    if st[0].label()[:2] in ['IN', 'CC'] and joinLeaves(st[0]).lower() == 'whether':
        clauseHead = 'q-whether'
    if st[0].label()[:2] == 'IN' and joinLeaves(st[0]).lower() == 'if':
        clauseHead = 'q-if'
    if st[0].label()[:2] == 'IN' and joinLeaves(st[0]).lower() == 'for' and st[1].label()[0] == 'S':
        clauseHead = 'for'
    if (st[0].label()[:2] in ['WDT', 'DT', 'IN', 'RB', 'NONE'] and joinLeaves(st[0]).lower() == 'that' 
        #and (st[1].label()[0] == 'S' or st[1].label()[0] == ',') #sometimes we have commas intervening between "that" and the clause
            ):
        clauseHead = 'd-that'
    if st[0].label()[:2] == 'IN' and joinLeaves(st[0]).lower() == 'like':
        clauseHead = 'd-like'
    if st[0].label()== '-NONE-' and joinLeaves(st[0]).lower() == '0':
        clauseHead = 'd-0'
    if st[0].label() == '-NONE-' and joinLeaves(st[0])[:3] == '*T*':
        clauseHead = 'slifting'
    if len(st) == 2 and st.leaves()[0] == '0' and st[1].leaves()[0][:3] == '*T*' and len(st[1]) == 1:
        clauseHead = 'slifting-0' # some slifting examples are "0 *T*-XXX"
    if len(st) > 1:
        if (st[0].label()[:2] in ['IN', 'RB'] and joinLeaves(st[0]).lower() == 'as'
            and (st[1].label()[:2] in ['IN', 'RB'] and joinLeaves(st[1]).lower() == 'if'
                 or st[1].label()[:2] in ['IN', 'RB'] and joinLeaves(st[1]).lower() == 'though')):
            clauseHead = 'd-asif/though'
    return clauseHead

def getQuote(st, leftSibStr):
    quote = ''
    if leftSibStr in ["``", "`", "'","''"]:
        quote = 'quote'
    return quote

def checkConjoined(st, label):
    stUse = st
    hasCoord = False
    for i in range(len(st)):
        if (i > 0 and st[0].label().startswith(label) and 
            st[i].label() in ['CC', 'CONJP', 'ADVP', # and, rather than, then
              ':', ',', ';', 'PRN', 'EDITED', 'RS', '.', 
              'VP','NP', 'SBAR-ADV' #appositives
              ] # We want to avoid instances where "whether" is coded as CC and is at the start of S
            ):
            hasCoord = True
    if hasCoord:
        try:
            #If so, take the first daughter S for clauseHead and finiteness marking
            stUse = next(daughter for daughter in st if daughter.label().startswith(label))
        except StopIteration:
            pass
    return stUse

def getFinite(st, verbLabs, verbStrs):
    for daughter in st:
        #print(daughter.label(), joinLeaves(daughter))
        if daughter.label()[:2] == 'VP':
            daughterUse = checkConjoined(daughter, 'VP')
            for gd in daughterUse:
                #print(joinLeaves(daughter))
                verbLabs.append(gd.label())
                verbStrs.append(joinLeaves(gd))
        elif len(daughter)>1:
            verbLabs, verbStrs = getFinite(daughter, verbLabs, verbStrs)
    #print(joinLeaves(st), verbLabs, verb)
    return verbLabs, verbStrs

def getParent(parent, s):
    parentHead = parent
    for child in parent:
        if joinLeaves(child) == 'it':
            s['it'] = True
        #this gets us the first sibling that shares the same initial letter as the parent, so first V in VP, first N in NP etc.
        if child.label()[0] == parent.label()[0] and parent.label()[:2] != 'AD': 
            parentHead = child
            
        elif parent.label()[:2] == 'AD':
            try:
                parentHead = next(daughter for daughter in parent if daughter.label() in ['JJ', 'JJR', 'JJS', 'VBN', 'VBG'])
            except StopIteration:
                try: 
                    #print(joinLeaves(parent[0]), parent[0].label())
                    parentHead = next(gd for gd in parent[0] if (
                            gd.label() in ['JJ', 'JJR', 'JJS', 'VBN', 'VBG'] 
                            or (gd.label() in ['RB', 'RBR', 'RBS']
                               and joinLeaves(gd).lower() not in ['not', 'so', 'as']
                            )))
                except StopIteration:
                    try:
                        parentHead = next(daughter for daughter in parent if daughter.label() in ['RB', 'RBR', 'RBS']
                                      and joinLeaves(daughter).lower() not in ['not', 'so', 'as']
                                      )
                    except StopIteration:
                        pass
        s['parentHeadLab'] = parentHead.label()
        s['parentHeadStr'] = joinLeaves(parentHead)

def hasItem(string, listOfItems):
    hasItem = False
    for item in listOfItems:
        if item in string:
            hasItem = True
    return hasItem

adjunctTags = ['EDITED', 'RS', 'PRN', '-DFL-', 
            'ADV',
            '-LRB', '-RRB', '.', '-',
            '-LOC', '-TMP', '-MNR', '-PRP'
            ':', ]


## GET syntactic environments, etc.
def verbFrames(treebank = ptbS, verbforms = verbforms, verbdict = verbdict):
    treeIndex = 0
    allLabelLeaves = []
    
    # Trees 0-571 are sentences related to air travel inquiries (formulaic)
    # and in a slightly different tree format
    for tree in ptbS[572:]:
        tr = ParentedTree.convert(tree)
        treeStr = joinLeaves(tr)
        for st in tr.subtrees():
            # Flags for annotating slifting / quotative inversion
            # and expletive it
            vSeen = 0
            itSeen = 0
            stleaf = joinLeaves(st)
            
            if stleaf in verbforms and st.label()[0] == 'V' and st.label() != 'VP':
                
                
                s = dict()
                s['treeIndex'] = treeIndex
                s['s'] = treeStr
                s['parentLab'] = st.parent().label().split("-")[0]
                s['verbLab'] = st.label()
                s['verbLemma'] = verbdict[stleaf]
                # These are all the sisters of the verb
                s['verbSynEnvFull'] = ''
                s['verbSynEnvFullStr'] = ''
                # These are the sisters of the verbs, after eliminating what looks like adjuncts or corrections
                # Therefore: likely to be subcategorization frames
                s['verbSubcat'] = ''
                s['verbSubcatStr'] = ''
                # If there is a clause: what kind of clause is it? S, SBAR, ...?
                s['sType'] = ''
                # What kind of "head" does the clause have? Is it interrogative, declarative, has a "that" or "if"...?
                s['clauseHead'] = ''
                # What is the label of the highest verb? A proxy for finiteness
                s['embVerbLabel'] = ''
                # What is the highest verb?
                s['embVerb'] = ''
                
                for d in st.parent():
                    # Update flags
                    if d.label()[0] == "V":
                        vSeen = 1
                    if joinLeaves(d) == "it":
                        itSeen = 1
                    # Generate output
                    s['verbSynEnvFull'] += d.label() + "~~"
                    s['verbSynEnvFullStr'] += joinLeaves(d) + "~~"
                
                    # Generate an "abbreviated" output without certain adjuncts
                    if ("MNR" not in d.label() 
                        and "TMP" not in d.label()
                        and "TPC" not in d.label() # 'as NP' 'in light of NP'
                        and "PRP" not in d.label()
                        and "ADV" not in d.label()
                        and "LOC" not in d.label()
                        and "EDITED" not in d.label()
                        and "$" not in d.label()
                        and "NAC" not in d.label() # asides and hedges like "but not very much"
                        and "CC" not in d.label() # 'but/and'
                        and "INTJ" not in d.label() # 'God!'
                        and "PRN" not in d.label() # 'you know'
                        and "SEZ" not in d.label() # 'you know'
                        and "RB" not in d.label() # '... *well* convinced that..
                        and d.label() != "-DFL" # uh, you know, ...
                        and d.label() not in [",", ":", "''", "."]
                        ):
                        if d.label()[:2] == 'VB':
                            s['verbSubcat'] += 'VB' + "~~"
                            s['verbSubcatStr'] += joinLeaves(d) + "~~"
                        
                        elif d.label()[:2] == 'NP':
                            s['verbSubcat'] += 'NP' + "~~"
                            s['verbSubcatStr'] += joinLeaves(d) + "~~"
    
                        elif d.label()[0] =="S":
                            # Add flags
                            s['verbSubcat'] += d.label().split('-')[0] + "~~"
                            s['verbSubcatStr'] += joinLeaves(d) + "~~"
    
                            if ((joinLeaves(d)[:4] == "*T*-"
                                     and len(d) == 1)
                                or (len(d) == 2 and
                                    joinLeaves(d[1])[0] == "0" and
                                    joinLeaves(d[1])[:4] == "*T*-"
                                    )
                                ):
                                # Slifting
                                s['verbSubcat'] += "sl"
                            if (itSeen == 1
                                    ):
                                # "it" expletive
                                s['verbSubcat'] += "it"
                                
                            
                            # if S is not a trace or dominating a single lex item
                            if len(d) > 1:
                                                            
                                stUse = checkConjoined(d, 'S')
                                
                                # Identify the type of clause, first-pass
                                s['clauseHead'] = getClauseHead(stUse)
                                s['sType'] = stUse.label()
                                # Mark the sentence for finiteness -- get a list of verbs and their labels
                                verbLabs, verbStrs = getFinite(stUse, [], [])
        
                                if len(verbLabs) > 0:
                                    if verbLabs[0] in ['MD', 'TO', 'BES'] or verbLabs[0][0] == 'V':
                                        s['embVerbLabel'] = verbLabs[0]
                                    s['embVerb'] = verbStrs[0]
                                
                        else:
                            s['verbSubcat'] += d.label() + "~~"
                            s['verbSubcatStr'] += joinLeaves(d) + "~~"
    
                
                allLabelLeaves.append(s)
        treeIndex +=1
    return allLabelLeaves

outputDict = verbFrames()

# Save output as a txt file
with open(outputfolder + 'ptb-scomp2.txt', 'w', encoding = 'utf8') as f:  # Just use 'w' mode in 3.x
    columnLabels = list(outputDict[0].keys())
    writer = csv.DictWriter(f, fieldnames=columnLabels)
    writer.writeheader()
    for cfList in outputDict:
        writer.writerow(cfList)