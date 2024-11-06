#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Union, Tuple
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..core.builtins import Builtins


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------



#--------------------------------------------------------------------------------
# 싱글톤 익셉션.
#--------------------------------------------------------------------------------
class SingletonException(Exception):
	"""싱글톤 인스턴스를 외부에서 직접 생성하려고 할 때 발생하는 예외."""
	pass