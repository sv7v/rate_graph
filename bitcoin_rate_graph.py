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
	class __LoadData(BG_Div):
		def __init__(self):
			super().__init__()
			self.inline()
			self <= 'Файл данных:'
			self <= BG_LocalTextFile(lambda s:
			                                self._callback(map(lambda i: i.split(' '),
			                                                   s)))

		def setCallback(self, callback):
			self._callback = callback

	class LogScale(BG_Div):
		def __init__(self):
			super().__init__()
			self.inline()
			self <= 'Логарифмический масштаб:'
			self._cb = BG_CheckBox()
			self._cb.set()
			self <= self._cb

		def setCallback(self, callback):
			self._cb.setCallback(callback)

		def getState(self):
			return self._cb.getState()

	class BubbleLevel(BG_Div):
		def __init__(self):
			super().__init__()
			self.inline()
			self <= 'Горизонтальный уровень:'
			self._cb = BG_CheckBox()
			self <= self._cb

		def setCallback(self, callback):
			self._cb.setCallback(callback)

		def getState(self):
			return self._cb.getState()

	class BRG_Date(BG_Div):
		def __init__(self):
			super().__init__()
			self.inline()

	class __Header(BG_Div):
		def __init__(self):
			super().__init__()
			self.inline()

			self._ls = BitcoinRateGraph.LogScale()
			self <= self._ls
			self <= '. '
			self._bl = BitcoinRateGraph.BubbleLevel()
			self <= self._bl
			self <= '. '
			self._d = BitcoinRateGraph.BRG_Date()
			self <= self._d
			self <= '. '
			self._d0 = BitcoinRateGraph.BRG_Date()
			self <= self._d0
			self <= '. '
			self._d1 = BitcoinRateGraph.BRG_Date()
			self <= self._d1

			self.show(False)

		def setCallback_LogScale(self, callback):
			self._ls.setCallback(callback)

		def setCallback_BubbleLavel(self, callback):
			self._bl.setCallback(callback)

		def getState_LogScale(self):
			return self._ls.getState()

		def getState_BubbleLevel(self):
			return self._bl.getState()

		def setDate(self, text):
			self._d.setText(text)

		def _setDate01(self, d, x):
			d.setText(str(date.fromtimestamp((x-1970)*
			                                 (365.25*24*60*60))))

		def setDate0(self, date): self._setDate01(self._d0, date)
		def setDate1(self, date): self._setDate01(self._d1, date)

	def __Range(self):
		def callback(value):
			self._decart.setProp(BG_Affinis(value))
			self._decart.redraw()

		self._affinis_range = BG_Range(callback)
		self._affinis_range.show(False)

		return self._affinis_range

	def __init__(self):
		loadData = self.__LoadData()
		doc <= loadData

		header = self.__Header()
		doc <= header
		doc <= html.BR()

		decart = BRG_Decart()

		def loadData_callback(s):
			decart.draw_callback(s)

			header.show()

			verticalRooler  = BG_VerticalRooler(decart)
			leftRightBorder = BG_LeftRightBorder(decart)

			def mouseover(dot_x, dot_y, x, y):
				header.setDate('Дата: %s, курс: %f.' % (str(date.fromtimestamp((x-1970)*
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
				header.setDate0(date0)
				header.setDate1(date1)

			decart.mouseover(mouseover)
			decart.mousedrag(mousedrag)
		#def loadData_callback(s):

		loadData.setCallback(loadData_callback)

		header.setCallback_LogScale(decart.logY_callback)
		header.setCallback_BubbleLavel(decart.bubbleLevel_callback)

		doc <= decart

		decart.fit()
		doc <= self.__Range()

		window.bind('resize', lambda event: decart.fit_callback())

		if header.getState_LogScale():
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
