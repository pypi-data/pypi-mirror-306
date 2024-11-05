from .__init__ import *
class SolverFormulasStore(BASE,Template):
    __tablename__="SolverFormulasStore"
    SFSiD=Column(Integer,primary_key=True)
    Script=Column(LargeBinary,default=b'')
    Description=Column(String,default="Tell Me What this Script DOES")
    Notes=Column(String,default="Addition Notes About this Script")
    DTOE=Column(DateTime,default=datetime.now())
    LastUsed=Column(DateTime,default=None)
    HTEXT=Column(String,default="Tell Me How to use this in the KISS principle (KEEP IT SIMPLE, STUPID[Don't be Bitch about either, yall treated me like I was a Crazy-Ass Mother-Fucker, now its your turn to eat God-Damned Shit Fresh of the Plate of I Fucking Told you so, asshole, and you know why that is? Because...])")

    def __init__(self,**kwargs):
        for k in kwargs.keys():
            if k in [s.name for s in self.__table__.columns]:
                setattr(self,k,kwargs.get(k))

SolverFormulasStore.metadata.create_all(ENGINE)