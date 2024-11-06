#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Union, Tuple
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins


#--------------------------------------------------------------------------------
# 상태코드 에러.
#--------------------------------------------------------------------------------
class HTTPStatusError(Exception):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__text : str
	__statusCode : int


	#--------------------------------------------------------------------------------
	# 오류메시지.
	#--------------------------------------------------------------------------------
	@property
	def Text(self) -> int:
		return self.__text
	

	#--------------------------------------------------------------------------------
	# 상태코드.
	#--------------------------------------------------------------------------------
	@property
	def StatusCode(self) -> int:
		return self.__statusCode
	

	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, statusCode : int, text : str = ""):
			self.__statusCode = statusCode
			self.__text = text
			base = super()
			if self.__text:
				base.__init__(f"HTTPStatusError: {self.__text} ({self.__statusCode})")
			else:
				base.__init__(f"HTTPStatusError: Status Code Exception. ({self.__statusCode})")