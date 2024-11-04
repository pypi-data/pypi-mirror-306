


import random





#
# This class assist in generating strong passwords.
#
class PasswordGenerator(object):

	def __init__(self,
		length:int = 24,
		numberOfSpecialChars:int = 3,
		minNumberOfNumericChars:int = 2,
		letterChars:str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQSTUVWXYZ",
		numberChars:str = "1234567890",
		specialChars:str = "_-+=./~%#",
		prohibitedChars:str = "Ol"):

		self.__length = -1
		self.__letterChars = ""
		self.__numericChars = ""
		self.__specialChars = ""
		self.__prohibitedChars = ""
		self.__numberOfSpecialChars = -1
		self.__minNumberOfNumericChars = -1

		self.setLength(length)
		self.setMinNumberOfNumericChars(minNumberOfNumericChars)
		self.setNumberOfSpecialChars(numberOfSpecialChars)
		self.setNumericCharacters(numberChars)
		self.setLetterCharacters(letterChars)
		self.setSpecialCharacters(specialChars)
		self.setProhibitedChars(prohibitedChars)

		self.__rng = random.Random()
	#

	@property
	def reservoir(self) -> str:
		return self.__filter(self.__letterChars, self.__numericChars, self.__prohibitedChars) + self.__specialChars
	#

	@property
	def standardReservoir(self) -> str:
		return self.__filter(self.__letterChars + self.__numericChars, self.__prohibitedChars)
	#

	def setMinNumberOfNumericChars(self, minNumberOfNumericChars:int):
		assert isinstance(minNumberOfNumericChars, int)

		self.__minNumberOfNumericChars = minNumberOfNumericChars
	#

	def setNumberOfSpecialChars(self, numberOfSpecialChars:int):
		assert isinstance(numberOfSpecialChars, int)

		self.__numberOfSpecialChars = numberOfSpecialChars
	#

	def setLength(self, length:int):
		assert isinstance(length, int)
		assert length > 1

		self.__length = length
	#

	def setSpecialCharacters(self, specialChars:str):
		assert isinstance(specialChars, str)

		self.__specialChars = specialChars
	#

	def setLetterCharacters(self, letterChars:str):
		assert isinstance(letterChars, str)

		self.__letterChars = letterChars
	#

	def setNumericCharacters(self, numericChars:str):
		assert isinstance(numericChars, str)

		self.__numericChars = numericChars
	#

	def setProhibitedChars(self, prohibitedChars:str):
		assert isinstance(prohibitedChars, str)

		self.__prohibitedChars = prohibitedChars
	#

	def __filter(self, s:str, prohibited:str) -> str:
		return "".join([ x for x in s if x not in prohibited ])
	#

	#
	# Build a reservoir or characters
	#
	def __pickCharacters(self) -> str:
		pool = []
		for i in range(0, self.__numberOfSpecialChars):
			c = self.__rng.choice(self.__specialChars)
			pool.append(c)

		reservoir = self.standardReservoir
		for i in range(0, self.__length - self.__numberOfSpecialChars):
			c = self.__rng.choice(reservoir)
			pool.append(c)

		return "".join(pool)
	#

	#
	# Check if there are enough numeric characters and if no letter exists more often than three times.
	#
	def __validate(self, characters:str):
		counting = {}
		nNumeric = 0
		for c in characters:
			counting[c] = counting.get(c, 0) + 1
			if c in self.__numericChars:
				nNumeric += 1

		if nNumeric < self.__minNumberOfNumericChars:
			return False

		for n in counting.values():
			if n > 3:
				return False

		return True
	#

	def generate(self) -> str:
		if (self.__numberOfSpecialChars > 0) and (len(self.__specialChars) == 0):
			raise Exception("No special characters available to choose from!")
		if (self.__minNumberOfNumericChars > 0) and (len(self.__numericChars) == 0):
			raise Exception("No numeric characters available to choose from!")

		nLoop = 0
		while True:
			# pick characters randomly
			reservoir = self.__pickCharacters()

			# check that we don't have too many identical characters
			if not self.__validate(reservoir):
				if nLoop == 20:
					raise Exception("Can't find a password with current settings!")
				nLoop += 1
				continue

			# now build the password
			ret = []
			while reservoir:
				c = self.__rng.choice(reservoir)
				ret.append(c)
				pos = reservoir.find(c)
				reservoir = reservoir[:pos] + reservoir[pos+1:]

			# return the password
			return "".join(ret)
	#

	def __call__(self):
		return self.generate()
	#

#




