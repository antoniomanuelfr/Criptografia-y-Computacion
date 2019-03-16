import random


def potencia_modular(x, y, z):
    aux = 1
    while y > 0:
        if y % 2 == 1:
            aux = (aux * x) % z
        x *= x
        y = y // 2
        x %= z
    return aux


def descomponer(a):
    c = 0
    b = a
    while b % 2 == 0:
        c = c + 1
        b = b // 2
    return c, b


def miller_rabin(p, ft=None, pr=False):
    if p >= 5 and p % 2 == 1:
        u, s = descomponer(p - 1)

        testigo_actual = random.randint(2, p - 2) if ft is None else ft

        if pr:
            print("Estamos usando como testigo: a = ", testigo_actual)

        res = potencia_modular(testigo_actual, s, p)

        if pr:
            print("{} ^ {} = {} mod {}".format(res, s, res, p))

        if res == 1 or res == p - 1:
            return True

        for i in range(1, u):
            res = potencia_modular(res, 2, p)
            if pr:
                print("{} ^ {} = {} mod {}".format(res, s * (2 ** i), res, p))
            if res == p - 1:
                return True
            elif res == 1:
                return False

    return False


def buscar_n_falsos_testigos(p, n=None, pr=False):
    falsos_testigos = []

    if p >= 5 and p % 2 == 1:
        u, s = descomponer(p - 1)
        rango = range(2, p - 2) if n is None else range(n)
        for aux in rango:
            a = random.randint(2, p - 2) if n is not None else aux
            res = potencia_modular(a, s, p)

            if res == 1 or res == p - 1:
                falsos_testigos.append(a)

            else:

                if pr:
                    print("{} ^ {} = {} mod {}".format(res, s, res, p))

                for i in range(1, u):
                    res = potencia_modular(res, 2, p)
                    if pr:
                        print("{} ^ {} = {} mod {}".format(res, s * (2 ** i), res, p))

                    if res == p - 1:
                        falsos_testigos.append(a)
                    elif res == 1:
                        break

    return falsos_testigos


# def buscar_falsos_testigos(p, pr=False):
#     falsos_testigos = []

#     if p >= 5 and p % 2 == 1:
#         u, s = descomponer(p - 1)
#         for a in range(2, p - 2):

#             res = potencia_modular(a, s, p)

#             if res == 1 or res == p - 1:
#                 falsos_testigos.append(a)

#             else:

#                 if pr:
#                     print("{} ^ {} = {} mod {}".format(res, s, res, p))

#                 for i in range(1, u):
#                     res = potencia_modular(res, 2, p)
#                     if pr:
#                         print("{} ^ {} = {} mod {}".format(res, s * (2 ** i), res, p))

#                     if res == p - 1:
#                         falsos_testigos.append(a)
#                     elif res == 1:
#                         break

#     return falsos_testigos


def es_primo(p, testigo=None, n=10, pr=False):
    for i in range(n):

        if not miller_rabin(p=p, ft=testigo, pr=False):

            if pr:
                print(p, " no es primo\n")

            return False
    if pr:
        if testigo is None:
            stri = "{} es posible primo".format(p)
        else:
            stri = "{} es posible primo usando como testigo {}".format(p, testigo)
        print(stri)

    return True


def siguiente_primo(p):
    aux = p + 1 if p % 2 == 0 else p + 2

    while not miller_rabin(p=aux, ft=None, pr=False):
        aux += 2
    return aux


def primo_fuerte(n):
    prmo = siguiente_primo(n)
    while not es_primo((prmo - 1) // 2):
        prmo = siguiente_primo(prmo)

    return prmo


def primo_fuerte_n_bits(n):
    sem = random.randint(2 ** (n - 1), 2 ** n)

    primo = primo_fuerte(sem)
    cont = 0
    while primo > 2 ** n:
        print("{} es mayor que 2^{} con la semilla {}".format(primo, n, sem))

        sem = random.randint(2 ** (n - 1), 2 ** n)
        primo = primo_fuerte(sem)

        cont += 1
        if cont == 10:
            break

    return primo


def primo_n_bits(n):
    sem = random.randint(2 ** (n - 1), 2 ** n)

    primo = siguiente_primo(sem)
    cont = 0
    while primo > 2 ** n:
        print("{} es mayor que 2^{} con la semilla {}".format(primo, n, sem))

        sem = random.randint(2 ** (n - 1), 2 ** n)
        primo = siguiente_primo(sem)

        cont += 1
        if cont == 10:
            break

    return primo


if __name__ == '__main__':

    prueba_primos = [13, 561, 6299, 921]
    # Apartado 1
    for prueba in prueba_primos:
        es_primo(p=prueba, testigo=None, n=10, pr=True)
        # Apartado 2
        es_primo(p=prueba, testigo=random.randint(2, prueba - 1), n=1, pr=True)
        print(
            "Los falsos testigos de {} son: \n{}\n".format(prueba, buscar_n_falsos_testigos(prueba, n=None, pr=False)))

        # Apartado 3
        print("El siguiente primo a {} es: {}".format(prueba, siguiente_primo(prueba)))

        # Apartado 4
        print("El siguiente primo fuerte a {} es: {}".format(prueba, primo_fuerte(prueba)))
    print("\n\n")
    # Apartado 5
    n_bits = 8
    print("Un primo fuerte de {} bits es: {}".format(n_bits, primo_fuerte_n_bits(n_bits)))

    # Apartado 6
    lista_pruebas = [6601, 8911, 10585, 15841, 29341]
    for pruebas in lista_pruebas:
        print("Los falsos testigos de {} son: \n{}\n".format(pruebas,
                                                             buscar_n_falsos_testigos(pruebas, n=None, pr=False)))

    # Apartado 7

    compuesto_varios_primos = 1
    for _ in range(5):
        primo1 = primo_n_bits(5)
        print("Multiplicamos {} por {}".format(compuesto_varios_primos, primo1))
        compuesto_varios_primos *= primo1

    print("El numero compuesto por varios primos pequeños es: {}".format(compuesto_varios_primos))

    primo2 = primo_n_bits(15)
    primo3 = primo_n_bits(10)
    compuesto_primos_grandes = primo2 * primo3
    print("El numero compuesto por dos primos grandes {} * {} es: {}".format(primo2, primo3, compuesto_primos_grandes))

    lista = [compuesto_varios_primos, compuesto_primos_grandes]
    n_veces = 200
    for j in lista:
        print("Los {} falsos positivos de {} son: \n{}\n".format(n_veces, j, buscar_n_falsos_testigos(j, n_veces, pr=False)))
    # Apartado 8

    lista = [3215031751, 2199733160881]
    for j in lista:
        print("Los {} falsos positivos de {} son: \n{}\n".format(n_veces, j, buscar_n_falsos_testigos(j, n_veces, pr=False)))
