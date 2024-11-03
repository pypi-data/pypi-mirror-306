# Author: Scott Woods <scott.18.ansar@gmail.com>
# MIT License
#
# Copyright (c) 2017-2023 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""General coding support.

Classes and functions that may be useful in any
Python development, i.e. not dependent on Ansar.
"""

__docformat__ = 'restructuredtext'

import sys
import uuid
import ansar.encode as ar

__all__ = [
	'cannot',
	'lor',
	'stream_word',
	'recover_word',
]

def cannot(line, newline=True, **kv):
	"""Place an error diagnostic on stderr, including the executable name."""
	if kv:
		t = line.format(**kv)
	else:
		t = line

	h = ar.program_name
	sys.stderr.write(h)
	sys.stderr.write(': ')
	sys.stderr.write(t)
	if newline:
		sys.stderr.write('\n')

#
#
def lor(a, max=32, separator=', '):
	t = 0
	for i, s in enumerate(a):
		t += len(s) + 2
		if t > max:
			# Output getting too long. Compose
			# an abbreviation.
			s = ', '.join(a[:i + 1])
			return f'{s} ... ({len(a)})'
	# No overflow including the
	# empty list.
	return separator.join(a)

#
#
D2W = {
	ar.Boolean:		lambda d: 'true' if d else 'false',
	ar.Character:	lambda d: d,
	ar.Rune:		lambda d: d,
	ar.Integer2:	lambda d: str(d),
	ar.Integer4:	lambda d: str(d),
	ar.Integer8:	lambda d: str(d),
	ar.Byte:		lambda d: str(d),
	ar.Unsigned2:	lambda d: str(d),
	ar.Unsigned4:	lambda d: str(d),
	ar.Unsigned8:	lambda d: str(d),
	ar.Float4:		lambda d: str(d),
	ar.Float8:		lambda d: str(d),
	ar.String:		lambda d: d,
	ar.Unicode:		lambda d: d,
	ar.ClockTime:	lambda d: ar.clock_to_text(d),
	ar.WorldTime:	lambda d: ar.world_to_text(d),
	ar.TimeSpan:	lambda d: ar.span_to_text(d),
	ar.TimeDelta:	lambda d: ar.delta_to_text(d),
	ar.UUID:		lambda d: str(d),
}

def stream_word(v, d):
	c = D2W.get(type(v), None)
	if c:
		return c(d)
	return None

# Auto conversion of a representation in a form to
# a member in an object.

W2D = {
	ar.Boolean:		lambda s: s == 'true',
	ar.Character:	lambda s: s,
	ar.Rune:		lambda s: s,
	ar.Integer2:	lambda s: int(s),
	ar.Integer4:	lambda s: int(s),
	ar.Integer8:	lambda s: int(s),
	ar.Byte:		lambda s: int(s),
	ar.Unsigned2:	lambda s: int(s),
	ar.Unsigned4:	lambda s: int(s),
	ar.Unsigned8:	lambda s: int(s),
	ar.Float4:		lambda s: float(s),
	ar.Float8:		lambda s: float(s),
	ar.String:		lambda s: s,
	ar.Unicode:		lambda s: s,
	ar.ClockTime:	lambda s: ar.text_to_clock(s),
	ar.WorldTime:	lambda s: ar.text_to_world(s),
	ar.TimeSpan:	lambda s: ar.text_to_span(s),
	ar.TimeDelta:	lambda s: ar.text_to_delta(s),
	ar.UUID:		lambda s: uuid.UUID(s),
}

def recover_word(v, d):
	c = W2D.get(type(v), None)
	if c:
		return c(d)
	return None
