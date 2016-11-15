import re

class RegexHelper:

	@staticmethod
	def containsMD(body):
		heading = r'\W#{1,6}\s'
		emphasis1 = r'\*{1,2}[\s\S]+\*{1,2}'
		emphasis2 = r'_{1,2}[\s\S]+_{1,2}'
		emphasis3 = r'~~[\s\S]+~~'
		superscript = r'\w\^\w'
		unordered = r'\W[\*\-\+]\s\S'
		ordered = r'\W\d\.\s\S'
		url = r'\[[\s\S]+\]\(http[s]?://[\w/\.&=\?;\+\-]+\)'
		code = r'`[\s\S]+`'
		quote = r'(&gt;){1,2}[\s\S]+'

		return (re.search(heading, body) is not None
			or re.search(emphasis1, body) is not None
			or re.search(emphasis2, body) is not None
			or re.search(emphasis3, body) is not None
			or re.search(superscript, body) is not None
			or re.search(unordered, body) is not None
			or re.search(ordered, body) is not None
			or re.search(url, body) is not None
			or re.search(code, body) is not None
			or re.search(quote, body) is not None)