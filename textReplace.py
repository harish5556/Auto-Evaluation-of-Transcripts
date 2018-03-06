import re
replacement_patterns=[
    (r'can\'t','can not'),
    (r'won\'t','will not'),
    (r'i\'m','i am'),
    (r'I\'m','I am'),
    (r'ain\'t','is not'),
    (r'(\w+)\'ll', '\g<1> will'),
    (r'(\w+)n\'t', '\g<1> not'),
    (r'(\w+)\'ve','\g<1> have'),
    (r'(\w+)\'s','\g<1> is'),
    (r'(\w+)\'re','\g<1> are'),
    (r'(\w+)\'d','\g<1> would')
]
class RegexpReplacer(object):
    def __init__(self,patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
    def replace(self, text):
        s=text
        for (pattern, repl) in self.patterns:
            (s,count) = re.subn(pattern, repl, s)
        return s