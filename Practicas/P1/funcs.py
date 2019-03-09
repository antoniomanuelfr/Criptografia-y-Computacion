from random import randint

def potencias(a,b,m):
    if m ==0:
        return -1
    aux = a 
    for i in range (b-1):
        aux = (aux * a)%m

    return aux 

def potencia_modular(x,y,z):
    aux = 1
    while y>0:
        if (y%2==1):
            aux = (aux * x)%z
        x *= x
        y = y//2
        x%=z
    return aux

def func3(n): 
    res = []
    for i in range (n):
        if potencia_modular(i,2,n) == 1:
            res.append(i)
    return res

def Descomponer (a): 
    cont = 0 
    b = a
    while b % 2 == 0: 
        cont = cont + 1
        b = b //  2
    return cont, b

def Miller_Rabin (p):

    if p >= 5 and p %2 ==1:
        u,s = Descomponer (p-1)
        a = randint(2, p-2)
        print ("Estamos usando como testigo: a = ", a)
        res = potencia_modular(a,s,p)

        print (a, "^", s, " = ", res, "mod ", p)

        if res == 1 or res == p-1: 
            return True

        for i in range (1,u):
            a *= a
            res = potencia_modular(a,s,p)
            print (a, "^", s*(2**i), " = ", res, "mod ", p)

            if res == p-1:
                return True
            elif res ==1:
                return False
    return False

if __name__ == '__main__':

    # p= 879976242195951958890801816612768566943805170226410617823301865416003514546684111640331356490455690766475339038983303063831818394885482954417406863802340357540397021808027209610884076158915519334125353771492979
    # p+=2
    # p=2199733160881
    # print (potencia_modular(21997331,p-1, p))
    # print (potencia_modular(2193323,p-1, p))
    # print (potencia_modular(4434342,p-1, p))
    # print (potencia_modular(2,p-1, p))
    # print (potencia_modular(432423444,p-1, p))
    # print (potencia_modular(20,35, 561))

    # #si m es primo x^2 -1 =0 tiene dos soluciones en zn
    # # si m es impar y producto de n primos x^2 -1 = 0 tiene 2^n soluciones 
    for i in range (5):
        if Miller_Rabin(561):
            print ("Posible primo\n")
        else:
            print ("No es primo\n")

