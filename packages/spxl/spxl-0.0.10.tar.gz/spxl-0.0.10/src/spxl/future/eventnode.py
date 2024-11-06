#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Union, Tuple
from typing import Any, List, Dict, Set
from typing import cast, overload
from enum import Enum
from ..core import BaseNode


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
EMPTY : str = ""


#--------------------------------------------------------------------------------
# 타입 별칭 정의 목록.
#--------------------------------------------------------------------------------
NodeEventFunction = Callable[..., Any] # function은 3.10에 존재하지 않음.


#--------------------------------------------------------------------------------
# 노드 이벤트 타입.
#--------------------------------------------------------------------------------
class NodeEventType(Enum):
	CREATEEVENT = "__OnCreateEvent" # callable[[None], None]
	DESTROYEVENT = "__OnDestroyEvent" # callable[[None], None]
	PARENTCHANGEEVENT = "__OnParentChangeEvent" # callable[[Node, Node], None]
	SIBLINGCHANGEEVENT = "__OnSiblingChangeEvent" # callable[[Node], None]
	CHILDCHANGEEVENT = "__OnChildChangeEvent" # callable[[Node], None]


#--------------------------------------------------------------------------------
# 노드 클래스.
#--------------------------------------------------------------------------------
class EventNode(BaseNode):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__events : dict[NodeEventType, set[NodeEventFunction]]
	__value : Any


	#--------------------------------------------------------------------------------
	# 값 프로퍼티 반환.
	#--------------------------------------------------------------------------------
	@property
	def Value(self) -> Any:
		return self.__value


	#--------------------------------------------------------------------------------
	# 값 프로퍼티 설정.
	#--------------------------------------------------------------------------------
	@property.setter
	def Value(self, value : Any) -> None:
		self.__value = value



	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, name : str, value : Any = None) -> None:
		base = super()
		base.__init__(name)
		
		self.__value = value

		# 이벤트 목록 초기화.
		for nodeEventType in NodeEventType:
			self.__events[nodeEventType] = set()
		self.__events[NodeEventType.CREATEEVENT].add(self.__OnCreateEvent)
		self.__events[NodeEventType.DESTROYEVENT].add(self.__OnDestroyEvent)
		self.__events[NodeEventType.PARENTCHANGEEVENT].add(self.__OnParentChangeEvent)
		self.__events[NodeEventType.SIBLINGCHANGEEVENT].add(self.__OnSiblingChangeEvent)
		self.__events[NodeEventType.CHILDCHANGEEVENT].add(self.__OnChildChangeEvent)

		# 생성 이벤트.
		self.NotifyEvent(NodeEventType.CREATEEVENT)


	#--------------------------------------------------------------------------------
	# 자식 추가.
	#--------------------------------------------------------------------------------
	def AddChild(self, child : BaseNode) -> None:
		base = super()
		base.AddChild(child)

		# 자식 변경 이벤트.
		self.NotifyEvent(NodeEventType.CHILDCHANGEEVENT, child)


	#--------------------------------------------------------------------------------
	# 자식 제거.
	#--------------------------------------------------------------------------------
	def RemoveChild(self, child : BaseNode) -> None:
		base = super()
		base.RemoveChild(child)

		# 자식 변경 이벤트.
		self.NotifyEvent(NodeEventType.CHILDCHANGEEVENT, child)


	#--------------------------------------------------------------------------------
	# 형제 노드 순서 설정.
	#--------------------------------------------------------------------------------
	def SetSiblingByIndex(self, index : int, newSibling : BaseNode) -> None:
		siblings = self.GetSiblings()
		if index < 0 or index >= len(siblings):
			raise IndexError("Sibling index out of range.")
		self.__parent.__children[self.__parent.__children.index(siblings[index])] = newSibling
		newSibling.Parent = self.__parent

		# 형제 변경 이벤트.
		self.NotifyEvent(NodeEventType.SIBLINGCHANGEEVENT, newSibling)



	#--------------------------------------------------------------------------------
	# 형제 노드 찾기.
	#--------------------------------------------------------------------------------
	def FindSibling(self, name : str) -> BaseNode:
		for sibling in self.GetSiblings():
			if sibling.Name == name:
				return sibling
		return None


	#--------------------------------------------------------------------------------
	# 파괴.
	#--------------------------------------------------------------------------------
	def Destroy(self, ) -> None:
		if self.__isAlive:
			return
		self.__isAlive = False

		self.NotifyEvent(NodeEventType.DESTROYEVENT)
		for child in list(self.__children):
			child.Destroy()
		if self.__parent:
			self.__parent.RemoveChild(self)
			self.__parent = None
		self.__children.clear()


	#--------------------------------------------------------------------------------
	# 노드가 생성됨.
	#--------------------------------------------------------------------------------
	def __OnCreateEvent(self) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 노드가 파괴됨.
	#--------------------------------------------------------------------------------
	def __OnDestroyEvent(self) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 부모 노드가 변경됨.
	#--------------------------------------------------------------------------------
	def __OnParentChangeEvent(self, previouslyParentNode : BaseNode, nextParentNode : BaseNode) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 형제 노드가 변경됨.
	#--------------------------------------------------------------------------------
	def __OnSiblingChangeEvent(self, siblingNode : BaseNode) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 자식 노드가 변경됨.
	#--------------------------------------------------------------------------------
	def __OnChildChangeEvent(self, childNode : BaseNode) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 이벤트 통지.
	#--------------------------------------------------------------------------------
	def NotifyEvent(self, nodeEventType : str, *args, **kwargs) -> None:
		for callback in self.__events[nodeEventType]:
			if not callback:
				continue
			callback(*args, **kwargs)


	#--------------------------------------------------------------------------------
	# 전체 이벤트 초기화.
	# - 전체를 초기화하지만 함수 목록 객체 자체를 삭제하진 않는다.
	#--------------------------------------------------------------------------------
	def ClearAllEvents(self) -> None:
		for nodeEventType, callbacks in self.__events.items():
			callbacks.clear()


	#--------------------------------------------------------------------------------
	# 이벤트 초기화.
	#--------------------------------------------------------------------------------
	def ClearEvent(self, nodeEventType : NodeEventType) -> None:
		callbacks = self.__events[nodeEventType]
		callbacks.clear()


	#--------------------------------------------------------------------------------
	# 이벤트 재설정.
	#--------------------------------------------------------------------------------
	def SetEvent(self, nodeEventType : NodeEventType, nodeEvent : NodeEventFunction) -> None:
		events = self.__events[nodeEventType]
		events.clear()
		events.update(nodeEvent)


	#--------------------------------------------------------------------------------
	# 이벤트 추가.
	#--------------------------------------------------------------------------------
	def AddEvent(self, nodeEventType : NodeEventType, nodeEvent : NodeEventFunction) -> None:
		events = self.__events[nodeEventType]
		if nodeEvent not in events:
			events.update(nodeEvent)


	#--------------------------------------------------------------------------------
	# 이벤트 제거.
	#--------------------------------------------------------------------------------
	def RemoveEvent(self, nodeEventType : NodeEventType, nodeEvent : NodeEventFunction) -> None:
		events = self.__events[nodeEventType]
		events.discard(nodeEvent)