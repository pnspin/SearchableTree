# SearchableTree


Simple list intended for simplifying traversal & node search

**Does not support deletion**

Example:
```python 
tree = SearchableTree("root", SearchableNode)
root = tree.root()
l1 = root.appendChild('l1')
l11 = root.appendChild('l11')
l12 = root.appendChild('l12')
l2 = root.appendChild('l2')
l21 = root.appendChild('l21')
l22 = root.appendChild('l22')
root.upsert("l1.l11.l111")
root.upsert("l1.l11.l112")

for el in root.traverse(): #Traverse all nodes
	print(el)

print(tree) #Pretty print tree
print(tree.find("l112")) #Get node by name
print(tree.find("root.l1.l11")) #Get node by path
for el in l2.ancestors(): #Get node ancestors
	print(el)
```

Extend *SearchableNode* to add custom funcionality

### Author
- [Spin](pnspin@gmail.com)
