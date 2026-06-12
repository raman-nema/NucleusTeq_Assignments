""" Program to perform set operations."""

first_set = {10, 20, 30, 40, 50, 60}
second_set = {40, 50, 60, 70, 80, 90}

# Union means all unique elements from both sets
print("Union =", first_set.union(second_set)) 

# Intersection means common elements in both sets
print("Intersection =", first_set.intersection(second_set))

# Difference means elements in the first set but not in the second set
print("Difference =", first_set.difference(second_set))