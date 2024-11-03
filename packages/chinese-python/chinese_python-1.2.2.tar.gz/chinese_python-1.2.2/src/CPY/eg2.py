import sys,math

pi = math.pi

class cercle:
        def __init__(self,r):
                try:
                        r = int(r)
                        self.r = r
                except TypeError or ValueError:
                        print("some error happen")
                        sys.exit()

        def D(self):
                return 2*self.r

        def C(self,float_number = 'unlimited'):
                if isinstance(float_number,str):
                        return 2*pi*self.r
                elif isinstance(float_number,int):
                        k = 2*pi*self.r*10**float_number
                        return int(k/10**float_number)
                else:
                        print("some error happen")
                        sys.exit()

        def S(self,float_number = 'unlimited'):
                if isinstance(float_number,str):
                        return pi*self.r**2
                elif isinstance(float_number,int):
                        k = pi*self.r**2*10**float_number
                        return int(k/10**float_number)
                else:
                        print("some error happen")
                        sys.exit()

if __name__ == '__main__':
        k=cercle(10)
        print(k.D())
        print(k.r)
        print(k.C(5))
        print(pi)
        print(k.S())
