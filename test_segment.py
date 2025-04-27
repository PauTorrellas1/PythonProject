from segment import *
n1 = Node ('aaa', 0, 0)
n2 = Node ('bbb', 1, 2)
n3 = Node ('ccc', 3, 4)
s1 = Segment ("111", n1, n2)
s2 = Segment ("222", n2, n3)

print (s1.__dict__)
print (s2.__dict__)
