#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
from threading import Lock
from ..core import Builtins, Object
from ..exception import SingletonException


#--------------------------------------------------------------------------------
# 싱글톤 클래스.
# - 이 클래스를 상속 받은 클래스는 외부에서 생성자를 호출해서 할당하려고 하면 예외가 발생한다.
# - 또한 GetInstance() 에서 멀티쓰레드 안정성 확보를 위해 약간의 지연이 있다.
# - DerivedClass(Singleton): pass
# - DerivedClass.GetInstance() # OK
# - newInstance = DerivedClass() # ERROR : SingletonException
#--------------------------------------------------------------------------------
TSingleton = TypeVar("TSingleton", bound = "Singleton")
class Singleton(Object, Generic[TSingleton]):
	#--------------------------------------------------------------------------------
	# 클래스 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__Instance : TSingleton = None
	__IsLocked : bool = True
	__ThreadLock: Lock = Lock()


	#--------------------------------------------------------------------------------
	# 인스턴스 할당.
	#--------------------------------------------------------------------------------
	def __new__(classType : Type[TSingleton]) -> TSingleton:
		# 인스턴스 명시적 생성시 예외 처리.
		if classType.__IsLocked:
			raise SingletonException("Cannot create instance directly. Use GetInstance() instead.")

		# 생성.
		classType.__Instance = super(Singleton, classType).__new__(classType)
		return classType.__Instance


	#--------------------------------------------------------------------------------
	# 인스턴스 파괴.
	#--------------------------------------------------------------------------------
	def __del__(self) -> None:
		# 인스턴스 삭제시 예외 처리.
		raise SingletonException("Cannot delete singleton instance.")


	#--------------------------------------------------------------------------------
	# 인스턴스 반환.
	# - 없으면 생성해서 반환.
	#--------------------------------------------------------------------------------
	@classmethod
	def GetInstance(classType : Type[TSingleton]) -> TSingleton:
		with classType.__ThreadLock:
			if not classType.__Instance:
				classType.__IsLocked = False
				classType.__Instance = classType()
				classType.__IsLocked = True
		return classType.__Instance