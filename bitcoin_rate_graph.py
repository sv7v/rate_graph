'''
Project 'Bitcoin rate graph' (BRG)
См.:
-  https://www.investing.com/crypto/bitcoin/historical-data
'''
from browser        import *
from br_gui         import *

from datetime       import date

class BitcoinRateGraph:
	def fit(self):
		self.__canvas.fit()
		self._decart.redraw()

	def draw(self, s):
		def convertDate(x):
			a = date.fromisoformat(x).timetuple()
			b = a.tm_year
			c = a.tm_yday
			return b+c/366

		def convert(x):
			return map(lambda i: (convertDate(i[0]), float(i[1])), x)

		self._decart.draw(BG_TableFunc(convert(s)))

		self._log_div.show()
		self._affinis_range.show()

		self._decart.mousemove(lambda x, y: self.date_div.setText(' Дата: %s, курс: %f.' % (str(date.fromtimestamp((x-1970)*
		                                                                                                          (365.25*24*60*60))),
		                                                                                   y)))

	def __init__(self):
		document <= 'Файл данных: '
		document <= BG_LocalTextFile(lambda s:
		                                    self.draw(map(lambda i:
		                                                         i.split(' '),
		                                                  s))).get()

		self._log_div = BG_Div()
		self._log_div.show(False)
		document <= self._log_div.get()

		self._log_div <= 'Логарифмический масштаб: '

		def checkbox_callback(checked):
			if checked: self._decart.setProp(BG_LogY())
			else:       self._decart.delProp(BG_LogY())
			self._decart.redraw()
		logY_checkbox = BG_CheckBox(checkbox_callback)
		logY_checkbox.set()

		self._log_div <= logY_checkbox

		date_div = BG_Div()
		self._log_div <= date_div

		document <= html.BR()

		self.__canvas = BG_HtmlCanvas(1,1)
		document <= self.__canvas.get()
		self.__canvas.fit()

		def affinis_callback(value):
			self._decart.setProp(BG_Affinis(value))
			self._decart.redraw()
		self._affinis_range = BG_Range(affinis_callback)
		self._affinis_range.show(False)

		document <= self._affinis_range.get()

		window.bind('resize', lambda event:self.fit())

		self._decart = BG_Decart(self.__canvas)

		if logY_checkbox.getState():
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
