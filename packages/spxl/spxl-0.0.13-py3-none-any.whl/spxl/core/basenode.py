#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import Any, List, Dict, Set
from typing import cast, overload
from .builtins import Builtins
from .baseclass import BaseClass as Object


#--------------------------------------------------------------------------------
# 노드 클래스.
#--------------------------------------------------------------------------------
TNode = TypeVar("TNode", bound = "BaseNode")
class BaseNode(Object, Generic[TNode]):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__parent : TNode
	__children : list[TNode]
	__isAlive : bool
	__name : str


	#--------------------------------------------------------------------------------
	# 부모 프로퍼티 반환.
	#--------------------------------------------------------------------------------
	@property
	def Parent(self) -> TNode:
		return self.__parent


	#--------------------------------------------------------------------------------
	# 부모 프로퍼티 설정.
	#--------------------------------------------------------------------------------
	@Parent.setter
	def Parent(self, parent : TNode) -> None:
		if self.__parent is parent:
			return		
		if self.__parent:
			self.__parent.RemoveChild(self)
		self.__parent = parent
		if self.__parent:
			self.__parent.AddChild(self)


	#--------------------------------------------------------------------------------
	# 자식 프로퍼티 반환. (신규 리스트 생성 후 얕은 복사로 반환되므로 수정 불가)
	#--------------------------------------------------------------------------------
	@property
	def Children(self) -> list[TNode]:
		return list(self.__children)


	#--------------------------------------------------------------------------------
	# 이름 프로퍼티 반환.
	#--------------------------------------------------------------------------------
	@property
	def Name(self) -> str:
		return self.__name


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, name : str, **keywordArguments) -> None:
		base = super()
		base.__init__()
		self.__children = list()
		self.__isAlive = True
		self.__name = name
		base.__dict__.update(**keywordArguments)


	#--------------------------------------------------------------------------------
	# 파괴됨.
	#--------------------------------------------------------------------------------
	def __del__(self) -> None:
		base = super()
		base.__del__()
		

	#--------------------------------------------------------------------------------
	# 자식 추가.
	#--------------------------------------------------------------------------------
	def AddChild(self, child : TNode) -> None:
		if child in self.__children:
			return
		
		self.__children.append(child)
		child.__parent = self


	#--------------------------------------------------------------------------------
	# 자식 제거.
	#--------------------------------------------------------------------------------
	def RemoveChild(self, child : TNode) -> None:
		if child not in self.__children:
			return
		self.__children.remove(child)
		child.__parent = None


	#--------------------------------------------------------------------------------
	# 형제 노드 순서 설정.
	#--------------------------------------------------------------------------------
	def SetSiblingByIndex(self, index : int, newSibling : TNode) -> None:
		siblings = self.GetSiblings()
		if index < 0 or index >= len(siblings):
			raise IndexError("Sibling index out of range.")
		self.__parent.__children[self.__parent.__children.index(siblings[index])] = newSibling
		newSibling.Parent = self.__parent


	#--------------------------------------------------------------------------------
	# 형제 목록 반환.
	#--------------------------------------------------------------------------------
	def GetSiblings(self) -> list[TNode]:
		if self.__parent is None:
			return list()
		return [child for child in self.__parent.Children if child != self]


	#--------------------------------------------------------------------------------
	# 순서에 대한 형제 노드 반환
	#--------------------------------------------------------------------------------
	def GetSiblingByIndex(self, index : int) -> TNode:
		siblings = self.GetSiblings()
		if index < 0 or index >= len(siblings):
			raise IndexError("Sibling index out of range.")
		return siblings[index]


	#--------------------------------------------------------------------------------
	# 조상 노드 찾기.
	# - path는 노드이름들로 엮인 경로이다.
	#--------------------------------------------------------------------------------
	def FindAncestor(self, path : str) -> TNode:
		parts = path.split("/")
		current : TNode = self
		for part in reversed(parts):
			if part == ".":
				continue
			if current is None or current.Name != part:
				return None
			current = current.Parent
		return current


	#--------------------------------------------------------------------------------
	# 형제 노드 찾기.
	#--------------------------------------------------------------------------------
	def FindSibling(self, name : str) -> TNode:
		for sibling in self.GetSiblings():
			if sibling.Name == name:
				return sibling
		return None


	#--------------------------------------------------------------------------------
	# 자손 노드 찾기.
	#--------------------------------------------------------------------------------
	def FindDescendant(self, path : str) -> TNode:
		parts : list[str] = path.split("/")
		current : TNode = self
		for part in parts:
			if part == ".":
				continue
			found = False
			for child in current.Children:
				if child.Name == part:
					current = child
					found = True
					break
			if not found:
				return None
		return current


	#--------------------------------------------------------------------------------
	# 복제.
	#--------------------------------------------------------------------------------
	def Clone(self) -> TNode:
		clonedNode : TNode = TNode(self.Name, self.__dict__)
		return clonedNode


	#--------------------------------------------------------------------------------
	# 파괴.
	#--------------------------------------------------------------------------------
	def Destroy(self) -> None:
		if self.__isAlive:
			return
		self.__isAlive = False
		for child in list(self.__children):
			child.Destroy()
		if self.__parent:
			self.__parent.RemoveChild(self)
			self.__parent = None
		self.__children.clear()


	#--------------------------------------------------------------------------------
	# 반복문 순회.
	#--------------------------------------------------------------------------------
	def __iter__(self) -> Iterator:
		yield self
		for child in self.__children:
			yield from iter(child)


	#--------------------------------------------------------------------------------
	# 대상 노드의 구조를 자신에게로 덮어쓰기.
	#--------------------------------------------------------------------------------
	def CopyStructure(self, sourceNode : TNode) -> None:
		self.Name = sourceNode.Name
		# self.__dict__.update(sourceNode.__dict__)
		for child in sourceNode.Children:
			newChild : TNode = TNode(child.Name, child.__dict__)
			newChild.CopyStructure(child)
			self.AddChild(newChild)


	#--------------------------------------------------------------------------------
	# 문자열 변환.
	#--------------------------------------------------------------------------------
	def __repr__(self) -> str:
		base = super()
		return base.__repr__()