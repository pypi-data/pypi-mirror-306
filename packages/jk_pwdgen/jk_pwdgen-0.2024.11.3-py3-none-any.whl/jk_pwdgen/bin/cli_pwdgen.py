#!/usr/bin/python

import os
import typing
import sys

import jk_typing
import jk_systools
import jk_logging

import jk_pwdgen








class MainApp(jk_systools.AbstractMultiCmdCLIApp):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self):

		super().__init__(
			appFilePath = __file__,
			appVersion = jk_systools.__version__,
			appDescription = "Generate passwords.",
		)

		# ----

		self.argsParser.addDescriptionChapter(None, [
			"This tool assists in the generation of strong passwords. Generation is based on the Python random number generator random.Random. According to the Python "
			"documentation this RNG is based on Mersenne Twister and os.urandom(), so it should provide sufficient randomness for password generation."
			,
			"This tool checks that passwords generated are of sufficient qualty. Depending on options set if invoked it ensures that passwords will have the "
			"correct number of special characters as well as enough numeric characters."
			,
			"In order to use this password generation tool just run it. On each run it will generate one or more passwords (depending on arguments specified). "
			"All passwords are printed to STDOUT line by line."
		])

		# ----

		# self.argsParser.createReturnCode(1, "An error occurred.")
		self.argsParser.createAuthor("Jürgen Knauth", "pubsrc@binary-overflow.de")

		# ----

		self.argsParser.setLicense("Apache",
			YEAR_FROM = 2020,
			YEAR_TO = 2024,
			COPYRIGHTHOLDER = "Jürgen Knauth",
		)

		# ----

		self.argsParser.optionDataDefaults.set("n", 1)
		self.argsParser.optionDataDefaults.set("length", 24)
		self.argsParser.optionDataDefaults.set("minNumberOfNumericChars", 2)
		self.argsParser.optionDataDefaults.set("numberOfSpecialChars", 3)
		self.argsParser.optionDataDefaults.set("prohibitedChars", "0l")

		self.argsParser.createOption("n", None, "Number of passwords to generate. (Default: 1)").expectInt32("n", minValue=1).onOption = \
			lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("n", argOptionArguments[0])
		self.argsParser.createOption("l", "length", "Length of password to generate. (Default: 24)").expectInt32("n", minValue=3).onOption = \
			lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("length", argOptionArguments[0])
		self.argsParser.createOption(None, "minNumberOfNumericChars", "Minimum number of numeric characters. (Default: 2)").expectInt32("n", minValue=0).onOption = \
			lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("minNumberOfNumericChars", argOptionArguments[0])
		self.argsParser.createOption(None, "numberOfSpecialChars", "Minimum number of special characters. (Default: 3)").expectInt32("n", minValue=0).onOption = \
			lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("numberOfSpecialChars", argOptionArguments[0])
		self.argsParser.createOption(None, "prohibitedChars", "Prohibites characters. (Default: \"0l\")").expectString("s", minLength=0).onOption = \
			lambda argOption, argOptionArguments, parsedArgs: \
				parsedArgs.optionData.set("prohibitedChars", argOptionArguments[0])
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################
 
	def runImpl(self, ctx:jk_systools.CLIRunCtx) -> int:
		pwdGen = jk_pwdgen.PasswordGenerator(
			length = ctx.parsedArgs.optionData["length"],
			minNumberOfNumericChars = ctx.parsedArgs.optionData["minNumberOfNumericChars"],
			numberOfSpecialChars = ctx.parsedArgs.optionData["numberOfSpecialChars"],
			prohibitedChars = ctx.parsedArgs.optionData["prohibitedChars"],
		)

		print()
		for i in range(0, ctx.parsedArgs.optionData["n"]):
			print(pwdGen.generate())
		print()

		return jk_systools.IExitCodes.SUCCESS
	#

#








def main():
	appExitCode = jk_systools.IExitCodes.ERR_INTERNAL
	try:
		appExitCode = MainApp().run()
	except jk_logging.ExceptionInChildContextException as ee:
		#print(repr(ee.originalExeption))
		pass

	sys.exit(appExitCode)
#













