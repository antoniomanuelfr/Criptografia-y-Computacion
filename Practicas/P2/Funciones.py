# -*- coding: utf-8 -*-
"""
Numpy usado para la generacion de arrays de forma automatica
y mejorando la eficiencia de su utilizacion ademas de aportar 
funcionalidad extra en el futuro:
            Funciones usadas
            ----------------
    - numpy.zeros
    - numpy.sum
    - scipy.stats.mode
"""
import numpy as np
from scipy import stats

def cadenatolista(cadena):
    """
    Parameters
    --------------

    cadena : string con el texto a analizar solo con las mayusculas

    Brief
    --------------
    Funcion para transformar las cadenas de texto en arrays numéricos
    señalando el número al que pertenecen, toma cuidado de las ñ para que
    sean la letra 14.

    TODO Puede realizar este mismo calculo independiente de si la cadena tiene
    minusculas  existen valores extraños.
    """

    l = np.zeros(len(cadena), dtype=np.uint8)
    
    for s, pos in zip( cadena, range(len(cadena)) ):
        x = ord(s)
        if x == 32:
            l[pos] = 0xff
        elif x < 79:
            l[pos] = x-65
        elif x == 209:
            l[pos] = 14
        else:
            l[pos] = x-64

    return l

def listatocadena(l):
    """
    Parameter
    -------------

    l: array numerico el cual simboliza los elementos que 
       aparecen en el texto riginal

    Return
    -------------

    s: string con las letras colocadas segun su aparicion en
       el array original
    
    """
    s = ''
    
    for x in l:
        if x == -1:
            s = s + ' '
        elif x <= 13:
            s = s + chr(x+65)
        elif x == 14:
            s = s + 'Ñ'
        else:
            s = s + chr(x+64)
    
    return s


def frecuencias(texto):
    """
    Parameter
    ------------

    texto: string del texto el cual vamos a analizar sus frecuencias

    Return
    ----------

    tabla: numpy array de uint con 27 posiciones simbolizando el numero de 
           apariciones de cada letra
    """
    tabla = np.zeros(27, dtype=np.uint)
    lista = cadenatolista(texto)

    for x in lista:
        tabla[x] = tabla[x]+1
    
    return tabla


def indice_coincidencia(texto, frec = None):
    """
    Parameter
    -------------

    texto: string representando el texto a analizar 

    Return
    -------------

    indexc: numpy array de 27 posiciones de tipo float con los indices de coincidencias
            de cada una de las diferentes letras del abecedario
    """
    if frec is None:
        tabla = frecuencias(texto)
    else:
        tabla = frec

    num_caracteres = np.sum(tabla)
    indexc = np.zeros(len(tabla), dtype=np.float)

    for id in range(len(tabla)):
        indexc[ id ] = ( tabla[id] * (tabla[id] - 1)) / (num_caracteres * ( num_caracteres-1 ) )

    return indexc


def divide_cadena(cadena,n):
    """
    Parameter
    ------------

    cadena : string con el texto el cual queremos dividir en pequeñas partes
    n : entero indicando de cuantos elementos van a realizarse las divisiones

    Return
    ------------

    subcadena : list con las subcadenas encontradas
    """
    subcadenas = []
    
    for i in range(n):
        subcadenas.append('')
    
    j = 0
    
    for x in cadena:
        subcadenas[j] = subcadenas[j] + x
        j = (j+1)%n
    
    return subcadenas


def cifra_vigenere(texto,clave):
    """
    Sustitucion polialfabetica por desplazamiento

    Parameter
    ---------------

    texto : Cadena de caracteres en mayuscula los cuales van a ser cifrados
    clave : Cadena de caracteres en mayuscula por la cual se van a cifrar los textos

    Return
    ---------

    texto_cifrado : String de mayusculas siendo el texto cifrado por la clave

    """
    lista_texto = cadenatolista(texto)
    lista_clave = cadenatolista(clave)
    (n,m) = (len(lista_texto),len(lista_clave))

    for i in range(n):
        lista_texto[i] = (lista_texto[i] + lista_clave[i%m])%27
    
    texto_cifrado = listatocadena(lista_texto)
    
    return texto_cifrado


def cifra_sustitucion(texto,permutacion):
    """
    Parameter
    -------------

    texto : string de letras mayusculas para cifrar
    permutacion : Diccionario de Strings, Strings donde el caracter que se encuentra en la clave
                se sustituye por el del valor

    Return
    --------------

    texto : cifrado haciendo uso de esta técnica
    """
    texto_cifrado = ''
    
    for x in texto:
        y = permutacion.get(x)
        texto_cifrado = texto_cifrado + y
    return texto_cifrado


def descifra_sustitucion(texto,permutacion):
    """
    Parameter
    --------------

    texto : string de mayusculas el cual debemos descifrar
    permitacion : Diccionario de String , String en el cual se dice cada caracter como 
                debe cifrarse

    Return
    --------

    texto_des : string que representa la aplicacion inversa del diccionario pasado
                es decir si existia un valor con el caracter en texto ese era cambiado
                por su valor de clave
    """
    texto_des = ''
    
    for x in texto:
        if x in permutacion:
            texto_des = texto_des + permutacion[x]
        else:
            texto_des = texto_des + x
    
    return texto_des 


def ngramas_repetidos(texto,n,m=5):
    """
    Brief
    -------------
    Cuenta el numero de repeticiones en un texto de una determinada
    cadena de texto


    Parameter
    --------------

    texto : string en mayusculas para analizar 
    n : tamanio de las agupaciones de letras que queremos usar
    m : numero de ngramas repetidos

    Return
    ---------------

    ngramasrep : ngramas que se repiten en el texto
    frecuencias : numero de veces que se repiten cada uno
    """

    ngramas = []
    ngramasrep = []
    frecuencias = []
    
    for i in range(m):
        frecuencias.append(1)
        ngramasrep.append(texto[ i : i+n ])
    
    minimo = 1
    
    for i in range(len(texto)-n):
        aux = texto[i:i+n]
        if aux not in ngramas:
            f = 1
            ngramas.append(aux)
            
            for j in range(i+1,len(texto)-n):
                if aux == texto[j:j+n]:
                    f+=1
            
            if f > minimo:
                k = frecuencias.index(minimo)
                ngramasrep[k] = aux
                frecuencias[k] = f
                minimo = min(frecuencias)
    
    return (ngramasrep,frecuencias)


def apariciones(cadena,texto):
    """
    Parameter
    -----------

    cadena : string con la cadena que queremos analizar, deben ser mayusculas
    texto : texto en el cual se van a buscar las apariciones de la cadena

    Result
    ------------

    posicion : lista de las apariciones de la cadena en el texto
    len(posicion) : numero de veces que esa cadena a aparecido
    """
    m = len(cadena)
    n = len(texto)
    posicion = []
    
    for i in range(n-m):
        if cadena == texto[i:i+m]:
            posicion.append(i)
    
    return (posicion,len(posicion))
     


def cifra_transposicion(texto,n):
    """
    Brief
    -------------
    Cifra el texto recorriendolo de n en n elemntos hasta terminar con el
    Ejemplo:
    
    texto = "HOLAMUNDO", n = 3
    text_cif = "HANOMDLUO"

    Parameter
    -------------

    texto : string de elementos en mayusculas para cifrar
    n : numero de elementos para saltar

    Result
    -------------
    
    texto_cif : texto recorrido de n en n elementos
    """
    m = len(texto)
    k = m % n
    texto_cif = ''
    
    for i in range(n):
        if i < k:
            aux = m // (n + 1)
        else: 
            aux = m//n
        for j in range(aux):
            texto_cif = texto_cif + texto[ i + n * j ]
    
    return texto_cif

def frecuencia_transposicion(file, n):
    frec = np.zeros((n,27), dtype=np.uint)

    for char, ind in zip( file, range(len(file)) ):
        charint = ord(char)

        if charint < 79:
            charint = (charint - 65) % 27
        elif charint == 209:
            charint = 14 
        elif charint >= 79:
            charint = (charint - 64 ) % 27

        frec[ind % n, charint] += 1
    
    return frec


def siguiente(m,n,x):
    """
    Parameter
    ------------

    m : tamanio del texto 
    n : entero que representa el tamanio de los saltos que se tomo
    x : posicion en el texto original

    Result
    ------------

    pos : entero representando la posicion que tiene en el texto 
        cifrado
    """
    aux = m % n
    aux2 = m // n
    
    if aux == 0:
        ultimo = -1
    else: 
        ultimo = aux * (aux2 + 1) - 1
    
    if ultimo == -1 and x == m-1:
        return -1
    elif x < ultimo:
        return x+1+aux2
    elif x >= m - aux2:
        return x + aux2 + 1 - m
    elif x > ultimo:
        return x+aux2
    else:
        return -1


def vignere_key_length(text, n=2):
    """
    Parameter
    ------------

    text : Texto cifrado al que se le va a buscar la longitud de la clave con la que se ha cifrado
    n : Partes en las que se va a dividir el texto

    Result
    ------------

    n : Longitud de la clave
    """

    if n > 23: 
        return -1
    
    ic_mean = 0
    for i in divide_cadena(text, n):
        ic_mean += sum(indice_coincidencia(i))
    ic_mean /= n
    if ic_mean > 0.07:
        return n
    else: 
        return vignere_key_length(text,n+1)

def ocurrencias(cadena,texto,n):
    """
    Brief
    --------
    Cuenta el numero de apariciones de una cadena suponiendo 
    que esta se ha recorrido de n en n elementos, ppor tanto 
    lo que realiza es el conteo de n en n elementos.

    Parameter
    -----------

    cadena : string en mayusculas que comparar en el texto
    texto  : string en mayusculas siendo este el texto cifrado
    n      : tamanio de los saltos dados.

    Result
    ----------

    ocur   : numero de ocurrencia de la cadena tomandose los elementos
             de n en n saltos
    """ 
    l = len(texto)
    k = len(cadena)
    ocur = 0
    
    for i in range(l):
        contador = i
        cadenab = ''
    
        for j in range(k):
            if contador == -1:
                cadenab = cadenab + ' '
                contador = 0
            else:
                cadenab = cadenab + texto[contador]
                contador = siguiente(l,n,contador)
    
        if cadena == cadenab:
            ocur +=1
    
    return ocur

class TextBase:

    """
    Clase base para el procesado de textos, en la cual se toma como parametro
    un path a un texto el cual se lee y se extraen atributos basicos

    Atributes
    --------------

    file : Texto leido
    frec : numpy array con las frecuencias de cada letra en el texto
    indes_c : numpy array con el indice de coincidencia de cada letra
    stats : Estadisticas basicas del texto, numero de letras, indice coincidencia total, valor medio de aparicion de cada letra
            valor maximo de aparicion, valor minimo, desviacion tipica de aparicion
    """

    def __init__(self, path):
        self.file = open(path, "r").read()
        self.frec = frecuencias(self.file)
        self.indes_c = indice_coincidencia(self.file,self.frec)
        self.stats = { 'longitud' : len(self.file),                       'media':self.frec.mean(),
                       'ic'       : self.indes_c.sum(),                   'max'  :self.frec.max() ,
                       'min'      : self.frec.min(),                      'des'  :self.frec.std()  }
    
    def __str__(self):
        return self.file
    
    def printStats(self):
        print("\tStadistics\nLongitud: {}\tMedia: {}\t Indice de coin.: {}\nMaximo: {}\tMinimo: {}\tStandar: {}"
            .format(self.stats.get('longitud'), self.stats.get('media'), self.stats.get('ic'),
                    self.stats.get('max'),      self.stats.get('min'),   self.stats.get('des') ))

class SustitutionText (TextBase):

    """
    Clase que hereda de TextBase la cual esta pensada para textos cifrados con sustitucion
    mono alfabética, en este texto se dan las utilidades basicas para resolver sustituciones
    de este tipo.

    Atributes
    -------------------
    
    [static] alfabOrd : Array de caracteres en orden alfabetico
    [static] basicOrd : Array de caracteres en orden de mayor frecuencia en español

    order : Array con las posiciones de las letras segun su frecuencia
    perm  : permutacion basica a aplicar para decodificar
    """

    alfabOrd = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ'
                , 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    basicOrd = ['E','A','O','S','R','N','I','D','L','C','T','U','M','P','B'
                , 'G', 'Y', 'V', 'Q', 'H', 'F', 'Z', 'J', 'Ñ', 'X', 'W', 'K']

    def __init__(self, path):
        super( ).__init__(path)
        self.order = np.argsort( self.frec )[::-1]
        self.perm = {letter: self.alfabOrd[changed] for letter,changed in zip( self.basicOrd, self.order ) }

    def generatePermutaion(self):
        aux = np.array([ x + (np.random.random_sample() - 0.5) * self.stats.get('des') for x in self.frec])
        self.order = np.argsort( - aux )

        for letter,changed in zip( self.basicOrd, self.order ):
            self.perm[letter] = self.alfabOrd[changed]

    
    def aparicionesCadenas(self):
        preposiciones = ['QUE','UNA','CON','LOS','LAS','PARA','COMO','PERO','SOBRE','ESTE','PORQUE','TAMBIEN']

        prob_es = 0.0
        for item in preposiciones:
            _ ,cantidad = apariciones(item,descifra_sustitucion(self.file,self.perm))
            prob_es += cantidad / len(preposiciones)
        
        print()
        print(descifra_sustitucion(self.file,self.perm)[:200] )
    
    def decodeCesar(self,valor):

        frec_max = self.order
        permutation = dict().fromkeys(self.alfabOrd)

        for id in frec_max:
            letter = ord(self.alfabOrd[id])

            if letter < 79:
                letter = (letter - 65 - valor) % 27
            elif letter == 209:
                letter = (14 - valor) % 27
            elif letter >= 79:
                letter = (letter - 64 - valor) % 27
            
            if letter < 14:
                letter += 65
            elif letter == 14:
                letter = 209
            elif letter > 14:
                letter += 64

            permutation[self.alfabOrd[id]] = chr(letter)
        
        
        return descifra_sustitucion(self.file, permutation)
    
    def solveCesar(self, orderfrecuencias = None):

        if orderfrecuencias is None:
            frec_max = self.order
        else:
            frec_max = orderfrecuencias
            
        distances = []

        for ind, elem in zip(frec_max, self.basicOrd):
            letter = ord( self.alfabOrd[ind] )
            charele = ord(elem)

            if letter == 209:
                letter = 79
            elif letter >= 79:
                letter += 1
            
            if charele == 209:
                charele = 79
            elif charele >= 79:
                charele += 1

            distances.append( (letter - charele) % 27  )

        return stats.mode(np.array(distances))

          
  
