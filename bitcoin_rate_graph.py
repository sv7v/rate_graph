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
		self._decart  = BG_Decart(self.__canvas, (BG_LogY(), BG_Affinis(-0.31)), BG_Frame(), BG_Grid(), BG_BubbleLevel(10))
		self._bitcoin = BG_TableFunc(BitcoinRateGraph._convertData(s))
		self._decart.draw(self._bitcoin, BG_Space(2020, 1e4, 2028, 1e6))

	def redraw(self):
		self._decart.setProp((BG_LogY() if self._checkbox.getState() else (), BG_Affinis(-0.3)))
		self._decart.redraw(self._bitcoin, BG_Space(2020, 1e4, 2028, 1e6))

	def __init__(self):
		document <= 'Файл данных: '
		document <= BG_LocalTextFile(self._readData).get()

		document <= 'Логарифмический масштаб:'
		self._checkbox = BG_CheckBox(lambda event: self.redraw())
		document <= self._checkbox.get()
		self._checkbox.set()

		document <= html.BR()

		self.__canvas = BG_HtmlCanvas(640, 480)
		document <= self.__canvas.get()
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
