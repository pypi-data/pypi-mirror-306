#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
import os
from .filter import Filter


#--------------------------------------------------------------------------------
# 파일 필터 클래스.
# - 루트 디렉토리를 넣고 for문을 돌리면 조건에 부합하는 파일경로만 출력됨.
#--------------------------------------------------------------------------------
class FileFilter(Filter[str]):
	def __init__(self, rootPath : str, predicate : Callable[[str], bool] = None):
		base = super()
		base.__init__()

		# 제너레이터 표현식. (Iterable 호출시 사용되어 메모리 할당됨)
		self.Iterable = (os.path.join(root, file) for root, directories, files in os.walk(rootPath) for file in files)
		self.Predicate = predicate