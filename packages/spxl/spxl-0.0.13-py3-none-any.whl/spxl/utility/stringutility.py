#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import Any, List, Dict, Set
from typing import cast, overload
from datetime import datetime
from ..core import Builtins, Object


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
TIMESTAMP_DEFUALT : str = "%Y/%m/%d %H:%M:%S" # 20241031 15:13:05
TIMESTAMP_SIMPLE : str = "%y%m%d%H%M" # 2410311522

#--------------------------------------------------------------------------------
# 문자열 유틸리티.
#--------------------------------------------------------------------------------
class StringUtility(Object):
	#--------------------------------------------------------------------------------
	# 클래스 멤버 변수 목록
	#--------------------------------------------------------------------------------


	#------------------------------------------------------------------------
	# 현재 시간 획득.
	#------------------------------------------------------------------------
	@staticmethod
	def GetTimestamp(format : str = TIMESTAMP_DEFUALT, useMilliseconds : bool = False) -> str:
		time : datetime = datetime.now()
		timestamp : str = time.strftime(format)
		if useMilliseconds:
			milliseconds = time.microsecond // 1000
			milliseconds = str(milliseconds).zfill(3)
			f"{timestamp}.{milliseconds}"
		return timestamp