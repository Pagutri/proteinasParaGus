# En la clase Gen() seria mejor utilizar la clase bool para heredar sus propiedades
# En el inicializador, pueden definir una opcion string para activar o dejar en default si es generacion random, o no.
# __str__ no parece necesario. pueden acceder desde self.alelo
# Falta metod para mutar
# Fatla variabble, paara definir probabilidad de mutacion. Caso default igual a 0. El usuario deberia activar la muatacion
# Todo en ingles
# Distribuir en accesores, mutadores, y metodos
# revisar excepciones en lugar de if elif o else

# Utilizar metodo getMutabilidad() en el inicializador
# 

import random

class Gen:
	"""
	Esta clase se encarga de crear genes (alelos) binarios.

	El constructor puede recibir hasta dos variables, que son:
	1. aleatorio. Tipo bool. Se genera un alelo de valor aleatorio si es True,
	y toma el valor especificado por el usuario, si es False. Su valor por 
	default es True.
	2. bit. Tipo entero. Es el valor que el usuario desea que tenga el bit. Es
	0 por default.

	El método mutarAlelo() recibe la probabilidad de mutación de un alelo, que es
	cero por default. Con esa probabilidad, invierte el valor del alelo.

	El método getAlelo() sirve para acceder al alelo desde otras clases.

	Nota: falta código que evite que el usuario ingrese un valor distinto de 0
	y 1 para bit o fuera del intervalo [0,1] para mutacion.
	"""

	numGen = 0

# Inicializador

	def __init__(self, myGen = 0, aleatorio = False, bit = 0):

                Gen.numGen = Gen.numGen + 1

                self.mutacion = 0

                if isinstance(myGen, Gen):
                        self.alelo = myGen.getAlelo()

                elif aleatorio:
                        self.alelo = random.randint(0,1)
                else:
                        self.alelo = bit


# Accesores

	def getAlelo(self):
		return self.alelo

	def getMutabilidad(self):
		return self.mutacion

	def getNumGen(self):
		return Gen.numGen

# Mutadores
	

	def setAlelo(self, a):
		self.alelo = a

	def setMutabilidad(self, a):
		self.mutacion = a

# Metodos

	def __str__(self):
                return str(self.getAlelo())

	def mutarAlelo(self):
		if random.random() <= self.mutacion:
			self.alelo = (self.alelo + 1 ) % 2


