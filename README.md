# cuckoo-hash
A cuckoo hash is a data structure that solves the problem of collisions of data in a certain way. In this cuckoo hash I used one hash table and two hash functions. A cuckoo hash 'kicks out' the information in one spot of the hash table and inserts a new piece of information in its place. The original piece of information that got 'kicked out' must then be re-inserted.
Sometimes, the cuckoo hash goes into an infinite loop by inserting and evicting the same two pieces of information (the key, data pair, in this case). Then, there 
are two solutions: either the hash table can be 'grown' and then everything should be re-inserted, or the hash function that's being used to find a spot in the hash array can be changed to a new hash function and likewise, then everything must be re-inserted.

I used Pytest for testing.
