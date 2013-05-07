import bootstrap
from apptools import model



class Person(model.Model):

	''' Describes a person. '''

	__adapter__ = "RedisAdapter"

	firstname = basestring
	lastname = basestring, {'required': True}
	age = int, {'choices': xrange(18, 100)}
	cool = bool, {'default': False}


print
key = model.Key('Person', 'blabs')
print "Getting key %s (should be None)..." % key
print Person.get(model.Key('Person', 'blabs'))

key = model.Key('Person', 'sam')
print


p = Person(key=key, firstname="Sam", lastname="Gammon", age=21, cool=True)
p.put()
print
print "Put key %s (with keyname)..." % key
print


david = Person(firstname="David", lastname="Rekow", age=24)
k = david.put()
print
print "Put key %s (without keyname)..." % david.key
print


print
print "Getting key (should return entity)..."
k = model.Key("Person", "sam").get()
print "Got entity from keyname: %s." % k
print

print
print "Getting key (should return entity)..."
d = david.key.get()
print "Got entity from ID: %s." % d
print

print "!!!!!! ALL TESTS DONE !!!!!!"
