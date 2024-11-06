#------------------------------------------------------------------------
# 참조 목록.
#------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
from .stringutility import StringUtility, TIMESTAMP_DEFUALT, TIMESTAMP_SIMPLE


#------------------------------------------------------------------------
# 전역 상수 목록.
#------------------------------------------------------------------------
EMPTY : str = ""
SPACE : str = " "
WRITETEXT : str = "wt"
APPENDTEXT : str = "at"
UTF8 : str = "utf-8"
TAB : str = "\t"
LINEFEED : str = "\n"


#------------------------------------------------------------------------
# 기록 처리기.
#------------------------------------------------------------------------
class Logger:
	#------------------------------------------------------------------------
	# 멤버 변수 목록.
	#------------------------------------------------------------------------
	__texts : list[str]


	#------------------------------------------------------------------------
	# 생성됨.
	#------------------------------------------------------------------------
	def __init__(self) -> None:
		self.__texts : list[str] = list()
		self.Clear()


	#------------------------------------------------------------------------
	# 비우기.
	#------------------------------------------------------------------------
	def Clear(self) -> None:
		self.__texts.clear()


	#------------------------------------------------------------------------
	# 추가.
	#------------------------------------------------------------------------
	def Enqueue(self, text : str, sections : list[str] = None, indent : int = 0) -> None:
		if not sections:
			sections = list()
		timestamp : str = StringUtility.GetTimestamp(TIMESTAMP_DEFUALT)
		sections.insert(0, timestamp)

		prefixString : str = "\t" * indent
		sectionString : str = EMPTY.join([f"{prefixString}[{section}]" for section in sections])
		result = f"{sectionString}{SPACE}{text}"
		self.__texts.append(result)
		builtins.print(result)


	#------------------------------------------------------------------------
	# 저장.
	#------------------------------------------------------------------------
	def SaveToFile(self, filepath : str) -> None:
		with open(filepath, APPENDTEXT, encoding = UTF8) as file:
			text = LINEFEED.join(self.__texts)
			file.write(text)
			file.write(LINEFEED)
			file.write(LINEFEED)
			self.Clear()