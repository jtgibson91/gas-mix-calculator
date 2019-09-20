from decimal import Decimal, InvalidOperation

SUPPORTED_COMPONENTS = ('H2', 'He', 'CH4', 'CO2', 'O2', 'N2', 'Ar')

H2_KG_PER_MOL = Decimal(0.002016)
HE_KG_PER_MOL = Decimal(0.0040026)
CH4_KG_PER_MOL = Decimal(0.016043)
CO2_KG_PER_MOL = Decimal(0.04401)
O2_KG_PER_MOL = Decimal(0.03200)
N2_KG_PER_MOL = Decimal(0.0280134)
AR_KG_PER_MOL = Decimal(0.039948)

COMPONENTS_MOLAR_MASS_DICT = {

	'H2': H2_KG_PER_MOL,
	'He': HE_KG_PER_MOL,
	'CH4': CH4_KG_PER_MOL,
	'CO2': CO2_KG_PER_MOL,
	'O2': O2_KG_PER_MOL,
	'N2': N2_KG_PER_MOL,
	'Ar': AR_KG_PER_MOL
}

SUPPORTED_CYL_SIZES = ('H', 'J', 'S')
S_CYL_SIZE_MOL = 80
H_CYL_SIZE_MOL = 250
J_CYL_SIZE_MOL = 350

CYL_SIZES_MOLES_DICT = {

	'H': H_CYL_SIZE_MOL,
	'J': J_CYL_SIZE_MOL,
	'S': S_CYL_SIZE_MOL
}

MIN_NUMBER_OF_COMPONENTS = 2
MAX_NUMBER_OF_COMPONENTS = 5

# Change this based on mix tolerance and/or scale sensitivity
DEFAULT_ROUNDING_VALUE = 4

def round_number(number, places_after_decimal=DEFAULT_ROUNDING_VALUE):
	"""
	Reduce places after decimal point for decimal.Decimal types
	:param number: The number to round
	:type number: decimal.Decimal
	:param places_after_decimal: The # of places after the decimal point to display number to. Defaults to 4
	:type places_after_decimal: int
	:return a decimal.Decimal object: Rounded to 'places_after_decimal' places after the decimal point
	"""

	if places_after_decimal == 4:
		return number.quantize(Decimal("0.0001"))

	elif places_after_decimal == 0:
		return number.quantize(Decimal("0"))

	elif places_after_decimal == 1:
		return number.quantize(Decimal("0.1"))

	elif places_after_decimal == 2:
		return number.quantize(Decimal("0.01"))

	elif places_after_decimal == 3:
		return number.quantize(Decimal("0.001"))

	elif places_after_decimal == 5:
		return number.quantize(Decimal("0.00001"))

	elif places_after_decimal == 6:
		return number.quantize(Decimal("0.000001"))

	elif places_after_decimal == 7:
		return number.quantize(Decimal("0.0000001"))

	elif places_after_decimal == 8:
		return number.quantize(Decimal("0.00000001"))

class GasMixture:

	def __init__(self, cylinder_size=None, number_of_components=0, components=None, components_masses=None):
		"""
		Create a new gas mixture

		:param cylinder_size: The size of cylinder used to make the mix. Value must be in SUPPORTED_CYL_SIZES
			e.g. 'H'
		:type cylinder_size: str
		:param number_of_components: The number of components that make up the mix
		:type number_of_components: int
		:param components: A dict with this format: keys: the gas component, values: the percent by volume
			that component accounts for in the mix
		:type components: dict {str: decimal.Decimal}
		:param components_masses: A dict with this format: keys: the gas component, values: the
			mass of that component
		:type components_masses: dict {str: decimal.Decimal}

		"""

		self.cylinder_size = cylinder_size
		self.number_of_components = number_of_components
		self.components = components
		self.components_masses = components_masses

	def __str__(self, feedback=''):
		return feedback

	def set_cylinder_size(self):
		"""
		Gets the cylinder size input from the user, validates the input, and sets self.cylinder_size

		:return: None
		"""

		print('Enter the cylinder size (H, J, S):')

		# Loop until user enters valid input
		while self.cylinder_size not in SUPPORTED_CYL_SIZES:

			self.cylinder_size = input()

			if self.cylinder_size not in SUPPORTED_CYL_SIZES:
				print('The cylinder size must be either H, J or S - try again:')

	def set_number_of_components(self):
		"""
		Gets the # of gas components that will make up the mix from the user, validates the input, and sets
			self.number_of_components

		:return: None
		"""

		print(f'Enter the # of components ({MIN_NUMBER_OF_COMPONENTS}-{MAX_NUMBER_OF_COMPONENTS}): ')

		while self.number_of_components not in range(MIN_NUMBER_OF_COMPONENTS, MAX_NUMBER_OF_COMPONENTS + 1):

			self.number_of_components = input()

			try:
				self.number_of_components = int(self.number_of_components)
			except ValueError:
				print(
					f'The # of components must be a number between {MIN_NUMBER_OF_COMPONENTS} and {MAX_NUMBER_OF_COMPONENTS} - try again:')
				continue

			if self.number_of_components not in range(MIN_NUMBER_OF_COMPONENTS, MAX_NUMBER_OF_COMPONENTS + 1):
				print(
					f'The # of components must be between {MIN_NUMBER_OF_COMPONENTS} and {MAX_NUMBER_OF_COMPONENTS} - try again:')

	def get_component_info(self):
		"""
		Gets the gas components and their corresponding proportions from the user. Sets self.components with that info

		:return: None
		"""

		num_of_components = self.number_of_components

		# Initialize them with None so we can access those indices before data is added
		components = [None for i in range(num_of_components)]
		components_percentages = [None for i in range(num_of_components)]

		# For each component, prompt the user for data on the command line and validate it
		for i in range(num_of_components):

			supported_components_str = ', '.join([i for i in SUPPORTED_COMPONENTS])

			print(
				f'Enter component #{i + 1} gas type (must be one of the following {supported_components_str}):')

			while components[i] not in SUPPORTED_COMPONENTS:

				components[i] = input()

				if components[i] not in SUPPORTED_COMPONENTS:
					print(f'The component must be one of these {SUPPORTED_COMPONENTS} - try again:')

			# If this is the final component, allow for Balance gas % calculation
			if not i == num_of_components - 1:
				print(f'Enter the percentage of {components[i]} in the mix (e.g. 3.5):')
			else:
				print(
					f'Enter the percentage of {components[i]} in the mix. You can also type Bal (balance gas) for auto-calculation of the %:')

			while not isinstance(components_percentages[i], Decimal):

				components_percentages[i] = input()

				if components_percentages[i] == 'Bal':
					# Only calculate balance gas amount of its the last component in the mix
					if not i == num_of_components - 1:
						print(
							f'You can only use the Bal calculation feature for the last component. Enter a numberic value or start over:')
						continue

					else:
						# Calculate balance gas amount by subtracting the sum of the other components_percentages from 100
						components_percentages[i] = 100 - sum(
							components_percentages[i] for i in range(len(components_percentages)) if
							not components_percentages[i] == 'Bal')
						break

				try:
					components_percentages[i] = Decimal(components_percentages[i])
				except InvalidOperation:
					print(f'The component percentage must be a number (e.g. 10, 10.0) - try again:')

		# Merge the two lists into a dict
		self.components = dict(zip(components, components_percentages))

	def percent_to_mass(self, component, component_percentage):
		"""
		Converts the percent by volume of a component to its mass (kilograms)
		:param component: The molecular/atomic symbol for the gas
		:type component: str
		:param component_percentage: The percentage of the cylinder that will be filled with this component
		:type component_percentage: decimal.Decimal
		:return decimal.Decimal: The mass (kg) of the gas component in the mixture
		"""

		component_percentage = component_percentage / 100

		# Get the size of the cylinder in moles from its cylinder_size code
		cyl_size_moles = CYL_SIZES_MOLES_DICT[self.cylinder_size]

		# Get # of moles of the component required
		component_moles = cyl_size_moles * component_percentage

		# Convert moles --> kg using the component's molar mass
		return round_number(component_moles * COMPONENTS_MOLAR_MASS_DICT[component])

	def calculate_mix_makeup(self):
		"""
		Calculates the masses of each component required to make the specified mix and sets self.components_masses

		:return: None
		"""

		components = self.components

		# Get the kg mass for each component, add to a dict
		components_masses_kg_dict = {}
		for component, component_percentage in components.items():
			components_masses_kg_dict[component] = (self.percent_to_mass(component=component,
																		 component_percentage=component_percentage))

		self.components_masses = components_masses_kg_dict

	def print_result(self):
		"""
		Prints the results to the console in a decent looking way

		:return: None
		"""

		components_masses = self.components_masses

		print('\n')
		print('--------------- RESULTS ---------------')
		for component, component_mass in components_masses.items():
			print(f' {component}                             {component_mass} kg')
		print('\n')

	def check_total_percentage(self):
		"""
		Sums the percentage values entered by the user to see if they add up to 100. If not, a warning
			message is given to the user. If they sum to 100, nothing happens. If not, the warning is
			sent to stdout

		"""

		if sum(self.components.values()) != 100:
			print(f"NOTE: The component %'s you entered do not sum to 100")


# Run CLI program on loop so that a) Console stays open and b) User can calculate multiple mixes
while True:
	# Create a new GasMixture instance
	mix = GasMixture()

	# What size gas cylinder is it?
	mix.set_cylinder_size()

	# How many different components are there in the gas mixture?
	mix.set_number_of_components()

	# What are the different components and what volume % do they contribute to the mix?
	mix.get_component_info()

	# If the mix's components' percentages don't sum to 100, give the user a warning message
	mix.check_total_percentage()

	# Calculate the mass (in kg) for each component
	mix.calculate_mix_makeup()

	# Display results in console
	mix.print_result()
