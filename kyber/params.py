
class Params:
    def __init__(
        self,
        n=16,
        q=3329,
        k=2,
        eta1=3,
        eta2=2,
        du=10,
        dv=4,
    ):
        self.n = n
        self.q = q
        self.k = k
        self.eta1 = eta1
        self.eta2 = eta2
        self.du = du
        self.dv = dv


PARAMS = Params()