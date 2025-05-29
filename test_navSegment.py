from navSegment import *

n1 = NavPoint (1, 'a', 0, 12)
n2 = NavPoint (2, 'b', 2, 4)
n3 = NavPoint (3, 'c', 4, 10)
s1 = NavSegment ( n1, n2)
s2 = NavSegment ("222", n2, n3)

print (s1.__dict__)
print (s2.__dict__)