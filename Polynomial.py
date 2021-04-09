from numpy import sign
from sympy import symbols, pprint, poly


class Polynomial:
    def __init__(self, coefficients):
        if len([i for i in coefficients if i == 0]) == len(coefficients):
            self.coefficients = [0]
        else:
            coefficients = [i for i in coefficients]
            while coefficients[-1] == 0:
                coefficients.pop(-1)
            self.coefficients = coefficients
        self.roots = []

    def deg(self):
        return len(self.coefficients) - 1

    def __str__(self):
        ai_set = [str(self.coefficients[0])]
        for i in range(1, len(self.coefficients)):
            ai = self.coefficients[i]
            if ai == 0:
                continue
            if ai > 0 and ai != 1:
                ai_set.append(f"+ {ai}*(x**{i})")
            elif ai == 1:
                ai_set.append(f"+ (x**{i})")
            elif ai == -1:
                ai_set.append(f"- (x**{i})")
            else:
                ai_set.append(f"- {abs(ai)}*(x**{i})")
        return " ".join(ai_set)

    def __neg__(self):
        return Polynomial([-i for i in self.coefficients])

    def __add__(self, other):
        if self.deg() >= other.deg():
            w1 = self.coefficients[:]
            w2 = other.coefficients[:]
        else:
            w1 = other.coefficients[:]
            w2 = self.coefficients[:]
        for i in range(len(w2)):
            w1[i] = w1[i] + w2[i]
        return Polynomial(w1)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        self_coef = self.coefficients[:]
        other_coef = other.coefficients[:]
        addition = Polynomial(other_coef)
        sum = Polynomial([0])
        for i in range(len(self_coef)):
            sum = sum + addition.single_mul(self_coef[i], i)
        return sum

    def single_mul(self, a, pow):
        self_coef = self.coefficients[:]
        for i in range(pow):
            self_coef.insert(0, 0)
        for i in range(len(self_coef)):
            self_coef[i] *= a
        return Polynomial(self_coef)

    def __eq__(self, other):
        return self.coefficients == other.coefficients

    def __call__(self, x):
        return self.coefficients[0] + sum([self.coefficients[i]*x**i for i in range(1, self.deg()+1)])

    def roots_range(self):
        r = sum([abs(i) for i in self.coefficients])
        return max(1, r)

    def bisection_method(self, a, b, epsilon):
        x = (a+b)/2
        while self(x) == 0:
            self.roots.append(x)
        if len(self.roots) == self.deg():
            return None
        if abs(a-x) < epsilon:
            if self.new_root((a+x)/2, epsilon):
                self.roots.append((a+x)/2)
            return None
        if sign(self(a)) != sign(self(x)):
            self.bisection_method(a, x, epsilon)
        if sign(self(b)) != sign(self(x)):
            self.bisection_method(x, b, epsilon)

    def get_roots(self, epsilon=0.00001):
        if self.deg() == 0:
            if self == Polynomial([0]):
                return "(-oo; oo)"
            else:
                self.roots = [] #"EmptySet"
                return self.roots
        if self.deg() == 1:
            self.roots.append(-self.coefficients[0]/self.coefficients[1])
            return self.roots
        if self.deg() == 2:
            a = self.coefficients[2]
            b = self.coefficients[1]
            c = self.coefficients[0]
            delta = b**2 - 4 * a * c
            if delta < 0:
                self.roots = [] #"EmptySet"
                return self.roots
            else:
                self.roots.append((-b + delta**(1/2))/2*a)
                x2 = (-b - delta**(1/2))/2*a
                if self.new_root(x2, 0.0001):
                    self.roots.append(x2)
                return self.roots
        r = self.roots_range()
        n = 1/(epsilon*16) + 1
        for i in range(int(n)+1):
            self.bisection_method(-r+i*(2*r/n), -r+(i+1)*(2*r/n), epsilon)
        if not len(self.roots) == self.deg():
            derivative = self.derivative()
            for i in range(self.deg() * int(n) + 1):
                derivative.bisection_method(-r+i*(2*r/n), -r+(i+1)*(2*r/n), epsilon)
            for i in derivative.roots:
                if self.new_root(i, epsilon) and -epsilon < self(i) < epsilon:
                    self.roots.append(i)
        self.roots = sorted([round(i, 4) for i in self.roots])
        return self.roots

    def new_root(self, root, epsylon):
        for i in self.roots:
            if i - epsylon < root < i + epsylon:
                return False
        return True

    def derivative(self):
        return Polynomial([(i+1)*self.coefficients[i+1] for i in range(len(self.coefficients[1:]))])

    def sympyfy(self, x):
        expr = 0
        for i in range(len(self.coefficients)):
            expr += self.coefficients[i]*x**i
        return poly(expr, x)

if __name__ == "__main__":
    x = symbols("x")
    w = Polynomial((1, 2, 3, 4, 5))
    pprint(w.sympyfy(x))
#    w1 = Polynomial((0, 1))
 #   w2 = Polynomial((-3, 1))
  #  w3 = Polynomial((-1, 1))
    #print((w*w1*w3*w3*w2).get_roots())
   # print(Polynomial((1, -2, 1)))
    #print(w)
    #print(Polynomial((0, 1)).get_roots())



