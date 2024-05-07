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

		self._header.show()
		self._affinis_range.show()

		def mousemove_callback(x, y):
			self._date.setText('Дата: %s, курс: %f.' % (str(date.fromtimestamp((x-1970)*
			                                                                   (365.25*24*60*60))),
			                                            y))
			self._verticalRooler.draw(x)

		self._decart.mousemove(mousemove_callback)

	def __LoadData(self):
		ret = BG_Div()
		ret.inline()
		ret <= 'Файл данных:'
		ret <= BG_LocalTextFile(lambda s:
		                               self.draw(map(lambda i:
		                                                    i.split(' '),
		                                             s)))
		return ret

	def __LogScaleCheckBox(self):
		def callback(checked):
			if checked: self._decart.setProp(BG_LogY())
			else:       self._decart.delProp(BG_LogY())
			self._decart.redraw()

		self.logY_checkbox = BG_CheckBox(callback)
		self.logY_checkbox.set()
		return self.logY_checkbox

	def __LogScale(self):
		ret = BG_Div()
		ret.inline()
		ret <= 'Логарифмический масштаб:'
		ret <= self.__LogScaleCheckBox()
		return ret

	def __BubbleLevelCheckBox(self):
		def callback(checked):
			if checked:
				self._decart.setRooler(BG_Frame(),
				                       BG_Grid(),
				                       BG_BubbleLevel(20))
			else:
				self._decart.setRooler(BG_Frame(),
				                       BG_Grid())
			self._decart.redraw()

		return BG_CheckBox(callback)

	def __BubbleLevel(self):
		ret = BG_Div()
		ret.inline()
		ret <= 'Горизонтальный уровень:'
		ret <= self.__BubbleLevelCheckBox()
		return ret

	def __Date(self):
		self._date = BG_Div()
		self._date.inline()

		return self._date

	def __Header(self):
		self._header = BG_Div()
		self._header.inline()

		self._header <= self.__LogScale()
		self._header <= '. '
		self._header <= self.__BubbleLevel()
		self._header <= '. '
		self._header <= self.__Date()

		self._header.show(False)

		return self._header

	def __Canvas(self):
		self.__canvas = BG_HtmlCanvas(1,1)
#		self.__canvas.fit()
		return self.__canvas

	def __Range(self):
		def callback(value):
			self._decart.setProp(BG_Affinis(value))
			self._decart.redraw()

		self._affinis_range = BG_Range(callback)
		self._affinis_range.show(False)

		return self._affinis_range

	def __init__(self):
		document <= self.__LoadData().get()
		document <= self.__Header().get()
		document <= html.BR()
		document <= self.__Canvas().get()
		self.__canvas.fit()
		document <= self.__Range().get()
		#--------------------------------------------------------------
		window.bind('resize', lambda event:self.fit())
		#--------------------------------------------------------------
		self._decart = BG_Decart(self.__canvas)

		if self.logY_checkbox.getState():
			self._decart.setProp(BG_LogY())

		self._decart.setProp(BG_Affinis(self._affinis_range.getState()))

		self._decart.setRooler(BG_Frame(),
		                       BG_Grid())

		self._verticalRooler = BG_VerticalRooler(self.__canvas)
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
