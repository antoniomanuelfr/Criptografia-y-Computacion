import Funciones as fc 


if __name__ == "__main__":
    # Texto 1 

    # Texto 2
    texto2 = fc.TextBase("IsmaelAntonio2.txt")
    texto2.printStats()

    print (fc.vignere_key_length(str(texto2)))