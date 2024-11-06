#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import Any, List, Dict, Set
from typing import cast, overload
import os
from ..core import Builtins
from ..core import BaseNode


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMPTY : str = ""



#--------------------------------------------------------------------------------
# 파일 시스템의 단위 항목.
#--------------------------------------------------------------------------------
TEntry = TypeVar("TEntry", bound = "Entry")
class Entry(BaseNode[TEntry]):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__path : str


	#--------------------------------------------------------------------------------
	# 전체 이름.
	#--------------------------------------------------------------------------------
	@property
	def FullName(self) -> str:
		return f"{self.__path}{self.Name}{self.__extension}"
	

	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, name : str, **keywordArguments) -> None:
		base = super()
		base.__init__(name, **keywordArguments)

		self.__path = keywordArguments.get("path")
		self.__extension = keywordArguments.get("extension")
		self.__fileFullName = f"{self.__path}{self.Name}{self.__extension}"


	#--------------------------------------------------------------------------------
	# 실제 존재 여부.
	#--------------------------------------------------------------------------------
	def Exists(self) -> bool:
		isExists : bool = os.path.exists(self.__path)
		return isExists