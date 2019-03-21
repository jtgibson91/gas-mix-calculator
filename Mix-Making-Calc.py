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

SUPPORTED_CYL_SIZES = ('H', 'J')
H_CYL_SIZE_MOL = 250
J_CYL_SIZE_MOL = 350

CYL_SIZES_MOLES_DICT = {

	'H': H_CYL_SIZE_MOL,
	'J': J_CYL_SIZE_MOL
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


def get_cylinder_size():
	""" 
	Gets the cylinder size input from the user and validates the input

	:return str: 'H' or 'J'; the gas cylinder type
	"""

	print('Enter the clyinder size (H or J):')

	cyl_size = None
	# Loop until user enters valid input
	while cyl_size not in SUPPORTED_CYL_SIZES:

		cyl_size = input()

		if cyl_size not in SUPPORTED_CYL_SIZES:
			print('The cylinder size must be either H or J - try again:')

	return cyl_size


def get_number_of_components():
	""" 
	Gets the # of gas components that will make up the mix from the user  and validates the input

	:return int: # of gas components
	"""

	print(f'Enter the # of components ({MIN_NUMBER_OF_COMPONENTS}-{MAX_NUMBER_OF_COMPONENTS}): ')

	num_components = None
	while num_components not in range(MIN_NUMBER_OF_COMPONENTS, MAX_NUMBER_OF_COMPONENTS+1):

		num_components = input()

		try:
			num_components = int(num_components)
		except ValueError:
			print(f'The # of components must be a number between {MIN_NUMBER_OF_COMPONENTS} and {MAX_NUMBER_OF_COMPONENTS} - try again:')
			continue

		if num_components not in range(MIN_NUMBER_OF_COMPONENTS, MAX_NUMBER_OF_COMPONENTS+1):
			print(f'The # of components must be between {MIN_NUMBER_OF_COMPONENTS} and {MAX_NUMBER_OF_COMPONENTS} - try again:')

	return num_components


def get_component_info(number_of_components):
	""" 
	Gets the gas components and their corresponding proportions from the user

	:param number_of_components: The # of chemical components making up the gas mixture
	:type number_of_components: int

	:return two lists: List 1 holds the gas components (list of str). List 2 holds the respective percentages for the gas 
	components (list of decimal.Decimal)
	"""

	# Lists for holding user input
	# Initialize them with None so we can access those indices before data is added
	components = [None for i in range(number_of_components)]
	components_percentages = [None for i in range(number_of_components)]

	# For each component, prompt the user for data on the command line and validate it
	for i in range(number_of_components):

		supported_components_str = ', '.join([i for i in SUPPORTED_COMPONENTS])

		print(f'Enter component #{i+1} gas type (must be one of the following {supported_components_str}):')

		while components[i] not in SUPPORTED_COMPONENTS:

			components[i] = input()

			if components[i] not in SUPPORTED_COMPONENTS:
				del components[i]
				print(f'The component must be one of these {SUPPORTED_COMPONENTS} - try again:')

		print(f'Enter the percentage of {components[i]} in the mix (e.g. 3.5):')

		while not isinstance(components_percentages[i], Decimal):

			components_percentages[i] = input()

			if components_percentages[i] == 'Bal':
				# Only calculate balance gas amount of its the last component in the mix
				if not i == number_of_components - 1:
					print(f'You can only use the Bal calculation feature for the last component. Enter a numberic value or start over:')
					continue

				else:
					# Calculate balance gas amount by subtracting the sum of the other components_percentages from 100
					components_percentages[i] = 100 - sum(components_percentages[i] for i in range(len(components_percentages)) if not components_percentages[i] == 'Bal')
					break

			try:
				components_percentages[i] = Decimal(components_percentages[i])
			except InvalidOperation:
				print(f'The component percentage must be a number (e.g. 10, 10.0) - try again:')

	return components, components_percentages


def percent_to_mass(component, cylinder_size, component_percentage):
	""" 
	Converts the percent by volume of a component to its mass (kilograms)

	:param component: The molecular/atomic symbol for the gas
	:type component: str
	:param cylinder_size: The size of the cylinder to be filled. Either 'H' or 'J'
	:type cylinder_size: str
	:param component_percentage: The percentage of the cylinder that will be filled with this component
	:type component_percentage: decimal.Decimal


	:return decimal.Decimal: The mass (kg) of the gas component in the mixture
	"""

	component_percentage = component_percentage/100
	
	# Get the size of the cylinder in moles from its cylinder_size code
	cyl_size_moles = CYL_SIZES_MOLES_DICT[cylinder_size]

	# Get # of moles of the component required
	component_moles = cyl_size_moles * component_percentage

	# Convert moles --> kg using the component's molar mass
	return round_number(component_moles * COMPONENTS_MOLAR_MASS_DICT[component])


def calculate_mix_makeup(components, components_percentages):
	""" 
	Calculates the masses of each component required to make the specified mix

	:param components: List holding the gas components
	:type components: list of str
	:param components_percentages: List holding the gas components percentages
	:type components_percentages: list of decimal.Decimal

	:return a dict {component1: component1_mass, 
					etc.. }
	"""

	# Merge the two lists into a dict
	components_dict = dict(zip(components, components_percentages))

	# Get the kg mass for each component, add to a dict
	components_masses_kg_dict = {}
	for component, component_percentage in components_dict.items():
		components_masses_kg_dict[component] = (percent_to_mass(component=component, cylinder_size=cyl_size, 
																component_percentage=component_percentage))

	return components_masses_kg_dict


def print_result(components_masses):
	""" 
	Prints the results to the console in a decent looking way

	:param components_masses: dict holding the gas components and their masses
	:type components_masses: dict

	:return None
	"""

	print('\n')
	print('--------------- RESULTS ---------------')
	for component, component_mass in components_masses.items():
		print(f' {component}                             {component_mass} kg')
	print('\n')




# Run CLI program on loop so that a) Console stays open and b) User can calculate multiple mixes
while True:

	# What size gas cylinder is it?
	cyl_size = get_cylinder_size()

	# How many different components are there in the gas mixture?
	num_components = get_number_of_components()
	

	# What are the different components and what volume % do they contribute to the mix?
	components, components_percentages = get_component_info(number_of_components=num_components)

	# Be liberal and just let user know that their math is off
	if not sum(components_percentages) == 100:
		print('NOTE: your component percentages do not add up to 100')

	# Calculate the mass (in kg) for each component
	components_masses_kg_dict = calculate_mix_makeup(components=components, components_percentages=components_percentages)

	# Display results in console
	print_result(components_masses=components_masses_kg_dict)

