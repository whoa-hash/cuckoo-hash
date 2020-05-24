import pytest

from BitHasher import *

class KeyDatapairObject(object):
    def __init__(self, k, d):
        self.key  = k
        self.data = d    

        
class HashTab(object):
    def __init__(self, size):
        #create a table
        self.__hashArray = [None] * size
        self.__numKeys = 0
    
    # return current number of keys in table    
    def __len__(self): return self.__numKeys

 
    # insert key/data if the key isn't already in the table
    # return False if the key is already in the table, True otherwise
    def insert(self, k, d, loop=0, reset=0): 
        # two hashes in order to identify the bucket where the key might be
        hash1=BitHash(k)
        hash2=BitHash(k,hash1)
        
        #two bits selected
        bit1 = hash1 % len(self.__hashArray)
        bit2 = hash2 % len(self.__hashArray) 

        # if the key is already there, return false
        l = self.find(k) 
        if l:
            return False   
        
        #otherwise, assign the bit object
        l=KeyDatapairObject(k, d)        

        #the key is not already there so add key/data pair
        #if either of the two bits are empty, set the empty bit
        if not self.__hashArray[bit1]: 
            self.__hashArray[bit1]=l
            self.__numKeys += 1
            
        elif not self.__hashArray[bit2]:
            self.__hashArray[bit2]=l
            self.__numKeys += 1 
            
        #if both are occupied, 
        else:
           #call both occupied function          
            self.bothOccupied(l, loop, reset, bit1)
          
        # If the table is getting too full, grow the table
        if self.__numKeys >= .5 * len(self.__hashArray): self.__growHash()           
        return True  
    
    def bothOccupied(self, l, loop, reset, bit1):
        #if we haven't reached the looping threshold yet
        if loop<5:  
            
            #call the loop function
            self.loop(loop, reset, bit1, l)             
        
        #after looping fails, the threshold of resetting hash is 5
        elif loop>=5 and reset<4: 
            
            #call the reset function
            self.reset(l, loop, reset)
                        
        #if the rehashes are not working, expand the nest array and rehash everything
        elif loop>=5:
            
            self.__numKeys+=1 
            self.__growHash()        
    
    #loop function
    def loop(self, loop, reset, bit1, l):           
        #store the bit that's there
        l2=self.__hashArray[bit1]
        
        #put a new bit in it's place
        self.__hashArray[bit1]=l

        #insert the old bit into a new place
        self.insert(l2.key, l2.data, loop+1, reset)  
        
        return True
     
    #rests the hash function and reinserts the table values       
    def reset(self, l, loop, reset):
        #reset the hash value
        ResetBitHash() 
        
        self.__numKeys = 0
        
        #make sure to reinsert every/t in table so that u can find things later
        number = len(self.__hashArray)
        new = HashTab(number)
        
        #copy the old array
        oldArray = self.__hashArray
        
        #put in the new key data pair
        bitone = BitHash(l.key) % len(self.__hashArray)
        new.__hashArray[bitone] = l
        new.__numKeys+=1
        
        #go through the old array
        for l in oldArray:
    
            #if the spot is occupied
            if l:
        
                #insert each key/data pair into the new hash table
                new.insert(l.key, l.data, loop, reset+1) 
        
        #make the hash array and the length of the keys set to the new hash array and new key length        
        self.__hashArray = new.__hashArray
        self.__numKeys += new.__numKeys
        

    # Returns bucket where k should be, and where k was found 
    def find(self, k): 
        # hash in order to identify the bucket where the key might be
        hash1=BitHash(k)
        hash2=BitHash(k,hash1)
        bit1 = hash1 % len(self.__hashArray)
        bit2 = hash2 % len(self.__hashArray)
       
        # get the key, data pair
        l = self.__hashArray[bit1] 
        l2 = self.__hashArray[bit2]
        
        #if there's something in the first bit
        if l:
            #return the data associated with the key
            if l.key == k: return l.data
            
            #if there was something in the first nest, but not the right key or there's something in the second nest
            elif l2:
                if l2.key == k: return l2.data      
        
        # return None if the key can't be found     
        else: return None       
    
    # delete from the hash table the element whose key is k and return key/data pair
    def delete(self, k):
        # if the key is not there, return false
        l = self.find(k)  
        if not l: return False 
        
        #copy the data to return
        keep = l        
        
        # two hashes in order to identify the bucket where the key might be
        hash1=BitHash(k)
        bit1 = hash1 % len(self.__hashArray)
        
        #then check the first hash if the nest has some/t in it
        l = self.__hashArray[bit1]
        if l.key == k: 
            #delete the keydata Pair
            l.key = None
            l.data = None
              
        else: #it must be in the second hash nest:
            hash2=BitHash(k,hash1)
            #select the bit
            bit2 = hash2 % len(self.__hashArray)
            l = self.__hashArray[bit2]
            #delete the key data Pair
            l.key = None
            l.data = None
        
        self.__numKeys -= 1
        return k, keep
            
    def __growHash(self):
        loop = 0
        reset = 0
        number = len(self.__hashArray)
        
        #create a new hash array which is twice the size of the old one
        new = HashTab(number * 2)
        
        #copy the old array
        oldArray = self.__hashArray
        
        #go throught the spots in the old array
        for spot in oldArray:
            
            #if the spot is occupied
            if spot:
               
                #insert all of the old key/data pairs into a new hash array   
                new.insert(spot.key, spot.data) 
                
        #set the hash array to the new hash array           
        self.__hashArray = new.__hashArray
        
        
        
    def keys(self):
        for l in self.__hashArray:
            if l:
                print(l.key)

                               
# PYTESTS BELOW THIS LINE

        
#test if insert keeps the right number of keys   
def test_insertworks():
    # make a simple list of words, and also put those words into a HashTab
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you", 
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]
    sh = HashTab(10)
    for w in words:
        sh.insert(w, 1)
    assert len(sh) == len(words)

def test_wordsInsertedFound():
    # make a simple list of words, and also put those words into a HashTab
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you", 
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]
    shi = HashTab(10)
    for w in words:
        shi.insert(w, 1) 
  #make sure that all the words in the list are found in the hash table
    for w in words:
        assert shi.find(w) != None
        assert shi.find(w) == 1

#test if one insert works    
def test__insertone():   
    shir=HashTab(1)
    shir.insert('hi', 1)
    assert shir.find('hi')==1
    assert len(shir) == 1
    
def test_noneIn():
    h = HashTab(3)
    assert len(h)==0
    
#test if the growHash works, the hash table will have to grow after five elements are inserted
def test_growHash():
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you", 
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]
    shira = HashTab(10)
    for w in words:
        shira.insert(w, 1)  
    assert len(shira) == len(words)
    
def test_growHash2():
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you", 
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]
    shirao = HashTab(10)
    for w in words:
        shirao.insert(w, 1)  
    assert shirao.find(w) != None

#test if the delete works when the word is in the table and when it's not   
def test_delete():
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you", 
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]
    h = HashTab(10)
    for w in words:
        h.insert(w, 1) 
    #make sure before the delete is correct
    assert len(h) == 12    
    h.delete('foo')
    #make sure after the delete is correct
    assert len(h) == 11  
    h.delete('fo')
    assert len(h) == 10
    
def test_deleteAgain():
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you", 
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]
    again = HashTab(10)
    for w in words:
        again.insert(w, 1) 
    again.delete('foo')
    #make sure the deleted word cannot be found
    assert again.find('foo') == None  
    
    
def test_deleteNotThere():
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you", 
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]
    h = HashTab(10)
    for w in words:
        h.insert(w, 1) 
    #make sure before the delete is correct
    assert len(h) == 12
    h.delete('notHere')
    #make sure after the delete is correct
    assert len(h) == 12   

def test_deleteNotThere2():
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you", 
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]
    h = HashTab(10)
    for w in words:
        h.insert(w, 1) 
    h.delete('notHere')
    #make sure after the delete did not work that it wasn't mistakenly inserted
    assert h.find('notHere') == None
    
#test the find when the word is in the table     
def test_find():
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you",
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]
    shiraor = HashTab(10)
    for w in words:
        shiraor.insert(w, 1) 
    for w in words:
        assert shiraor.find(w)!=None    
      
#and when it's not    
def test_findNotThere():
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you", 
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]
    h = HashTab(10)
    for w in words:
        h.insert(w, 1) 
    assert h.find('notHere') == None   
    
def test_duplicate():
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you", 
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]
    shiraorl = HashTab(10)
    for w in words:
        shiraorl.insert(w, 1) 
    #make sure that inserting an already inserted key doesn't insert it again
    for w in words:
        assert shiraorl.insert(w, 1)==False    
        
def test_duplicate2():
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you", 
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]
    shiraorl = HashTab(10)
    for w in words:
        shiraorl.insert(w, 1) 
    #make sure that inserting an already inserted key doesn't increment the length of the hash array
    assert len(shiraorl)==len(words)
    
#test your reset function   
def test_reset():
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you", 
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]
    shiraorli = HashTab(10)
    for w in words:
        shiraorli.insert(w, 1) 
    #this is the bithash value before the reset
    a =BitHash('me')
    me=KeyDatapairObject('me', 1)
    shiraorli.reset(me, 2, 1)
    #test that the hashval was reset
    assert BitHash('me')!=a
        
def test_reset2():
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you", 
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]
    shiraorlia = HashTab(10)
    for w in words:
        shiraorlia.insert(w, 1) 
    #reset the bithash to a new one
    a =BitHash('me')
    #create a keydata pair
    me=KeyDatapairObject('me', 1)
    #use the reset function
    shiraorlia.reset(me, 2, 1)
    for w in words:
        #test that all the words are still there
        assert shiraorlia.find(w)!=None
        
#test that the length increased with a key/data pair that's used as the first insert in the reset function
def test_reset3():
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you", 
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]  
    shiraorlian = HashTab(10)
    for w in words:
        shiraorlian.insert(w, 1) 
    me=KeyDatapairObject('me', 1)
    shiraorlian.reset(me, 2, 1)
    
    #test that the len is one more than before
    assert len(shiraorlian)==len(words) + 1
       
        
def test_reset4():
    words = ["foo", "fo", "fool", "fools", "foolish", "fooled me", "fools you", 
             "fooling", "no fooling", "fooled", "fool fool", "april fools ha!"]
    s = HashTab(10)
    for w in words:
        s.insert(w, 1) 
    a =BitHash('me')
    me=KeyDatapairObject('me', 1)
    s.reset(me, 2, 1)
    #test that the new keydata pair was inserted
    assert s.find('me')==1         

#the loop tests will only pass if there was indeed something to be evicted
#so if it fails that proves that the eviction is working
#it just means that there was nothing to be evicted; it fails because it cannot evict a 'None'          
def test_loop():
    words = ["foo", "fo", "fool"]
    h = HashTab(10)
    for w in words:
        h.insert(w, 1)
    l=KeyDatapairObject('fools', 1)
    bit1 = BitHash('fools') % 10
    #make sure the loop function worked (that means that there was indeed something to be evicted)
    assert h.loop(1, 0, bit1, l) == True
    
def test_loop2():
    words = ["foo", "fo", "fool"]
    h = HashTab(10)
    for w in words:
        h.insert(w, 1)
    l=KeyDatapairObject('fools', 1)
    bit1 = BitHash('fools') % 10
    h.loop(1, 0, bit1, l) 
    #make sure the loop function increments the length of keys
    assert len(h) == 4
    
def test_loop3():
    words = ["foo", "fo", "fool"]
    h = HashTab(10)
    for w in words:
        h.insert(w, 1)
    l=KeyDatapairObject('fools', 1)
    bit1 = BitHash('fools') % 10
    h.loop(1, 0, bit1, l) 
    #make sure all the keys can be found after the eviction and replacement in the loop
    for w in words:
        assert h.find(w) != None
    
           
pytest.main(["-v", "-s", "cuckoo hash data structure.py"])     
    
    
    
    
    
 
   

