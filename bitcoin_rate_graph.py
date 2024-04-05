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

	def fit(self):
		self.__canvas.fit()
		self._decart.redraw()

	def draw(self, s):
		self._decart.draw(BG_TableFunc(BitcoinRateGraph._convertData(s)))

	def __init__(self):
		document <= 'Файл данных: '
		document <= BG_LocalTextFile(lambda s: self.draw(s)).get()

		document <= 'Логарифмический масштаб: '
		def checkbox_callback(checked):
			if checked: self._decart.setProp(BG_LogY())
			else:     self._decart.delProp(BG_LogY())
			self._decart.redraw()
		self._logY_checkbox = BG_CheckBox(checkbox_callback)
		document <= self._logY_checkbox.get()
		self._logY_checkbox.set()

		document <= html.BR()

		self.__canvas = BG_HtmlCanvas(1,1)
		document <= self.__canvas.get()
		self.__canvas.fit()

		def affinis_callback(value):
			self._decart.setProp(BG_Affinis(value))
			self._decart.redraw()
		self._affinis_range = BG_Range(affinis_callback)
		document <= self._affinis_range.get()

		window.bind('resize', lambda event:self.fit())

		self._decart = BG_Decart(self.__canvas)

		if self._logY_checkbox.getState():
			self._decart.setProp(BG_LogY())

		self._decart.setProp(BG_Affinis(self._affinis_range.getState()))

		self._decart.setRooler(BG_Frame(),
		                       BG_Grid(),
		                       BG_BubbleLevel(20))
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
