import time

start_time = time.time()

def PatternToNumber(pattern):
	num = 0
	d = {'a' : 0, 't': 3, 'g': 2, 'c': 1}
	pattern = pattern.lower()
	p = len(pattern) - 1
	for i in range(0,len(pattern)):
		num += d[pattern[i]]*(4**p)
		p -= 1
	return num

def SymbolToNumber(symbol):
	symbol = symbol.lower()
	d = {'a' : 0, 't': 3, 'g': 2, 'c': 1}
	return d[symbol]

def NumberToSymbol(number):
	d = {0: 'a', 1: 'c', 2: 'g', 3: 't'}
	return d[number].upper();

def NumberToPattern(number, k):
	pattern = ""
	d = {0: 'a', 1: 'c', 2: 'g', 3: 't'}
	for i in range(0, k):
		div = number//4
		temp = number%4
		pattern = pattern + d[temp]
		number = div
	return pattern[:: - 1].upper()

def ComputingFrequencies(text, k):
	FrequencyArray = []
	for i in range(0, 4**k):
		FrequencyArray.append(0)
	for i in range(0, len(text) - k + 1):
		pattern = text[i:i+k]
		j = PatternToNumber(pattern)
		FrequencyArray[j] += 1

	return FrequencyArray

def FasterFrequentTerms(text, k):
	FrequentPatterns = []
	FrequencyArray = ComputingFrequencies(text, k)
	maxCount = max(FrequencyArray)
	for i in range(0, len(FrequencyArray)):
		if FrequencyArray[i] == maxCount:
			pattern = NumberToPattern(i, k)
			FrequentPatterns.append(pattern)

	return FrequentPatterns

def RecursivePatternToNumber(pattern):

	if pattern == "":
		return 0
	symbol = pattern[-1]
	prefix = pattern[0: len(pattern) - 1]
	return 4*RecursivePatternToNumber(prefix) + SymbolToNumber(symbol)

def RecursiveNumberToPattern(number, k):
	if k == 1:
		return NumberToSymbol(number)
	remainder = number%4
	quotient = number//4
	symbol = NumberToSymbol(remainder)
	prefix = RecursiveNumberToPattern(quotient, k - 1)
	return prefix + symbol

def FrequentWordsBySorting(text, k):
	index = []
	count = []
	FrequentPatterns = []
	for i in range(0, len(text) - k + 1):
		pattern = text[i:i+k]
		index.append(RecursivePatternToNumber(pattern))
		count.append(1)
	#print index
	#print count
	index.sort()
	for i in range(1, len(text) - k + 1):
		if index[i] == index[i-1]:
			count[i] = count[i - 1] + 1
	maxCount = max(count)
	for i in range(0, len(text) - k + 1):
		if count[i] == maxCount:
			pattern = RecursiveNumberToPattern(index[i], k)
			FrequentPatterns.append(pattern)
	return FrequentPatterns

def ClumpFinding(Genome, k, L, t):
	FrequentPatterns = []
	clump = []
	for i in range(0, 4**k):
		clump.append(0)
	for i in range(0, len(Genome) - L + 1):
		text = Genome[i:i+L]
		FrequencyArray = ComputingFrequencies(text, k)
		for j in range(0, 4**k):
			if FrequencyArray[j] >= t:
				clump[j] = 1
	for i in range(0, 4**k):
		if clump[i] == 1:
			pattern = RecursiveNumberToPattern(i, k)
			FrequentPatterns.append(pattern)
	return FrequentPatterns

def BetterClumpFinding(Genome, k, L, t):
	FrequentPatterns = []
	clump = []
	for i in range(0, 4**k):
		clump.append(0)
	text = Genome[0:L]
	FrequencyArray = ComputingFrequencies(text, k)
	for i in range(0,4**k):
		if FrequencyArray[i] >= t:
			clump[i] = 1
	for i in range(1, len(Genome) - L + 1):
		FirstPattern = Genome[i-1: i - 1 + k]
		index = RecursivePatternToNumber(FirstPattern)
		FrequencyArray[index] -= 1
		LastPattern = Genome[i+L-k: i + L]
		index = RecursivePatternToNumber(LastPattern)
		FrequencyArray[index] +=1
		if FrequencyArray[index] >= t:
			clump[index] = 1
	for i in range(0, 4**k):
		if clump[i] == 1:
			pattern = RecursiveNumberToPattern(i, k)
			FrequentPatterns.append(pattern)
	return FrequentPatterns