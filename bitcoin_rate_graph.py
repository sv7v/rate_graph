'''
Project 'Bitcoin rate graph' (BRG)
См.:
-  https://www.investing.com/crypto/bitcoin/historical-data
'''
from browser        import *
from br_gui         import *

from datetime       import date

class BRG_Doc:
	def __le__(self, other):
		try:
			document <= other
		except TypeError:
			document <= other.get()

doc = BRG_Doc()

class BRG_Decart(BG_Decart):
	def draw_callback(self, s):
		def convertDate(x):
			a = date.fromisoformat(x).timetuple()
			b = a.tm_year
			c = a.tm_yday
			return b+c/366

		def convert(x):
			return map(lambda i: (convertDate(i[0]), float(i[1])), x)

		self.draw(BG_TableFunc(convert(s)))

	def logY_callback(self, checked):
		if checked:
			self.setProp(BG_LogY())
		else:
			self.delProp(BG_LogY())
		self.redraw()

	def bubbleLevel_callback(self, checked):
		if checked:
			self.setRooler(BG_Frame(),
			               BG_Grid(),
			               BG_BubbleLevel(20))
		else:
			self.setRooler(BG_Frame(),
			               BG_Grid())
		self.redraw()

	def fit_callback(self):
		self.fit()
		self.redraw()
#class BRG_Decart(BG_Decart):

class BitcoinRateGraph:
	def __LoadData(self):
		ret = BG_Div()
		ret.inline()
		ret <= 'Файл данных:'
		ret <= BG_LocalTextFile(lambda s:
		                               self._loadData_callback(map(lambda i: i.split(' '),
		                                                           s)))
		return ret

	def __CheckBox(self, text):
		ret = BG_Div()
		ret.inline()
		ret <= str(text)
		cb = BG_CheckBox()
		ret <= cb
		return cb, ret

	def __Header(self):
		ret = BG_Div()
		ret.inline()

		self._logScale, a = self.__CheckBox('Логарифмический масштаб:')
		self._logScale.set()
		ret <= a
		ret <= '. '

		self._bubbleLevel, a = self.__CheckBox('Логарифмический масштаб:')
		ret <= a
		ret <= '. '

		self._dateRate = BG_Div()
		self._dateRate.inline()
		ret <= self._dateRate
		ret <= '. '

		self._dateFrom = BG_Div()
		self._dateFrom.inline()
		ret <= self._dateFrom
		ret <= '. '

		self._dateTo = BG_Div()
		self._dateTo.inline()
		ret <= self._dateTo
		ret <= '. '

		return ret
	#def __Header(self):

	def __Range(self):
		def callback(value):
			self._decart.setProp(BG_Affinis(value))
			self._decart.redraw()

		self._affinis_range = BG_Range(callback)
		self._affinis_range.show(False)

		return self._affinis_range

	def __loadData_callback(self, decart, s):
		decart.draw_callback(s)

		try:
			self._loadData_callback0_done
		except AttributeError:
			self._loadData_callback0_done = True
			self._loadData_callback0(decart, s)
	#def __loadData_callback(self, decart, s):

	def _loadData_callback0(self, decart, s):
		self._header.show()

		verticalRooler  = BG_VerticalRooler(decart)
		leftRightBorder = BG_LeftRightBorder(decart)

		def mouseover(dot_x, dot_y, x, y):
			self._dateRate.setText('Дата: %s, курс: %f' % (str(date.fromtimestamp((x-1970)*
			                                                                      (365.25*24*60*60))),
			                                               y))
			verticalRooler.mouseover(dot_x, x)
			leftRightBorder.mouseover(dot_x, x)

		def mousedrag(dot_x0, dot_y0,
		              dot_x1, dot_y1,
		              x0, y0,
		              x1, y1):
			leftRightBorder.mousedrag(dot_x0, dot_x1, x0, x1)
			date0, date1 = leftRightBorder.get()

			self._dateFrom.setText(date0)
			self._dateTo.setText(date1)

		decart.mouseover(mouseover)
		decart.mousedrag(mousedrag)
	#def _loadData_callback0(self, decart, s):

	def __init__(self):
		doc <= self.__LoadData()

		self._header = self.__Header()
		doc <= self._header
		doc <= html.BR()

		decart = BRG_Decart()
		self._loadData_callback = lambda s: self.__loadData_callback(decart, s)

		self._logScale.setCallback(decart.logY_callback)
		self._bubbleLevel.setCallback(decart.bubbleLevel_callback)

		doc <= decart

		decart.fit()
		doc <= self.__Range()

		window.bind('resize', lambda event: decart.fit_callback())

		if self._logScale.getState():
			decart.setProp(BG_LogY())

		decart.setProp(BG_Affinis(self._affinis_range.getState()))

		decart.setRooler(BG_Frame(),
		                 BG_Grid())
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
