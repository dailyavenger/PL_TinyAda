#chario

class Chario:

    def chario(self):
        fname = input("Enter the input file name: ")
        f = open(fname, 'r')
        t = []

        while True:
            text = f.readline()
            if not text:
                break
            tmp = list(text)
            t = t + tmp

        cha = []

        for i in t:
            # 대소문자
            if ord(i) >= 65 and ord(i) <= 90:
                cha.append(chr(ord(i) + 32))
            else:
                cha.append(i)
        chaRet = ''.join(cha)
        return chaRet


    def reportErrors(self):
        print("Error Ocurred")
