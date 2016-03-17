#!/usr/bin/python


#this is how you define functions
def generate_prime(x):
	return  x * x - x + 41

def main():
	print 'basic lists:'
	a = [1, 2 , 3 , 4, 5]
	print 'my list', a

	a = a + 4 * [6] + [1.1] + [3.14]
	print 'my updated list', a

	print 'last index', a[-1]

	print 'second last index', a[-2]

	# " and ' are interchangable
	print "Strins are basicaly lists with nice features"
	somestring = 'Lorem ipsum dolor sit amet, consectetur aDipisicing elIt, Sed do eiusmod'

	print 'Original string:', somestring
	print 'Remove comas:', somestring.replace(",", '')
	print 'Remove spaces:', somestring.replace(" ", '')
	print 'Replace spaces:', somestring.replace("ipsum", '***')
	print 'Some changes:', somestring.lower()
	print 'Some changes:', somestring.upper()
	print 'Split on words:', somestring.split()
	print 'Split on parts:', somestring.split(',')[0]
	print "Who needs wariables:",  'Lorem ipsum dolor sit amet,'.replace(',','').replace(' ', '  ').upper()

	print 'for loop'
	for i in range(8):
		print i, a[i] ** 2 #not really safe i can be > than max index of a

	print 'oneliner'
	for i in range(8): print i, a[i] ** 2


	print 'safer way'
	for v in a: print v ** 2


	print 'if you want indexces -- use enumerate'
	for i, v in enumerate(a): print i, v * v


	print 'List comprehension:'
	data = [2 * i + 1 for i in range(8)]
	print data

	print 'List comprehension with if-else'
	data = [d if d % 3 != 0 else 0 for d in data ]
	print data

	print 'List comprehension with only if'
	data = [d for d in data if d != 0]
	print data


	print 'Function is an object, you can assing function to a variable'
	some_variable = generate_prime # this function to variable assignment
	newdata = [some_variable(i) for i in range(10)]
	print 'primes', newdata


	print "Function if you don't want to define function, keeping your code cleaner"
	# lambda -- function without a name. 
	some_variable = lambda x : x * x - x + 41 
	newdata = [some_variable(i) for i in range(10)]
	print 'primes', newdata


	print 'For loops are ugly use map instead'
	# map(function that accepts n arguments, 1st arguemnt, ..., n-th argument)
	newdata = map(some_variable, range(10)) 
	print 'primes', newdata


	print 'Why do you have to care about the name of function that you use only once'
	newdata = map(lambda x : x * x - x + 41,  range(10))
	print 'primes', newdata


	print 'The last example with map'
	newdata = map(lambda x, y: x ** 2 + 100 * y, range(10), range(10, 20))
	print newdata

	# read this file and print it (quine)
	# print open('syntax.py').read()




# We want to run main function only if we invoke this file
# don't run main when importing this file
if __name__ == '__main__':
	main()
