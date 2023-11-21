class SearchableNode:
	def __init__(self, name, tree, parent=None):
		self.name = name
		self.tree = tree
		self.parent = parent
		self.level = 0
		self.children = []

		identity = []
		if parent is not None:
			self.level = parent.level + 1
			identity = [el for el in parent._identity]
		identity.append(name)
		self._identity = tuple(identity)

	def appendChild(self, name):
		newNode = self.tree.createNode(name, self)
		self.children.append(newNode)
		return newNode

	def traverse(self, level=0):
		"""downtraverse from node"""
		yield self
		for child in self.children:
			for node in child.traverse(level+1):
				yield node

	def __ancestors(self):
		yield self
		for parent in self.ancestors():
			yield parent

	def ancestors(self):
		"""get node grand*parents. Does not include self"""
		if self.parent:
			for parent in self.parent.__ancestors():
				yield parent

	def level(self):
		return self.level

	def identity(self, pathSeparator='.'):
		return pathSeparator.join(self._identity)

	def __repr__(self):
		return f'<{self.__class__.__name__} "{self.name}">'

class SearchableTree:
	def __init__(self, name="root", NodeClass=SearchableNode):
		self.root = NodeClass(name, self)
		self.fullQualifiedIndex = {(name,): self.root}
		self.index = {(name,): self.root}

	def getRoot(self):
		return self.root

	def createNode(self, name, parent):
		"""to be used by nodes"""
		node = self.root.__class__(name, self, parent)
		self.fullQualifiedIndex[node._identity] = node
		self.index[node.name] = node
		return node

	def __pathFind(self, path, pathSeparator='.'):
		identity = tuple(path.split(pathSeparator))
		return self.fullQualifiedIndex.get(identity)

	def __nameFind(self, name):
		return self.index.get(name)

	def find(self, path, pathSeparator='.'):
		"""find by node name, or full path"""
		ret = None
		if pathSeparator in path:
			ret = self.__pathFind(path, pathSeparator)
		else:
			ret = self.__nameFind(path)
		return ret

	def traverse(self):
		return self.root.traverse()

	def leafs(self):
		"""get end leafs"""
		for el in self.traverse():
			if not el.children:
				yield el

	def upsert(self, name, pathSeparator='.'):
		"""insert full path (and create necessary nodes) by specifying nodes separates by path separator"""
		splitted = name.split(".")
		base = self.root
		for element in splitted:
			if element == self.root.name:
				continue
			elementFullName = tuple(list(base._identity) + [element])
			match = self.fullQualifiedIndex.get(elementFullName)
			if match is None:
				base = base.appendChild(element)
			else:
				base = match

	def __repr__(self, indent=1, verticalIndent=0):
		repr = ""
		for node in self.traverse():
			connector = ''
			if node.level > 0:
				connector = ''
				connector += '│\n' * verticalIndent
				connector += '├'
				connector += '─' * indent * node.level
				connector += ' '
			repr += f"{connector}{node}\n"
		
		formatedRepr = ''
		foundLastBound = False
		for index, char in enumerate(repr[::-1]):
			if not foundLastBound and char == '├':
				foundLastBound = True
				formatedRepr += '└'
			else:
				formatedRepr += char
		repr = formatedRepr[::-1].strip()
		return repr.strip()
