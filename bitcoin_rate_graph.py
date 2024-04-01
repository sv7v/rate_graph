'''
Project 'Bitcoin rate graph' (BRG)
См.:
-  https://www.investing.com/crypto/bitcoin/historical-data
'''
from browser        import *
from br_gui         import *

from datetime       import date
from io             import StringIO

class BitcoinRateGraph:
	def _convertData(s):
		with StringIO(s) as f:
			for i in f.readlines():
				d, r = i.split(' ')
				a = date.fromisoformat(d).timetuple()
				b = a.tm_year
				c = a.tm_yday
				yield (b+c/366,
				       float(r))

	def _readData(self, s):
		canvas = BG_HtmlCanvas(640, 480)
		document <= canvas.get()
		self._decart  = BG_Decart(canvas, (BG_LogY()), BG_Frame())
		self._bitcoin = BG_TableFunc(BitcoinRateGraph._convertData(s))
		self._decart.draw(self._bitcoin)

	def redraw(self):
		print(820)
		self._decart.setProp(BG_LogY() if self._checkbox.getState() else ())
		self._decart.redraw(self._bitcoin)

	def __init__(self):
		document <= 'Файл данных: '
		document <= BG_LocalTextFile(self._readData).get()

		document <= 'Логарифмический масштаб:'
		self._checkbox = BG_CheckBox(lambda event: self.redraw())
		document <= self._checkbox.get()
		self._checkbox.set()
#class BitcoinRateGraph:

def main():
	BitcoinRateGraph()

if __name__ == "__main__":
	try:
		from traceback  import format_exc
		main()
	except Exception:
		document <= html.HR()
		document <= 'Fatal error: uncaught exception:'
		p = html.PRE(format_exc())
		document <= p
		window.scrollBy(0,  p.getBoundingClientRect().top
		                  - document.documentElement.clientHeight
		                  + p.offsetHeight
		                  + 8)
		alert('Fatal error: uncaught exception')