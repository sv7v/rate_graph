'''
Project 'Bitcoin rate graph' (BRG)
См.:
-  https://www.investing.com/crypto/bitcoin/historical-data
'''
from browser        import *
from br_gui         import *

from datetime       import date

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

	def affinas_callback(self, value):
		self.setProp(BG_Affinis(value))
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

	def __Header1(self):
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
	#def __Header1(self):

	def __resize_callback(self):
		self.decart.resize(window.innerWidth-200, window.innerHeight - 80)
		self.decart.redraw()

	def __loadData_callback(self, s):
		try:
			self._loadData_callback0_done
		except AttributeError:
			self._loadData_callback0_done = True

			self.__loadData_callback0()
			self.decart.draw_callback(s)
			self.__loadData_callback1()
		else:
			self.decart.draw_callback(s)
	#def __loadData_callback(self, decart, s):

	def __loadData_callback0(self):
		header1 = BG_Div()
		header1.inline()
		self.header0 <= self.__Header1()

		self.decart = BRG_Decart(window.innerWidth-200, window.innerHeight - 80)

		self.document <= html.BR()
		self.document <= self.decart

		self._affinis_range = BG_Range(lambda value: self.decart.affinas_callback(value))
		self.document <= self._affinis_range

		if self._logScale.getState():
			self.decart.setProp(BG_LogY())

		self.decart.setProp(BG_Affinis(self._affinis_range.getState()))

		self.decart.setRooler(BG_Frame(),
		                      BG_Grid())
	#def __loadData_callback0(self):

	def __loadData_callback1(self):
		verticalRooler  = BG_VerticalRooler(self.decart)
		leftRightBorder = BG_LeftRightBorder(self.decart)

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

		self.decart.mouseover(mouseover)
		self.decart.mousedrag(mousedrag)

		self._logScale.setCallback(self.decart.logY_callback)
		self._bubbleLevel.setCallback(self.decart.bubbleLevel_callback)
	#def __loadData_callback1(self):

	def __init__(self):

		self.document = BG_Document()
		self.header0 = BG_Div()
		self.header0.inline()
		self.header0 <= self.__LoadData()

		self.document <= self.header0

		self._loadData_callback = lambda s: self.__loadData_callback(s)

		window.bind('resize', lambda event: self.__resize_callback())
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
