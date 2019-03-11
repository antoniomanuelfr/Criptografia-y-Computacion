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

def Miller_Rabin (p, pr=False):

    if p >= 5 and p %2 ==1:
        u,s = Descomponer (p-1)
        a = randint(2, p-2)
        if pr:
            print ("Estamos usando como testigo: a = ", a)
        res = potencia_modular(a,s,p)
        if pr:
            print ("{} ^ {} = {} mod {}".format(res,s,res,p))

        if res == 1 or res == p-1: 
            return True

        for i in range (1,u):
            res = potencia_modular(res,2,p)
            if pr:
                print ("{} ^ {} = {} mod {}".format(res,s*(2**i),res,p))
            if res == p-1:
                return True
            elif res ==1:
                return False
    return False

def primo(p, n=10, pr=False):

    for i in range (n):
        if not Miller_Rabin(p):
            if pr:
                print (p, " no es primo\n")
            return False
    if pr :
        print (p, " es posible primo\n")
    return True

def siguiente_primo(p): 

    aux = p+1 if p % 2 == 0 else p+2
    
    while not Miller_Rabin(aux): 
        aux += 2
    return aux
    
def primo_n_bits(n):
    sem = randint(2**n-1, 2**n)
    return siguiente_primo(sem)

def primo_fuerte(n):

    pr = siguiente_primo(n)
    while not primo( (pr-1) // 2): 
        pr = siguiente_primo(pr)
    return pr

if __name__ == '__main__':

    print (primo_n_bits(2))
    print (siguiente_primo(5))
    print(primo_fuerte(23))