import numpy as np
from unicodedata import normalize
import string

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


class TextoAnalisis:

    wordsBasics = ['QUE','UNA','CON','LOS','LAS','PARA','COMO','PERO','SOBRE','ESTE','PORQUE','TAMBIEN']
    trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)

    def textoBruto(self,file):
        text_res = ''
        text_raw = ''

        for char in file:

            val = ord(char.upper()) - ord('A')

            if val < 0:
                text_res = text_res + ''
            elif val <= ord('Z') - ord('A'):
                text_res = text_res + char.upper()
                text_raw = text_raw + char.upper()
            elif val == ord('Ñ') - ord('A'):
                text_res = text_res + 'Ñ'
                text_raw = text_raw + 'Ñ'
            elif val == ord(' ') - ord('A'):
                text_raw = text_raw + ' '
            
        return (text_res, text_raw)

    def __init__(self):
        self.file = open("QuijoteAnalisis.txt", "r").read()
        self.file = normalize('NFKC', normalize('NFKD', self.file).translate(self.trans_tab))
        
        self.rawTex, self.file = self.textoBruto(self.file)
        
        self.stats = {'NumApariciones' : 0, 'MediaApariciones' : 0.0, 'StdApariciones' : 0.0, 'Maximo' : 0, 'Minimo' : 0}
        self.aparionesCadenas = np.zeros(len(self.wordsBasics))
        self.uniqueWord = set()
    
    def procces(self):

        for word, ind in zip( self.wordsBasics, range(len(self.wordsBasics)) ):
            _, cantidad = apariciones(word, self.rawTex)

            self.aparionesCadenas[ind] = cantidad
        
        self.stats['NumApariciones'] = self.aparionesCadenas.sum()
        self.stats['MediaApariciones'] = self.aparionesCadenas.mean()
        self.stats['StdApariciones'] = self.aparionesCadenas.std()
        self.stats['Maximo'] = self.aparionesCadenas.max()
        self.stats['Minimo'] = self.aparionesCadenas.min()

    def analisis(self):
        palabras = self.file.split()

        print("La longitud de palabras es de {}".format( len(palabras) ))

        self.uniqueWord = set(palabras)