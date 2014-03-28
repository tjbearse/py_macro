


    
class ParseException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

''' Grammar
# LIST => TERM LIST | TERM
# TERM => SEQ | REP
# SEQ => ITEM SEQ | ITEM
# REP => (<num>, LIST)
# ITEM => MOD {vk_name} | MOD <alpha_num> | "QUOTE
# MOD => \u(p) | \d(own) | <blank>
# QUOTE => <alpha_num> QUOTE | "
'''
   
# A A A...
def ParseLevel1(text, list):
    while len(text):
        text = ParseLevel2(text, list)

# 
def ParseLevel2(text, list):
    c = text.pop()
    while c != '{' and len(text):
        if c == '\\':
            text = ParseEscape(text, list)
        elif c.isalphanum():
            ParseChar(c, list)
    return text


""" Parses: \vkCode_name
returns text after escape sequence
appends KeyBdInput items to list
"""     
def ParseEscape(text, list):
    ''

# single char, appends to list
def ParseChar(text, list):
    ''