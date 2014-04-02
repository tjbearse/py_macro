
import vkCodes as vk
from sendInputs import mkKey, KeyBdInput, run, runSlow
import string
from time import sleep
    
class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def Parse(text):
    l = list()
    ParseList(text, l)
    return l
    

''' Grammar
LIST => TERM LIST | TERM
TERM => SEQ | (REP)
SEQ => ITEM SEQ | ITEM
REP => <num>, LIST
ITEM => {SPEC} | <alpha_num> | "QUOTE
SPEC => vkname/action (params)
QUOTE => <alpha_num> QUOTE | "
'''

   
""" Takes care of:
LIST => TERM LIST | TERM
TERM => SEQ | (REP)
"""
def ParseList(text, keys):
    while len(text):
        if text[0] == '(':
            
            try:
                index = GetRightParen(text)
            except ValueError:
                raise ParseError('mismatched parens')
            ParseRep(text[1:index], keys)
            text = text[index + 1:]
        else:
            index = GetLeftParen(text)
            ParseSeq(text[0:index], keys)
            text = text[index:]

""" returns index of first outer right paren
requires matched parens
"""
def GetRightParen(text):
    i = 0
    left_paren = 0
    while i < len(text):
        if text[i] == '\\' :
            i += 1  # skip escaped
        elif text[i] == ')':
            if left_paren == 1:
                return i
            else:
                left_paren -= 1
        elif text[i] == '(':
            left_paren += 1
        i += 1
    raise ValueError

def GetLeftParen(text):
    i = 0
    while i < len(text):
        if text[i] == '\\':
            i += 1
        elif text[i] == '(':
            return i
        i += 1
    return len(text)

"""
REP => <num>, LIST
"""
def ParseRep(text, keys):
    try:
        index = text.index(',')
    except ValueError:
        raise ParseError('no comma in repeat term')
    try:
        num = int(float(text[:index]))
    except ValueError:
        raise ParseError('invalid number in repeat term')
    
    if num <= 0:
        raise ParseError('must be a positive number in repeat term')
    
    tmp_keys = list()
    ParseList(text[index + 1:], tmp_keys)
    keys.extend(tmp_keys * num)

"""
SEQ => ITEM SEQ | ITEM
ITEM => {SPEC} | <alpha_num> | "QUOTE
"""
def ParseSeq(text, keys):
    i = 0
    while i < len(text):
        escaped = False
        if text[i] == '"':
            try:
                index = (text[i + 1:].index('"'))
                ParseQuote(text[i + 1: i + index + 1], keys)
                i += index + 1
            except ValueError:
                raise ParseError("mismatched quotes")
        elif text[i] != ' ':
            escaped = 0;
            if text[i] == '\\':
                escaped = True
                i += 1  # move to escaped char
            
            try:
                if text[i] == '{' and not escaped:
                    index = (text[i:]).index('}')
                    ParseSpec(text[i + 1: i + index], keys)
                    i = i + index
                else:
                    ParseChar(text[i], keys)  # TODO: have shifting disabled?
            
            except IndexError:
                raise ParseError("invalid escape sequence")
            except ValueError:
                raise ParseError("mismatched braces '{ }' ")
            
        i += 1

""" parse a special sequence
SPEC => vkname/action (params)
"""
def ParseSpec(text, keys):
    words = (text.upper()).split()
    if words[0] in vk.Codes.keys():
        if len(words) > 1:
            if words[1] == "UP":
                keys.append(mkKey(vk=vk.Codes[words[0]], flag=KeyBdInput.KeyUp))
            elif words[1] == "DOWN":
                keys.append(mkKey(vk=vk.Codes[words[0]], flag=0))
            else:
                raise ParseError("invalid option" + words[1])
        else:
            keys.append(mkKey(vk=vk.Codes[words[0]], flag=0))
            keys.append(mkKey(vk=vk.Codes[words[0]], flag=KeyBdInput.KeyUp))
    else:
        raise ParseError("keyword " + words[0] + "?")

""" parse a character literally (no escapes etc)
"""
def ParseChar(char, keys):
    shift = False  # TODO: get keyboard state
    if char == ' ':
        vkcode = vk.Codes['SPACE']
        keys.append(mkKey(vk=vkcode, flag=0))
        keys.append(mkKey(vk=vkcode, flag=KeyBdInput.KeyUp))
    elif char in string.ascii_lowercase or char in string.digits:
        if shift:
            keys.append(mkKey(vk=vk.Codes['SHIFT'], flag=KeyBdInput.KeyUp))
            keys.append(mkKey(vk=ord(char.upper()), flag=0))
            keys.append(mkKey(vk=ord(char.upper()), flag=KeyBdInput.KeyUp))
        else:
            keys.append(mkKey(vk=ord(char.upper()), flag=0))
            keys.append(mkKey(vk=ord(char.upper()), flag=KeyBdInput.KeyUp))
    elif char in string.ascii_uppercase:
        if shift:
            keys.append(mkKey(vk=ord(char), flag=0))
            keys.append(mkKey(vk=ord(char), flag=KeyBdInput.KeyUp))
        else:
            keys.append(mkKey(vk=vk.Codes['SHIFT'], flag=0))
            keys.append(mkKey(vk=ord(char), flag=0))
            keys.append(mkKey(vk=ord(char), flag=KeyBdInput.KeyUp))
    elif char in string.punctuation:
        # TODO: do punctuation
        print "punctuation char: ", char
    else:
        print "unknown char: ", char

def ParseQuote(text, keys):
    for c in text:
        ParseChar(c, keys)










