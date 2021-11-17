import sys, time

CONSTRAINTS = list()
SYMSET = set()
N = 0
NEIGHBORS = list()
def setGlobals(pzl): # set Global symbols, Size of Puzzle, Neighbors, and Constraints
  global SYMSET
  global CONSTRAINTS
  global N
  global NEIGHBORS
  N = int(len(pzl)**.5)
  CONSTRAINTS = [ [set() for x in range(3)] for k in range(N) ]

  SYMSET = set(pzl.replace('.', ''))
  if N > len(SYMSET):
    for i in range(1,10):
      if str(i) not in SYMSET: SYMSET.add(str(i))
      if N == len(SYMSET): break
  if N > len(SYMSET):
    if '0' not in SYMSET: SYMSET.add('0')
  if N > len(SYMSET):
    for i in range(65,91):
      if chr(i) not in SYMSET: SYMSET.add(chr(i))
      if N == len(SYMSET): break

  subBlockHeight = int(N**.5)
  while(N % subBlockHeight != 0): N += -1
  subBlockWidth = N // subBlockHeight

  for i in range(N):
    for x in range(i * N, i * N + N): CONSTRAINTS[i][0].add(x)  # adds all rows
    for x in range(i, N*(N-1)+i+1, N): CONSTRAINTS[i][1].add(x) # adds all collumns
  numBox = 0
  for row in range(subBlockWidth): # adds all subblocks
    for col in range(subBlockHeight):
      for r in range(subBlockHeight):
        for c in range(subBlockWidth):
          CONSTRAINTS[numBox][2].add((subBlockWidth * col) + c + (r * N) + (row * subBlockHeight * N))
      numBox += 1

  NEIGHBORS = [ set() for x in range(len(pzl)) ]
  for p in range(len(pzl)):
    row = p // N
    col = p % N
    subBlock = ((p // N) // subBlockHeight) * subBlockHeight + ((p % N) // subBlockWidth)
    NEIGHBORS[p] = CONSTRAINTS[row][0] | CONSTRAINTS[col][1] | CONSTRAINTS[subBlock][2]
    NEIGHBORS[p].remove(p)

def checkSum(pzl): # returns sum of every character in puzzle, is 405 for 9x9
  return sum(ord(c) for c in pzl) - (48 * N**2)

def isInvalid(pzl): # returns True if current puzzle is invalid. If a character has neighbor with same symbol it is invalid puzzle.
  for p in range(len(pzl)):
    for x in NEIGHBORS[p]:
      if pzl[p] != '.' and pzl[x] != '.':
        if pzl[p] == pzl[x]: return True
  return False

def charsInNBR(pzl,i):
  chars = set()
  for p in NEIGHBORS[i]: chars.add(pzl[p])
  return chars

def findMinPos(pzl, nbrVals): # finds the position with the minimum amount of symbols that can go into it, how many symbols can go into it
	max = 0
	ind = 0
	for i, c in enumerate(pzl):
		if c == '.':
			num = len(nbrVals[i])
			if num > max:
				max = num
				ind = i
				if max == N:
					return None
			if num == N-1:
				return [ind, N-max]
	return [ind, N - max]

def findNbrVals(pzl): # returns a list with index as position and the value is a set of all the taken symbols
	nbrVals = [set() for i in range(len(pzl))]
	for p in range(len(pzl)):
		if pzl[p] != '.': continue
		for nbr in NEIGHBORS[p]:
			if pzl[nbr] != '.': nbrVals[p].add(pzl[nbr])
	return nbrVals

def findMinSym(pzl, nbrVals): # returns the symbol that can go in least amount of positions, list of positions it can go in
	minTracker = ('!', [n for n in range(N+1)])
	for conL in CONSTRAINTS:
		for conSet in conL:
			for sym in SYMSET - {pzl[x] for x in conSet if pzl[x] != '.'}:
				tempSet = list()
				for i in conSet:
					if pzl[i] == '.' and sym not in nbrVals[i] :
						tempSet.append(i)
				if len(tempSet) <  len(minTracker[1]) and len(tempSet) >= 1:
					minTracker = (sym,tempSet)
	return minTracker

def bruteForce(pzl, nbrVals): # BruteForce algorithm to solve Sudoku Puzzle
	if pzl.find('.') == -1: return pzl  # solution
	minPosData = findMinPos(pzl, nbrVals)
	if minPosData is None: return ''
	minPos = minPosData[0]
	minPosSyms = SYMSET - nbrVals[minPos]
	if minPosData[1] <= 1:
		poss = [minPos]
		syms = minPosSyms
	else:
		minSymData = findMinSym(pzl, nbrVals)
		minSym = minSymData[0]
		if len(minSymData[1]) < len(minPosSyms):
			poss = minSymData[1]
			syms = [minSym]
		else:
			poss = [minPos]
			syms = minPosSyms
	for pos in poss:
		for sym in syms:
			newNbrVals = [s.copy() for s in nbrVals]
			newPzl = list(pzl)
			newPzl[pos] = sym
			newPzl = ''.join(newPzl)
			newNbrVals[pos].add(sym)
			for p in NEIGHBORS[pos]:
				newNbrVals[p].add(sym)
			bF = bruteForce(newPzl,newNbrVals)
			if bF: return bF
	return ""

puzzles = open(sys.argv[1] if len(sys.argv) > 1 else "puzzles.txt","r").read().splitlines()
totalStart = time.time()
for i, pzl in enumerate(puzzles):
  print('{0:03}'.format(i+1) + ": " + pzl)
  start = time.time()
  setGlobals(pzl)
  sol = bruteForce(pzl, findNbrVals(pzl))
  end = time.time()
  print("     " + sol + " " + str(end-start) + "s " + str(checkSum(sol)))
  if i == 52: print("Time for first 51 puzzles = " + str(time.time()-totalStart))
totalEnd = time.time()
print("Total time = " + str(totalEnd - totalStart) + 's')
