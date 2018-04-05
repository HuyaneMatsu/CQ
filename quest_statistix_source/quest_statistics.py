# -*- coding: utf-8 -*-
from math import ceil
from dereaddons_local import it_con,deconverter,sortedlist
from PIL import Image as PIL
from itertools import count

quest_types=[]
class length_meta(type):
    def __str__(cls):
        return cls.__name__
    def __init__(klass,name,bases,dict):
        quest_types.append(klass)
        type.__init__(klass,name,bases,dict)

class emergency(metaclass=length_meta):
    pass
class repeat(metaclass=length_meta):
    pass
class request(metaclass=length_meta):
    pass
class scout(metaclass=length_meta):
    pass

class GetOutException(Exception):
    pass
class req_base(object):
    def __init_subclass__(cls):
        cls.all={}
    def __new__(cls,*args,**kwargs):
        new=object.__new__(cls)
        try:
            cls.all[args[0]]=new
            return new
        except IndexError:
            pass
        try:
            cls.all[kwargs['name']]=new
            return new
        except KeyError:
            pass
        raise ValueError('missing value name')
    def __eq__(self,other):
        if isinstance(other,str):
            return self.name==other
        else:
            return self.name==other.name

global meat_cost
meat_cost=1/110
def stage_cost(v):
    if v=='colosseum':
        return 24*meat_cost
    if v=='raid':
        return 10*meat_cost
    return 30*meat_cost

class other_stages(req_base):
    def __init__(self,name):
        self.name=name
        self.stage={name:1}

other_stages('colosseum')
other_stages('raid')

class unit(req_base):
    def __init__(self,name,stage,boss=False):
        self.name=name
        self.stage=stage
        self.image=False
        self.boss=boss
    @property
    def chaptermetas(self):
        re=[]
        for v in self.stage:
            if v[6]=='C':
                p=v[:7]
            else:
                p=v[:9]
            if p not in re:
                re.append(p)
        return re

unit('goblin warrior',{'S2-E1-N-1-1':4,'S2-E1-N-1-2':2,'S2-E1-N-1-3':2}) #S2-E1-N-1-4/S2-E1-N-1-5 stage has 0
unit('goblin archer',{'S2-E1-N-1-1':6,'S2-E1-N-1-2':4,'S2-E1-N-1-4':3,'S2-E1-N-1-5':2}) #S2-E1-N-1-3 has 0
unit('mini ogre',{'S2-E1-N-1-1':1,'S2-E1-N-1-2':6,'S2-E1-N-1-3':4,'S2-E1-N-1-4':2,'S2-E1-N-1-5':6})
unit('goblin catapult',{'S2-E1-N-1-2':1,'S2-E1-N-1-3':4,'S2-E1-N-1-4':2,'S2-E1-N-1-5':5}) #S2-E1-N-1-1 has 0
unit('goblin champion',{'S2-E1-N-1-4':2,'S2-E1-N-1-5':1}) #S2-E1-N-1-1/S2-E1-N-1-2/S2-E1-N-1-3 has 0

unit('aggressive small ogre',{'S2-E1-N-1-1':1},boss=True)
unit('aggressive goblin catapult',{'S2-E1-N-1-2':1},boss=True)
unit('aggressive goblin champion',{'S2-E1-N-1-3':1},boss=True)
unit('scholar of the forest',{'S2-E1-N-1-4':1},boss=True)
unit('goblin chief',{'S2-E1-N-1-5':1},boss=True)


unit('red shadow rose charger',{'S2-E1-N-2-1':4,'S2-E1-N-2-2':8,'S2-E1-N-2-6':4})
unit('red shadow rose marksman',{'S2-E1-N-2-1':3,'S2-E1-N-2-2':2,'S2-E1-N-2-6':7})
unit('red shadow rose cavalry',{'S2-E1-N-2-6':2})
unit('blue shadow rose marksman',{'S2-E1-N-2-3':3,'S2-E1-N-2-4':5}) #S2-E1-N-2-5 has 0
unit('blue shadow rose charger',{'S2-E1-N-2-3':2,'S2-E1-N-2-4':4})
unit('blue shadow rose cavalry',{'S2-E1-N-2-3':2,'S2-E1-N-2-4':1})
unit('yellow shadow rose cavalry',{'S2-E1-N-2-5':3})
unit('yellow shadow rose marksman',{'S2-E1-N-2-5':4})
unit('yellow shadow rose cavalry',{'S2-E1-N-2-5':3})
unit('heavens cavalry soldier',{'S2-E1-N-2-8':2,'S2-E1-N-2-9':4})
unit('heavens cavalry sergeant',{'S2-E1-N-2-8':1,'S2-E1-N-2-9':1})
unit('blue chaos shadowdemon',{'S2-E1-N-2-7':2,})
unit('blue fury shadowdemon',{'S2-E1-N-2-7':3,})
unit('yellow chaos shadowdemon',{'S2-E1-N-2-8':2,'S2-E1-N-2-9':1,'S2-E1-N-2-10':1})
unit('yellow fury shadowdemon',{'S2-E1-N-2-8':2,'S2-E1-N-2-9':1,'S2-E1-N-2-10':1})
unit('red chaos shadowdemon',{'S2-E1-N-2-9':1,'S2-E1-N-2-10':2,'S2-E1-N-4-2':2,'S2-E1-N-4-3':1,'S2-E1-N-4-4':3,'S2-E1-N-4-5':4})#S2-E1-N-4-2 has 0
unit('red fury shadowdemon',{'S2-E1-N-2-9':1,'S2-E1-N-2-10':2,'S2-E1-N-4-2':1,'S2-E1-N-4-5':2})


unit('horifying red shadow rose charger',{'S2-E1-N-2-1':1},boss=True)
unit('horrifying red shadow rose marksman',{'S2-E1-N-2-2':1},boss=True)
unit('horrifying blue shadow rose cavalry',{'S2-E1-N-2-3':1},boss=True)
unit('shadow rose agent',{'S2-E1-N-2-4':1},boss=True)
unit('horrifying yellow shadow rose calvalry',{'S2-E1-N-2-5':1},boss=True)
unit('horrifying red shadow rose cavalry',{'S2-E1-N-2-6':1},boss=True)
unit('horrifying blue chaos shadowdemon',{'S2-E1-N-2-7':1},boss=True)
unit('shadow rose priest',{'S2-E1-N-2-8':1},boss=True)
unit('horrifying yellow fury shadowdemon',{'S2-E1-N-2-8':1},boss=True)
unit('holy cavalry sergeant',{'S2-E1-N-2-9':1},boss=True)
unit('hybrid shadowdemon',{'S2-E1-N-2-10':1},boss=True)



unit('warrat',{'S2-E1-N-3-1':6,'S2-E1-N-3-2':6,'S2-E1-N-3-3':4,'S2-E1-N-3-6':10,'S2-E1-N-3-8':8}) #S2-E1-N-3-4/S2-E1-N-3-5/S2-E1-N-3-7/S2-E1-N-3-9/S2-E1-N-3-10 has 0
unit('huntrat',{'S2-E1-N-3-1':5,'S2-E1-N-3-2':2,'S2-E1-N-3-4':2,'S2-E1-N-3-5':2,'S2-E1-N-3-6':6}) #S2-E1-N-3-3/S2-E1-N-3-7/S2-E1-N-3-8/S2-E1-N-3-9/S2-E1-N-3-10 has 0
unit('bigrat',{'S2-E1-N-3-5':3,'S2-E1-N-3-7':1,'S2-E1-N-3-8':10,'S2-E1-N-3-9':4,'S2-E1-N-3-10':5})#S2-E1-N-3-1/S2-E1-N-3-2/S2-E1-N-3-3 has 0
unit('bombrat',{'S2-E1-N-3-6':5,'S2-E1-N-3-8':6,'S2-E1-N-3-9':3,'S2-E1-N-3-10':2,})#S2-E1-N-3-1/S2-E1-N-3-2/S2-E1-N-3-3 has 0
unit('rotting mutarat',{'S2-E1-N-3-2':2,'S2-E1-N-3-3':5,'S2-E1-N-3-4':3,'S2-E1-N-3-5':3,'S2-E1-N-3-6':8,'S2-E1-N-3-7':6,'S2-E1-N-3-9':6,'S2-E1-N-3-10':6}) #S2-E1-N-3-8 has 0
unit('giant mutarat',{'S2-E1-N-3-4':3,'S2-E1-N-3-5':1,'S2-E1-N-3-7':5,'S2-E1-N-3-9':5,'S2-E1-N-3-10':5})#S2-E1-N-3-2/S2-E1-N-3-3/S2-E1-N-3-6/S2-E1-N-3-8 has 0
unit('poisonous spore',{'S2-E1-N-3-2':3,'S2-E1-N-3-3':5,'S2-E1-N-3-4':3,'S2-E1-N-3-5':3,'S2-E1-N-3-6':8,'S2-E1-N-3-7':6,'S2-E1-N-3-9':6,'S2-E1-N-3-10':6})



unit('dangerous warrat',{'S2-E1-N-3-1':1},boss=True)
unit('dangerous rottin mutarat',{'S2-E1-N-3-2':1},boss=True)
unit('ratman enthusiast',{'S2-E1-N-3-3':1},boss=True)
unit('dangerous giant mutarat',{'S2-E1-N-3-4':1,'S2-E1-N-3-9':1},boss=True)
unit('dangerous bigrat',{'S2-E1-N-3-5':1,'S2-E1-N-3-8':1},boss=True)
unit('dangerous huntrat',{'S2-E1-N-3-6':1},boss=True)
unit('hermit',{'S2-E1-N-3-7':1},boss=True)
unit('rudrat',{'S2-E1-N-3-10':1},boss=True)



unit('kitchen poltergeist',{'S2-E1-N-4-1':2,'S2-E1-N-4-2':1,'S2-E1-N-4-3':1,'S2-E1-N-4-4':3,'S2-E1-N-4-5':2})
unit('library poltergeist',{'S2-E1-N-4-1':2,'S2-E1-N-4-2':1,'S2-E1-N-4-3':2,'S2-E1-N-4-4':3,'S2-E1-N-4-5':1})
unit('mana mass',{'S2-E1-N-4-1':2,'S2-E1-N-4-2':6,'S2-E1-N-4-3':7,'S2-E1-N-4-4':11,'S2-E1-N-4-5':9,})

unit('turbulent kitchen poltergeist',{'S2-E1-N-4-1':1},boss=True)
unit('turbulent library poltergeist',{'S2-E1-N-4-2':1,'S2-E1-N-4-4':1},boss=True)
unit('bewitched priest',{'S2-E1-N-4-3':1},boss=True)
unit('bewitched magician',{'S2-E1-N-4-3':1},boss=True)
unit('horrifying red fury shadowdemon',{'S2-E1-N-4-4':1},boss=True)
unit('artificial god avenir',{'S2-E1-N-4-5':1},boss=True)


unit('elite goblin archer',{'S2-E1-C-1':18}) #only here
unit('elite goblin warrior',{'S2-E1-C-1':12}) #only here
unit('elite mini ogre',{'S2-E1-C-1':6}) #only here
unit('elite goblin catapult',{'S2-E1-C-1':2}) #only here
unit('elite goblin champion',{'S2-E1-C-1':1}) #only here

unit('windstrider',{'S2-E1-C-1':1},boss=True)
unit('catapult no.6',{'S2-E1-C-1':1},boss=True)
unit('crouching ox',{'S2-E1-C-1':1},boss=True)
unit('desperate goblin chief',{'S2-E1-C-1':1},boss=True)

unit('bouillabaisse',{'S2-E1-C-2':1},boss=True)
unit('dom peringnon',{'S2-E1-C-2':1},boss=True)
unit('matahari',{'S2-E1-C-2':1},boss=True)
unit('freed hybrid shadowdemon',{'S2-E1-C-2':1},boss=True)
unit('ancient regime',{'S2-E1-C-2':1},boss=True)

unit('georgia & gujarat & grease',{'S2-E1-C-3':1},boss=True)
unit('greof & feralt',{'S2-E1-C-3':1},boss=True)
unit('blind swordman ratoichi',{'S2-E1-C-3':1},boss=True)
unit('tyrant rudrat',{'S2-E1-C-3':1},boss=True)
unit('blind and foolish mother',{'S2-E1-C-3':1},boss=True)

unit('revived dom peringnon',{'S2-E1-C-4':1},boss=True)
unit('enhanced bouillabaisse',{'S2-E1-C-4':1},boss=True)
unit('the abandoned lion',{'S2-E1-C-4':1},boss=True)
unit('innocent avenir',{'S2-E1-C-4':1},boss=True)

class unitview():
    def __init__(self,unit):
        self.unit=unit
    def _str_builder(self):
        yield '<a class=\'title\'>'
        yield self.unit.name.title()
        yield '</a>'
        if self.unit.boss:
            yield ' (Boss)'
        yield '</br></br>Appearance: '
        yield '<table class=\'listing\'><tbody>'
        for k,v in self.unit.stage.items():
            yield '<tr><td>%s :</td><td>%s</td><td>%s</td></tr>'%(v,k,stagecut[k])
        yield '</tbody></table>'
    def __str__(self):
        return ''.join(self._str_builder())

class stagedict(list):
    def __init__(self,*args):
        list.__init__(self,args)
    def keys(self):
        return self
    def values(self):
        return tuple(1 for x in range(len(self)))
    def items(self):
        return tuple((v,1) for v in self)
    def __getitem__(self,key):
        if key in self:
            return 1
        else:
            raise KeyError(key)

class stage(req_base):
    limit=1
    def __init__(self,name,stage,popularity=9999,note=''):
        self.name=name
        self.stage=stage
        self.popularity=popularity
        self.note=note
    def __hash__(self):
        return id(self)

stage('to the hyro forest',stagedict('S2-E1-N-1-1'),12)
stage('in search of voices',stagedict('S2-E1-N-1-2'),14)
stage('misterious girl',stagedict('S2-E1-N-1-3'),11)
stage('the road back',stagedict('S2-E1-N-1-4'),10)
stage('in the fellwood forest',stagedict('S2-E1-N-1-5'),15)

stage('shadow of the city',stagedict('S2-E1-N-2-1'),8)
stage('enter, musketeers',stagedict('S2-E1-N-2-2'),11,note='red, red')
stage('escaping the pursuers',stagedict('S2-E1-N-2-3'),8,note='blue, blue')
stage('Possessor of the shadow',stagedict('S2-E1-N-2-4'),11,note='blue, blue')
stage('into the city',stagedict('S2-E1-N-2-5'),11,note='yellow, yellow')
stage('behind the shadow',stagedict('S2-E1-N-2-6'),14,note='red, red')
stage('road of the fugitive',stagedict('S2-E1-N-2-7'),6,note='blue, blue')
stage('execution of light, assault of darkness - 1',stagedict('S2-E1-N-2-8'),9,note='yellow, yellow')
stage('execution of light, assault of darkness - 2',stagedict('S2-E1-N-2-9'),10,note='red, yellow')
stage('a hasty escape',stagedict('S2-E1-N-2-10'),7,note='red, yellow')



stage('seeker of truth',stagedict('S2-E1-N-3-1'),12)
stage('vicious rats',stagedict('S2-E1-N-3-2'),14)
stage("ellie's disappearance",stagedict('S2-E1-N-3-3'),15)
stage('a suspicious pursuer',stagedict('S2-E1-N-3-4'),12)
stage('village of ratmen',stagedict('S2-E1-N-3-5'),13)
stage('defending the village',stagedict('S2-E1-N-3-6'),38)
stage('a new companion',stagedict('S2-E1-N-3-7'),19)
stage('echoes in the void',stagedict('S2-E1-N-3-8'),25)
stage("the rat's secret",stagedict('S2-E1-N-3-9'),25)
stage('lord of the sewern',stagedict('S2-E1-N-3-10'),25)

stage('capturing the palace',stagedict('S2-E1-N-4-1'),7)
stage('light of deceit',stagedict('S2-E1-N-4-2'),12)
stage('searching the palace',stagedict('S2-E1-N-4-3'),14)
stage('stream of mana',stagedict('S2-E1-N-4-4'),22)
stage('the false creator',stagedict('S2-E1-N-4-5'),19)

stage('challenge mode',stagedict('S2-E1-C-1','S2-E1-C-2','S2-E1-C-3','S2-E1-C-4'))
stage('goblin battlegorunds',stagedict('S2-E1-C-1'),43)
stage('city of turmoil',stagedict('S2-E1-C-2'))
stage('a plague in the detphs',stagedict('S2-E1-C-3'))
stage('the hidden palace',stagedict('S2-E1-C-4'))


class block(req_base):
    stage=''
    limit=9999999
    def __init__(self,name):
        self.name=name

block('1-chain')
block('2-chain')
block('3-chain')
block('special skill')

class state(req_base):
    stage=False
    limit=1
    def __init__(self,name):
        self.name=name

state('entyre team alive')

class raid(req_base):
    stage={'raid':1}
    limit=1
    name='raid'

class rq_simulator:
    class _ld(list):
        def keys(self,):
            return self
        def __getitem__(self,i):
            if type(i)==str:
                return popularities[i]
            else:
                return list.__getitem__(self,i)
                
    def __init__(self,name,value,chapter):
        self._desc=name
        self.value=value
        self.chapter=chapter
        self.stage=self._ld(by_chapters[chapter])
    @property
    def name(self):
        return '%s at %s'%(self._desc,self.chapter)
        
class requiment(object):
    def __init__(self,name,value=1,*args):
        self.value=value
        try:
            self._rq=unit.all[name]
            return
        except KeyError:
            pass
        try:
            self._rq=block.all[name]
            return
        except KeyError:
            pass
        try:
            self._rq=stage.all[name]
            return
        except KeyError:
            pass
        try:
            self._rq=state.all[name]
            return
        except KeyError:
            pass
        try:
            self._rq=other_stages.all[name]
            return
        except KeyError:
            pass
        if name=='enemies':
            self._rq=rq_simulator(name,value,*args)
            return
        raise ValueError(name)
    @property
    def stage(self):
        return self._rq.stage
    @property
    def name(self):
        return self._rq.name
    def __str__(self):
        rq=self._rq
        if type(rq)==state:
            return 'as %s'%rq.name
        else:
            return '%s: %s times'%(rq.name,self.value)
    def __getitem__(self,key):
        return self._rq.stage[key]
    
def is_challenge_mode(v):
    if type(v)!=str:
        try:
            v=v[0]
        except KeyError:
            v=iter(v).__next__()
    try:
        return v[6]=='C'
    except:
        return False

def is_raid(v):
    return v=='raid'

def is_colosseum(v):
    return v=='colosseum'

def is_normal(v):
    if type(v)!=str:
        try:
            v=v[0]
        except KeyError:
            v=iter(v).__next__()
    try:
        return v[6] in ('N','H')
    except:
        return False
def is_chapter(v,c):
    if type(v)!=str:
        try:
            v=v[0]
        except KeyError:
            v=iter(v).__next__()
    return v.startswith(c)

class reward(object):
    _types={
        'gold':'normal','honor':'normal',
        'iron':'forging-material','dust':'forging-material','shard':'forging-material','crystal':'forging-material',
        'lucky-box':'item','old-weapon-box':'item','honor-box':'item','ring-box':'item'}
    _costs={
        'gold':1/(110/30*15000),'honor':1/(50/9*(600/4)),
        'iron':1/(110/30*2000),'dust':1/240,'shard':1/60,'crystal':1/40,
        'lucky-box':1/5,'old-weapon-box':15000/(110/30*15000),'honor-box':150/(50/9*(600/4)),'ring-box':40/110}
    def __init__(self,name,value):
        self.name=name
        self.value=value
        self.type=self._types[name]
    def __str__(self):
        return '%s: %s'%(self.name,self.value)
    @property
    def as_gem(self):
        return self.value*self._costs[self.name]
class quest(object):
    def __init__(self,*args):
        self.length=length_=False
        self.requiment=requiment_=[]
        self.reward=reward_=[]
        for arg in args:
            if isinstance(arg,length_meta):
                if self.length:
                    raise ValueError('more than 1 length is implemented')
                else:
                    self.length=arg
                continue
            elif isinstance(arg,requiment):
                requiment_.append(arg)
                continue
            elif isinstance(arg,reward):
                reward_.append(arg)
                continue
            else:
                raise TypeError(type(arg).__name__)

        potential=[]
        for value in requiment_:
            if value.stage:
                potential.append(value)
        ln=len(potential)
        if ln==0:
            self.stage='any'
            self.clears=1
        else:
            if ln>1:
                try:
                    for value in potential:
                        if len(value.stage)==1:
                            potential=[value]
                            ln=1
                            raise GetOutException()
                    by_stages=[]
                    for value in potential:
                        by_stages.append(list(value.stage.keys()))
                    for by_stage in by_stages:
                        for i in range(len(by_stage)-1,-1,-1):
                            key=by_stage[i]
                            try:
                                for x in by_stages:
                                    if key not in x:
                                        raise GetOutException()
                            except GetOutException:
                                del by_stage[i]
                    keys=by_stages[0]
                    if len(keys)==1:
                        self.stage=key=keys[0]
                        max_clears=1
                        for value in potential:
                            v=ceil(value.value/value[key])
                            if v>max_clears:
                                max_clears=v
                        self.clears=max_clears
                    else:
                        min_results=''
                        min_clears=99999
                        for key in keys:
                            max_clears=1
                            for value in potential:
                                v=ceil(value.value/value[key])
                                if v>max_clears:
                                    max_clears=v
                            if max_clears<min_clears:
                                min_clears=max_clears
                                min_result=key
                        self.stage=min_result
                        self.clears=min_clears
                        
                except GetOutException:
                    pass
            if ln==1:
                value=potential[0]
                keys=value.stage.keys()
                if len(keys)==1:
                    self.stage=result=next(iter(keys))
                    self.clears=ceil(value.value/value[result])
                else:
                    keys=tuple(keys)
                    totalkills=value.value
                    result=[]
                    for key in keys:
                        result.append(ceil(totalkills/value[key]))
                    manindex=[]
                    clears=99999
                    for i,v in enumerate(result):
                        if v<clears:
                            minindex=[i]
                            clears=v
                        elif v==clears:
                            minindex.append(i)
                    if len(minindex)==1:
                        self.stage=keys[minindex[0]]
                    else:
                        self.stage=tuple(keys[key] for key in minindex)
                    self.clears=clears
        self.all.append(self)
        self.cost=round(self.clears*stage_cost(self.stage),2)
        as_gem=0
        for value in reward_:
            as_gem+=value.as_gem
        self.as_gem=round(as_gem,2)
        self.worthness=as_gem/self.cost

##        if not is_challenge_mode(self.stage) and self.as_gem<=2:
##            self.tier='normal'
##        elif self.as_gem<=6 and self.cost<=1:
##            self.tier='rare'
##        elif self.as_gem<=9:
##            self.tier='epic'
##        elif self.as_gem<=12:
##            self.tier='legendary'
##        else:
##            self.tier='undefined'
    def _str_builder(self):
##        yield 'Tier: '
##        yield self.tier
        yield '<div class=\'quest_box\'>'
        yield '<div class=\'quest_box_i1\'>'
        yield 'Type: '
        yield str(self.length).title()
        yield '<br><br>Minimum runs: '
        yield str(self.clears)
        yield '<ul class=\'quest_box_ul\'>'
        if isinstance(self.stage,str):
            yield '<li>'
            yield self.stage
            yield '</li>'
        else:
            for v in self.stage:
                yield '<li>'
                yield v
                yield '</li>'
        yield '</ul>'
        yield '<br>Worthness: '
        yield str(int(self.worthness*100))+'%'
        yield '<br>'
        yield '</div>'
        yield '<div class=\'quest_box_i2\'>'
        yield 'Requiments: '
        yield '(%s)'%self.cost
        yield '<ul class=\'quest_box_ul\'>'
        for v in self.requiment:
            yield '<li>'
            yield str(v).title()
            yield '</li>'
        yield '</ul>'
        yield '<br>Rewards: '
        yield '(%s)'%self.as_gem
        yield '<ul class=\'quest_box_ul\'>'
        for v in self.reward:
            yield '<li>'
            yield str(v).title()
            yield '</li>'
        yield '</ul>'
        yield '</div>'
        yield '</div>'
##        yield '\nType: '
##        yield str(self.length)
##        yield '\nStage: '
##        yield str(self.stage)
##        yield '\nMinimum runs: '
##        yield str(self.clears)
##        yield '\nWorthness: '
##        yield str(int(self.worthness*100))+'%'
##        yield '\nRequiments:'
##        yield ' (%s)'%self.cost
##        for value in self.requiment:
##            yield '\n    '
##            yield str(value)
##        yield '\nRewards:'
##        yield ' (%s)'%self.as_gem
##        for value in self.reward:
##            yield '\n    '
##            yield str(value)

    def __str__(self):
        return ''.join(self._str_builder())


quests=quest.all=[]

class unit_order():
    def __init__(self,name,boss,number):
        self.number=number
        self.name=name
        self.boss=boss
    def __lt__(self,other):
        if self.boss<other.boss:
            return True
        if self.boss==other.boss:
            if self.number<other.number:
                return True
            if self.number==other.number:
                if self.name>other.name:
                    return True
        return False
    def __le__(self,other):
        if self.boss<other.boss:
            return True
        if self.boss==other.boss:
            if self.number<other.number:
                return True
            if self.number==other.number:
                if self.name>=other.name:
                    return True
        return False
    def __eq__(self,other):
        return self.boss==other.boss and self.number==other.number and self.name==other.name
    def __ne__(self,other):
        return not (self.boss==other.boss and self.number==other.number and self.name==other.name)
    def __ge__(self,other):
        if self.boss>other.boss:
            return True
        if self.boss==other.boss:
            if self.number>other.number:
                return True
            if self.number==other.number:
                if self.name<=other.name:
                    return True
        return False
    def __gt__(self,other):
        if self.boss>other.boss:
            return True
        if self.boss==other.boss:
            if self.number>other.number:
                return True
            if self.number==other.number:
                if self.name<other.name:
                    return True
        return False
    def __str__(self):
        if self.boss:
            return '<tr><td>%s :</td><td>%s (Boss)</td></tr>'%(self.number,self.name)
        else:
            return '<tr><td>%s :</td><td>%s</td></tr>'%(self.number,self.name)
class undefined_number:
    def __lt__(self,other):
        return False
    def __le__(self,other):
        return type(self)==type(other)
    def __eq__(self,other):
        return type(self)==type(other)
    def __ne__(self,other):
        return not (type(self)==type(other))
    def __ge__(self,other):
        return True
    def __gt__(self,other):
       return True
    def __repr__(self):
        return '?'
    __str__=__repr__

undefined_number=undefined_number()

class stageview():
    def __init__(self,stage):
        self.stage=stage
        short=list.__getitem__(stage.stage,0)
        self.units=units=sortedlist(reverse=True)
        global unit
        total=0
        for v in unit.all.values():
            if short in v.stage:
                t=v.stage[short]
                units.append(unit_order(v.name.title(),v.boss,t))
                total+=t
        #stageview.all.append(self)
        self.total=total
        if stage.popularity>4999:
            self.popularity='?'
            units.append(unit_order('undefined',False,undefined_number))
        else:
            self.popularity=stage.popularity
            ppl=stage.popularity-total
            if ppl!=0:
                units.append(unit_order('undefined',False,ppl))
    def _str_builder(self):
        yield '<a class=\'title\'>'
        yield self.stage.name.title()
        yield '</a> ('
        yield list.__getitem__(self.stage.stage,0)
        yield ')</br></br>'
        if self.stage.note:
            yield 'Note: '
            yield self.stage.note
        yield '</br>Units: '
        yield str(self.popularity)
        yield '<table class=\'listing\'><tbody>'
        for v in self.units:
            yield str(v)
        yield '</tbody></table>'
    def __str__(self):
        return ''.join(self._str_builder())

#stageview.all=[]
#for lv in stage.all.values():
#    if len(lv.stage)==1:
#        stageview(lv)

def printall():
    for v in quests:
        print(v)
        print()

class simple_order():
    def __init__(self,name,number):
        self.name=name
        self.number=number
    def __lt__(self,other):
        return self.number<other.number
    def __le__(self,other):
        return self.number<=other.number
    def __eq__(self,other):
        return self.number==other.number
    def __ne__(self,other):
        return self.number!=other.number
    def __ge__(self,other):
        return self.number>=other.number
    def __gt__(self,other):
        return self.number>other.number
    def __str__(self):
        return '<tr><td>%.2f</td><td>%s</td></tr>'%(1/self.number,self.name)

def gemcosts():
    def _builder():
        yield '<table class=\'listing\'><tbody>'
        yield from (str(v) for v in sorted(simple_order(*args) for args in reward._costs.items()))
        yield '</tbody></table>'
    return ''.join(_builder())

##tiernames=[]
##
##class lendict(dict):
##    def __repr__(self):
##        return it_con(('%s:%s'%(k,len(v)) for k,v in self.items()),start='dict{',end='}')
##    __str__=__repr__
##    
##def tierize():
##    re=lendict(tuple((name,list()) for name in ('normal','rare','epic','legendary','undefined')))
##    for value in quest.all:
##        re[value.tier].append(value)
##    return re

stagecut={}
for v in stage.all.values():
    if len(v.stage)==1:
        stagecut[next(iter(v.stage))]=v.name.title()

class imagedata():
    zeropath='questimages\\'
    def __init__(self,name,units):
        self.all.append(self)
        self.name=name
        self.units=units
        for value in unit.all.values():
            if value.name in units:
                value.image=self
        self._data=None
        self._size=None
    @property
    def size(self):
        if self._size is None:
            self._size=PIL.open(self.zeropath+self.name).size
        return self._size
    @property
    def data(self):
        if self._data is None:
            self._data=deconverter(self.zeropath+self.name,16).decode()
        return self._data
    def __bool__(self):
        return True

imagedata.all=[]

imagedata('S2-E1-N-1_goblin_archer.png',{'goblin archer','elite goblin archer'})
imagedata('S2-E1-N-1_goblin_catapult.png',{'goblin catapult','elite goblin catapult'})
imagedata('S2-E1-N-1_goblin_champion.png',{'goblin champion','elite goblin champion'})
imagedata('S2-E1-N-1_goblin_warrior.png',{'goblin warrior','elite goblin warrior'})
imagedata('S2-E1-N-1_mini_ogre.png',{'mini ogre','elite mini ogre'})
imagedata('S2-E1-N-2_shadow_rose_cavalry.png',{'blue shadow rose cavalry','yellow shadow rose cavalry','red shadow rose cavalry'})
imagedata('S2-E1-N-2_shadow_rose_marksman.png',{'blue shadow rose marksman','yellow shadow rose marksman','red shadow rose marksman'})
imagedata('S2-E1-N-2_shadow_rose_charger.png',{'blue shadow rose charger','yellow shadow rose charger','red shadow rose charger'})
imagedata('S2-E1-N-2_heavens_cavalry_soldier.png',{'heavens cavalry soldier'})
imagedata('S2-E1-N-2_heavens_cavalry_sergeant.png',{'heavens cavalry sergeant'})
imagedata('S2-E1-N-2_chaos_shadowdemon.png',{'blue chaos shadowdemon','yellow chaos shadowdemon','red chaos shadowdemon'})
imagedata('S2-E1-N-2_fury_shadowdemon.png',{'blue fury shadowdemon','yellow fury shadowdemon','red fury shadowdemon'})
imagedata('S2-E1-N-3_bigrat.png',{'bigrat'})
imagedata('S2-E1-N-3_bombrat.png',{'bombrat'})
imagedata('S2-E1-N-3_giant_mutarat.png',{'giant mutarat'})
imagedata('S2-E1-N-3_huntrat.png',{'huntrat'})
imagedata('S2-E1-N-3_poisonous_spore.png',{'poisonous spore'})
imagedata('S2-E1-N-3_rotting_mutarat.png',{'rotting mutarat'})
imagedata('S2-E1-N-3_warrat.png',{'warrat'})
imagedata('S2-E1-N-4_kitchen_poltergeist.png',{'kitchen poltergeist'})
imagedata('S2-E1-N-4_library_poltergeist.png',{'library poltergeist'})
imagedata('S2-E1-N-4_mana_mass.png',{'mana mass'})

global chapter_names,challenge_stages,by_chapters,chapter_metas,popularities
challenge_stages=list(x for x in stage.all.values() if len(x.stage)==1 and is_challenge_mode(x.stage))
chapter_names=list(x.name for x in challenge_stages)
chapter_name_titles=list(x.title() for x in chapter_names)
chapter_name_titles.append('Challenge Mode')
chapter_metas=list('S2-E1-N-'+str(x) for x in range(1,len(chapter_names)+1))
chapter_metas.append('S2-E1-C')
class _cl(list):
    def __init__(self,it):
        add=self.append
        for v in it:
            for x in v:
                if x not in self:
                    add(x)
by_chapters={x:_cl(y.stage for y in stage.all.values() if is_chapter(y.stage,x)) for x in chapter_metas}
by_chapters_ns={x:list(set(y for y in stage.all.values() if is_chapter(y.stage,x))) for x in chapter_metas}
popularities={list.__getitem__(y.stage,0):y.popularity for y in stage.all.values() if len(y.stage)==1}
quest_type_metas=list(v.__name__ for v in quest_types)
quest_type_names=list(str.capitalize(v) for v in quest_type_metas)
quest_reward_metas=list(v for v in reward._types.keys())
quest_reward_names=list(str.capitalize(v) for v in quest_reward_metas)

    
def createdocument():
    file=open('quest_statistix.html','w')
    write=file.write
    #start
    write('<!DOCTYPE html><html><style>')
    #general
    write('body{min-height: 100%;max-height: 100%;margin: 0;padding: 0;}')
    write('.view-box{background-color:#a59683;margin: 0 auto;padding: 4px 4px 4px 4px;display: block;height: 100%;vertical-align: middle;width: 1200px;box-sizing: inherit;flex-wrap:wrap;-webkit-box-pack: justify;}')
    write('.view{min-height: calc(100vh - 8px);background-color:#a59683;margin 0;width: 1192px;}')
    write('.view .mimiarea{display: flex;margin: 0px;width: 1192px;}')
    write('.view .mimiarea .mimi{background-color: #ffcc00;border: None;border-top-left-radius: 10px;border-top-right-radius: 10px;color: #3e1727;cursor: pointer;float: right;font: 16px Arial;font: 550 16px Arial;height:34px;text-align: center;text-decoration: none;text-shadow: -1px -1px 1px #ff8d8d14, -1px 1px 1px #ff8d8d14, 1px -1px 1px #ff8d8d14, 1px 1px 1px #ff8d8d14;outline: 0;white-space: nowrap;width: 100%;}')
    write('.view .mimiarea .mimi-box{border: None;border-top-left-radius: 10px;border-top-right-radius: 10px;color: #000000;cursor: pointer;float: right;text-align: center;text-decoration: none;outline: 0;padding: 4px 4px 0px 4px;min-width: 292px;}')
    write('.view .atamaarea{background-color: #fbdf9e;border-bottom-left-radius: 10px;border-bottom-right-radius: 10px;display:flex;margin: 0px;padding: 0px 4px;position:relative;width: 1192px;height: calc(100vh - 46px)}')
    write('.view .atamaarea .atama{padding: 4px 0;position: absolute;width: 100%;}')
    #page1
    write('.index_page{display: flex;}')
    write('.index_page .mimiarea{display: block; float: right; width: 320px;height: calc(100vh - 54px);overflow: auto;}')
    write('.index_page .mimiarea .mimi{color: #3a3a3a;border: solid;border-radius: 8px;border-color: #ab9269;}')
    write('.index_page .mimiarea .mimi-box{width: calc(100% - 8px);margin-bottom: 5px;border-top-right-radius: 5px;border-bottom-right-radius: 5px;border-top-left-radius: 5px;border-bottom-left-radius: 5px;}')
    write('.index_page .atamaarea{width: calc(100% - 340px);height: calc(100vh - 54px);overflow: auto;}')
    write('.index_page .atamaarea .atama{padding: 10px;width: calc(100% - 36px);}')
    #page2
    write('''.stage_page{display: flex;}''')
    write('''.stage_column1{width: 300px;height: calc(100vh - 54px);float: left;overflow: auto;}''')
    write('''.stage_column2{width: calc(100% - 336px);height: calc(100vh - 74px);margin-left: 310px;padding: 10px;position: absolute;overflow: auto;}''')
    write('''.stage_chapter_select{width: 100%;font-size: 16px;border: None;text-align: left;position: relative;padding: 2px 0 2px 25px;height: 26px;margin: 4px 0 0 0;outline: 0;cursor: pointer;border-radius: 8px;border-color: #c79e5b;border-style: solid;border-width: 2px;background-color: #ffde85;overflow: hidden;}''')
    write('''.stage_chapter_select option{font-size: 14px;}''')
    write('''.stage_chapter_stages{width: 100%;}''')
    write('''.stage_button{font-size: 16px;width: 100%;border: None;text-align: left;position: relative;padding: 2px 0 2px 0;height: 26px;margin: 4px 0 0 0;outline: 0;cursor: pointer;border-radius: 8px;border-color: #c79e5b;border-style: solid;border-width: 2px;background-color: #e4d4a8;}''')
    write('''.stage_button_indexing{font-size: 16px;min-width: 30px;max-width: 30px;padding-left:0px;position: absolute;text-align: right;min-height: 18px;max-height: 18px;}''')
    write('''.stage_button_text{line-height: 18px;margin-left: 35px;    min-width: calc(100% - 35px);max-width: calc(100% - 35px);overflow: hidden;min-height: 18px;max-height: 18px;}''')
    write('''.title{font-size:24px;}''')
    write('''.listing{}''')
    write('''.listing td:nth-child(1) {width: 34px; text-align: right;}''')
    write('''.listing td:nth-child(2) {min-width: 96px;}''')
    write('td{padding: 1px;}')
    #page3
    write('.unit_page{display: flex;}')
    write('.unit_column1{width: 300px;height: calc(100vh - 54px);float: left;overflow:auto;}')
    write('.unit_column2whole{width: calc(100% - 316px);height: calc(100vh - 54px);margin-left: 310px;position: absolute;overflow: auto;display: flex;}')
    write('.unit_column2{width: 100%;height: calc(100vh - 74px);padding: 10px;float: left;}')
    write('.unit_column3{text-align: center;width: 500px;height: calc(100vh - 114px);margin-left: calc(100% - 500px);position: absolute;padding-top: 40px;}')
    write('.unit_select_line{width:100%;margin: 4px 0 0 0;}')
    write('.unit_select_text{float: left;width: 77px;padding: 4px 3px 4px 0px;text-align: right;}')
    write('.unit_select{width: calc(100% - 80px);font-size: 16px;border: None;text-align: left;position: relative;padding: 2px 0px 2px 5px;height: 26px;outline: 0;cursor: pointer;border-radius: 8px;border-color: #c79e5b;border-style: solid;border-width: 2px;background-color: #ffde85;overflow: hidden;}')
    write('.unit_entry{width: calc(100% - 90px);font-size: 16px;border: None;text-align: left;position: relative;padding: 0px 0px 0px 6px;height: 22px;outline: 0;border-radius: 8px;border-color: #c79e5b;border-style: solid;border-width: 2px;background-color: #fff1c5;overflow: hidden;}')
    write('.unit_choises{margin: 4px 0 0 0;background-color:#efd8a2;width: calc(100% - 6px);height: calc(100vh - 162px);min-height: 90px;border-radius: 10px;border-width: 4px;padding: 3px 3px 3px 3px;border-color: #c79e5b;border-style: solid none solid none;overflow: auto;}')
    write('.unit_button{width: 100%;border: None;text-align: left;position: relative;padding: 2px 10px 2px 10px;height: 26px;outline: 0;cursor: pointer;border-radius: 8px;border-color: #ca4e62;border-style: none solid none solid;border-width: 2px;background-color: #ffefc2;font-size: 16px;margin: 0 0 4px 0;}')
    write('::-webkit-scrollbar{width: 8px;height: 8px;}')
    write('::-webkit-scrollbar-track{margin: 3px 0 3px 0;background-color: #00000000;}')
    write('::-webkit-scrollbar-thumb{border-radius: 8px;background-color: #d0bb83;}')
    write('::-webkit-scrollbar-corner{background-color: #00000000;}')
    #page4
    write('.quest_page{display: flex;margin: 0 auto 0 auto;width: 1200px;}')
    write('.quest_column1{width: 300px;height: calc(100vh - 54px);float: left;overflow: auto;}')
    write('.quest_column2{width: 900px;height: calc(100vh - 74px);margin: 10px 10px 10px 10px;position: relative;overflow: auto;}')
    write('.quest_so_line{width:100%;margin: 4px 0 0 0;display: flex;}')
    write('.quest_so_t_p1{width: 70%;text-align: center;float: left;disply: block;text-shadow:   -1px  0px 1px rgba(255, 134, 134, 0.8),   +1px  0px 1px rgba(255, 134, 134, 0.8),0px -1px 1px rgba(255, 134, 134, 0.8),0px +1px 1px rgba(255, 134, 134, 0.8);}')
    write('.quest_so_t_p2{width:30%;text-align: center;position: relative;dispaly: block;text-shadow:   -1px  0px 1px rgba(255, 134, 134, 0.8),   +1px  0px 1px rgba(255, 134, 134, 0.8),0px -1px 1px rgba(255, 134, 134, 0.8),0px +1px 1px rgba(255, 134, 134, 0.8);}')
    write('.quest_so_t_full{width: 100%;text-align: center;dispaly: block;text-shadow:   -1px  0px 1px rgba(255, 134, 134, 0.8),   +1px  0px 1px rgba(255, 134, 134, 0.8),0px -1px 1px rgba(255, 134, 134, 0.8),0px +1px 1px rgba(255, 134, 134, 0.8);}')
    write('.quest_so_space{width:100%;height: 8px;}')
    write('.quest_entry_p1{width: calc(70% - 10px);font-size: 16px;border: None;text-align: left;float: left;position: relative;padding: 0px 0px 0px 6px;height: 22px;outline: 0;border-radius: 8px;border-color: #c79e5b;border-style: solid;border-width: 2px;background-color: #fff1c5;overflow: hidden;margin-right:10px;}')
    write('.quest_entry_p2{width: calc(30% - 0px);font-size: 16px;border: None;text-align: left;position: relative;padding: 0px 0px 0px 6px;height: 22px;outline: 0;border-radius: 8px;border-color: #c79e5b;border-style: solid;border-width: 2px;background-color: #fff1c5;overflow: hidden;}')
    write('.quest_select{width: 100%;font-size: 16px;border: None;text-align: left;position: relative;padding: 2px 0px 2px 5px;height: 26px;outline: 0;cursor: pointer;border-radius: 8px;border-color: #c79e5b;border-style: solid;border-width: 2px;background-color: #ffde85;overflow: hidden;}')
    write('.quest_box{min-height: 140px;width: calc(100% - 18px);border-radius: 8px;border-color: #eac588;border-style: solid;border-width: 3px;background-color: #fff5eb;margin-bottom: 4px;padding: 4px 6px 4px 6px;display: flex;}')
    write('.quest_box_i1{position: relative;width:300px;}')
    write('.quest_box_i2{position: relative;width: calc(100% - 300px);}')
    write('.quest_box_ul{list-style-type: circle;margin-top: 0px;margin-bottom: 0px;}')
    #general
    write('</style><body><div class="view-box"><div id="view" class="view"></div></div></body>')
    #general fucntion
    write('<script>function $(v){return document.getElementById(v);}')
    #general
    write('''class clickdater_default{constructor(){}update(){}}class updater{constructor(){var self=this;self._d={};self.default=new clickdater_default();self.to_update=self.default;}append(index,obj){var self=this;if (obj=='None'){obj=self.default;}self._d[index]=obj;} swich(index){var self=this;index=index.toString();if (Object.keys(self._d).indexOf(index)>-1){self.to_update=self._d[index];}else{self.to_update=self.default;}}update(){var self=this;self.to_update.update();}}var entryupdater=new updater();setInterval(function() {entryupdater.update()}, 200);''')
    write('''var starting_page=3;''')
    write('all_chooserbox=[];')
    write('class chooserbox_configured{get passive_color(){return \'#bda88d\';}get active_color(){return \'#f5e6af\';}constructor(id,titles,texts,selected){var self=this;self.index=all_chooserbox.length;all_chooserbox.push(self);self.id=id;self.titles=titles;self.texts=texts;self.selected=selected;var index=0;var final="<div class=\'mimiarea\'>";while (index<selected){final+="<div class=\'mimi-box\' id=\'"+self.id+\'_m_\'+index.toString()+"_box\'><button id=\'"+self.id+\'_m_\'+index.toString()+"\' style=\'background-color: "+self.passive_color+"; height: 30px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;\' class=\'mimi\' onclick=\'all_chooserbox["+self.index+"].onclick("+index+")\'>"+titles[index]+"</button></div>";index+=1;}final+="<div class=\'mimi-box\' id=\'"+self.id+\'_m_\'+index.toString()+"_box\' style=\'background-color: #fbdf9e;\'><button id=\'"+self.id+\'_m_\'+index.toString()+"\' style=\'background-color: "+self.active_color+";\' class=\'mimi\' onclick=\'all_chooserbox["+self.index+"].onclick("+index+")\'>"+titles[index]+"</button></div>";index+=1;while (index<titles.length){final+="<div class=\'mimi-box\' id=\'"+self.id+\'_m_\'+index.toString()+"_box\'><button id=\'"+self.id+\'_m_\'+index.toString()+"\' style=\'background-color: "+self.passive_color+"; height: 30px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;\' class=\'mimi\' onclick=\'all_chooserbox["+self.index+"].onclick("+index+")\'>"+titles[index]+"</button></div>";index+=1;}final+="</div><div class=\'atamaarea\'>";index=0;while (index<selected){final+="<div id=\'"+self.id+\'_a_\'+index.toString()+"\' style=\'display: none;\' class=\'atama\' onclick=\'\'>"+texts[index]+"</div>";index+=1;}final+="<div id=\'"+self.id+\'_a_\'+index.toString()+"\' style=\'display: block;\'class=\'atama\' onclick=\'\'>"+texts[index]+"</div>";index+=1;while (index<titles.length){final+="<div id=\'"+self.id+\'_a_\'+index.toString()+"\' style=\'display: none;\' class=\'atama\' >"+texts[index]+"</div>";index+=1;}final+="</div>";var line=$(id);line.innerHTML=final;}onclick(selected){var self=this;if (selected==self.selected){return;}entryupdater.swich(selected);var line=$(self.id+\'_m_\'+self.selected.toString());line.style.backgroundColor=self.passive_color;line.style.borderBottomRightRadius=\'10px\';line.style.borderBottomLeftRadius=\'10px\';line.style.height=\'30px\';var line=$(self.id+\'_m_\'+self.selected.toString()+\'_box\');line.style.backgroundColor=\'inherit\';var line=$(self.id+\'_a_\'+self.selected.toString());line.style.display=\'none\';self.selected=selected;var line=$(self.id+\'_m_\'+self.selected.toString());line.style.backgroundColor=self.active_color;line.style.borderBottomRightRadius=\'0px\';line.style.borderBottomLeftRadius=\'0px\';line.style.height=\'34px\';var line=$(self.id+\'_m_\'+self.selected.toString()+\'_box\');line.style.backgroundColor=\'#fbdf9e\';var line=$(self.id+\'_a_\'+self.selected.toString());line.style.display=\'block\';}}')
    write('''new chooserbox_configured("view",["Index","Stages",'Units','Quests'],["<div class='index_page' id='index_page'></div>","<div class='stages_page' id='stage_page'></div>","<div class='unit_page' id='unit_page'></div>","<div class='quest_page' id='quest_page'>"],starting_page);''')
    #page1
    write('class chooserbox{get passive_color(){return \'#f6ffc6\';}get active_color(){return \'#67f156\';}constructor(id,titles,texts,selected){var self=this;self.index=all_chooserbox.length;all_chooserbox.push(self);self.id=id;self.titles=titles;self.texts=texts;self.selected=selected;var index=0;var final="<div class=\'mimiarea\'>";while (index<selected){final+="<div class=\'mimi-box\' id=\'"+self.id+\'_m_\'+index.toString()+"_box\'><button id=\'"+self.id+\'_m_\'+index.toString()+"\' style=\'background-color: "+self.passive_color+";\' class=\'mimi\' onclick=\'all_chooserbox["+self.index+"].onclick("+index+")\'>"+titles[index]+"</button></div>";index+=1;}final+="<div class=\'mimi-box\' id=\'"+self.id+\'_m_\'+index.toString()+"_box\'><button id=\'"+self.id+\'_m_\'+index.toString()+"\' style=\'background-color: "+self.active_color+";\' class=\'mimi\' onclick=\'all_chooserbox["+self.index+"].onclick("+index+")\'>"+titles[index]+"</button></div>";index+=1;while (index<titles.length){final+="<div class=\'mimi-box\' id=\'"+self.id+\'_m_\'+index.toString()+"_box\'><button id=\'"+self.id+\'_m_\'+index.toString()+"\' style=\'background-color: "+self.passive_color+";\' class=\'mimi\' onclick=\'all_chooserbox["+self.index+"].onclick("+index+")\'>"+titles[index]+"</button></div>";index+=1;}final+="</div><div class=\'atamaarea\'>";index=0;while (index<selected){final+="<div id=\'"+self.id+\'_a_\'+index.toString()+"\' style=\'display: none;\' class=\'atama\' onclick=\'\'>"+texts[index]+"</div>";index+=1;}final+="<div id=\'"+self.id+\'_a_\'+index.toString()+"\' style=\'display: block;\'class=\'atama\' onclick=\'\'>"+texts[index]+"</div>";index+=1;while (index<titles.length){final+="<div id=\'"+self.id+\'_a_\'+index.toString()+"\' style=\'display: none;\' class=\'atama\' >"+texts[index]+"</div>";index+=1;}final+="</div>";var line=$(id);line.innerHTML=final;}onclick(selected){var self=this;if (selected==self.selected){return;}var line=$(self.id+\'_m_\'+self.selected.toString());line.style.backgroundColor=self.passive_color;var line=$(self.id+\'_a_\'+self.selected.toString());line.style.display=\'none\';self.selected=selected;var line=$(self.id+\'_m_\'+self.selected.toString());line.style.backgroundColor=self.active_color;var line=$(self.id+\'_a_\'+self.selected.toString());line.style.display=\'block\';}}')
    write('''new chooserbox("index_page",["About","Buglist",'Rewards'],["''')
    write('''<a class='title'>Matsu's quest-thingy</a></br></br></br>Thanks for help for:<ul><li>Ubers for C3 quests</li><li>Shiki for raid/colo quests</li><li>BiBi/BrainLord for C4 quests</li><li>Narwhal for being Kitty Cat</li></ul></br></br>If u find any missing quests, please report them, so I can add them.",''')
    write('''"<ul><li>Elite archer goblins are not counted from the catapult boss wave at C1</li></ul>",''')
    write('''"Every quest's reward is estimated, by how much gem it should cost to buy enough meat/keys etc.. to farm them out or buy them from farmable resources. The table down contains, the estimated outfarmable amount by spending 1 gem.</br></br>''')
    write(gemcosts())
    write('''"],0);''')
    #page2
    write('var line=$("stage_page");line.innerHTML="<div class=\'stage_column1\'><select name=\'chapter\' class=\'stage_chapter_select\' id=\'stage_select\' onchange=\'stage_select_modify()\'></select><div class=\'stage_chapter_stages\' id=\'stage_choises\'></div></div><div class=\'stage_column2\' id=\'stage_details\'></div>";')
    write('class stage_object{constructor(arg0,arg1){var self=this;self.name=arg0;self.text=arg1;}}')
    write('var chapters={};')
    write('class chapter_controler{get choises_id(){return \'stage_choises\';}get details_id(){return \'stage_details\';}get active_color(){return \'#b3d4a1\';}get passive_color(){return \'#e4d4a8\';}get button_example(){return "<button class=\'stage_button\' id=\'stage_button_%s\' onclick=\'selected_chapter.onclick(%s)\'><div class=\'stage_button_indexing\'>%s</div><div class=\'stage_button_text\'>%s</div></button>";}constructor(id,name){var self=this;self._data=[];self._selected=0;self._id=id;self.name=name;chapters[id]=self;}append(arg0,arg1){var self=this;self._data.push(new stage_object(arg0,arg1));}render(){var self=this;var final=\'\';var index=0;var ln=self._data.length;while (index<ln){var value=self._data[index];var part=self.button_example;part=part.replace(\'%s\',index.toString());part=part.replace(\'%s\',index.toString());index+=1;part=part.replace(\'%s\',index.toString());part=part.replace(\'%s\',value.name);final+=part;}var line=$(\'stage_choises\');line.innerHTML=final;var line=$(\'stage_button_\'+self._selected.toString());line.style.backgroundColor=self.active_color;var line=$(\'stage_details\');line.innerHTML=self._data[self._selected].text;var index=0;while(index<ln){var value=self._data[index];var l_ln=value.name.length;if (l_ln>34){var line=$(\'stage_button_\'+index.toString());var height=Math.floor((34/l_ln)*16);line.style.fontSize=height.toString()+\'px\';}index+=1;}}onclick(v){var self=this;if (v==self._selected){return;}var line=$(\'stage_button_\'+self._selected.toString());line.style.backgroundColor=self.passive_color;self._selected=v;var line=$(\'stage_button_\'+self._selected.toString());line.style.backgroundColor=self.active_color;var line=$(\'stage_details\');line.innerHTML=self._data[v].text;}}')
    for i,c,v in zip(count(1),chapter_names,by_chapters.keys()):
        write('var act=new chapter_controler(%s,"%s");'%(i,c.title()))
        for v in by_chapters_ns[v]:
            write('act.append("%s","%s");'%(v.name.title(),stageview(v)))
    write('var act=new chapter_controler("X","Challenge Mode");')
    for v in challenge_stages:
        write('act.append("%s","%s");'%(v.name.title(),stageview(v)))
    write("function stage_select_modify(){var line=$('stage_select');selected_chapter=chapters[line.value];selected_chapter.render();}")
    write('var index=0;var keys=Object.keys(chapters);var ln=keys.length;var value=chapters[keys[index]];var selected_chapter=value;var part=\'<option value="%s" selected="selected">%s</option>\';part=part.replace(\'%s\',value._id.toString());part=part.replace(\'%s\',value.name);var final=part;index=1;while (index<ln){var value=chapters[keys[index]];var part=\'<option value="%s">%s</option>\';part=part.replace(\'%s\',value._id.toString());part=part.replace(\'%s\',value.name);index+=1;final+=part;}line=$(\'stage_select\');line.innerHTML=final;selected_chapter.render();')
    #page3
    write('''var line=$("unit_page");line.innerHTML="<div class='unit_column1'><div class='unit_select_line'><div class='unit_select_text'>Type</div><select name='unit_type' class='unit_select' id='unit_type_select' onchange='unitupdater.update()'></select></div><div class='unit_select_line'><div class='unit_select_text'>Appearance</div><select name='unit_chapters' class='unit_select' id='unit_chapter_select' onchange='unitupdater.update()'></select></div><div class='unit_select_line'><div class='unit_select_text'>Search</div><input type=text class='unit_entry' id='unit_meta_input' /></div><div class='unit_choises' id='unit_choises'></div></div><div class='unit_column2whole'><div class='unit_column2' id='unit_details'></div><div class='unit_column3' id='unit_image'></div></div>";''')
    write('var images={};class image{constructor(name,data,size){var self=this;self.name=name;self.data=data;self.size=size;images[name]=self;}}')
    for image in imagedata.all:
        write('new image("')
        write(image.name)
        write('","')
        write(image.data)
        write('",')
        write('[%s,%s]'%image.size)
        write(');')
    write('var all_unit=[];')
    write('class unitupdater_object{get entry_passive_color(){return \'#fff1c5\';}get entry_active_color(){return \'#d6ffc5\';}get entry_negative_color(){return \'#ff9a9a\';}get default_value(){return -1;}get default_value_c(){return \'Any\';}get button_active_color(){return \'#cafdb1\';}get button_passive_color(){return \'#ffefc2\';}get units(){return all_unit;}constructor(chapter_names,chapter_metas){var self=this;self.type_indexes=[-1,0,1];self.types=[self.default_value_c,\'Normal\',\'Boss\'];self.chapter_indexes=[-1];self.chapter_metas=[\'None\'];self.chapters=[self.default_value_c];var index=0;var ln=chapter_names.length;while (index<ln){self.chapters.push(chapter_names[index]);self.chapter_indexes.push(index);self.chapter_metas.push(chapter_metas[index]);index+=1;}var final=\'\';index=0;ln=self.types.length;while (index<ln){var part=\'<option value="%s">%s</option>\';part=part.replace(\'%s\',self.type_indexes[index].toString());part=part.replace(\'%s\',self.types[index]);self.types[index]=self.types[index].toLowerCase();index+=1;final+=part;}var line=$(\'unit_type_select\');line.innerHTML=final;var final=\'\';index=0;ln=self.chapters.length;while (index<ln){var part=\'<option value="%s">%s</option>\';part=part.replace(\'%s\',self.chapter_indexes[index].toString());part=part.replace(\'%s\',self.chapters[index]);self.chapters[index]=self.chapters[index].toLowerCase();index+=1;final+=part;}var line=$(\'unit_chapter_select\');line.innerHTML=final;self.selected=0;var final=\'\';index=0;ln=self.units.length;while (index<ln){var value=self.units[index];final+=value.button;index+=1;}self._default_rendering=final;var line=$(\'unit_choises\');line.innerHTML=final;self._last_type=self.default_value;self._last_chapter=self.default_value;self._last_search=\'\';self._after_type=self.units.slice();self._after_chapter=self.units.slice();self._after_search=self.units.slice();self._last_clicked=0;line=$(\'unit_button_0\');line.style.backgroundColor=self.button_active_color;self.units[0].render();entryupdater.append(2,self);}update(){var self=this;var count=0;var line=$(\'unit_type_select\');var new_type=parseInt(line.value);if (self._last_type!=new_type){count+=1;if (new_type==self.default_value){self._after_type=self.units.slice();}else{var index=0;var ori=self.units;var new_=[];var ln=ori.length;while (index<ln){var value=ori[index];index+=1;if (value.boss==new_type){new_.push(value);}}self._after_type=new_;}self._last_type=new_type;}var line=$(\'unit_chapter_select\');var new_chapter=parseInt(line.value);if (self._last_chapter!=new_chapter || count>0){count+=1;if (new_chapter==self.default_value){self._after_chapter=self._after_type.slice();}else{var index=0;var ori=self._after_type;var new_=[];var ln=ori.length;var converted=self.chapter_metas[self.chapter_indexes.indexOf(new_chapter)];while (index<ln){var value=ori[index];index+=1;if (value.appearance.indexOf(converted)!=-1){new_.push(value);}}self._after_chapter=new_;}self._last_chapter=new_chapter;}var line=$(\'unit_meta_input\');var new_search=line.value.toLowerCase();if (self._last_search!=new_search || count>0){count+=1;if (new_search==\'\'){self._after_search=self._after_chapter.slice();line.style.backgroundColor=self.entry_passive_color;}else{if (count==1 && new_search.includes(self._last_search)){var index=0;var ori=self._after_search;var new_=[];var ln=ori.length;while (index<ln){var value=ori[index];index+=1;if (value.meta.includes(new_search)){new_.push(value);}}}else{var index=0;var ori=self._after_chapter;var new_=[];var ln=ori.length;while (index<ln){var value=ori[index];index+=1;if (value.meta.includes(new_search)){new_.push(value);}}}self._after_search=new_;}self._last_search=new_search;}if (count==0){return;}if (new_type==self.default_value && new_chapter==self.default_value && new_search==\'\'){var line=$(\'unit_choises\');line.innerHTML=self._default_rendering;var index=0;var ln=self.units.length;var to_render=self.units;while (index<ln){if (to_render[index].id==self._last_clicked){break;}index+=1;}if (index==ln){self._last_clicked=0;}line=$(\'unit_button_\'+self._last_clicked.toString());line.style.backgroundColor=self.button_active_color;self.units[self._last_clicked].render();return;}var ln=self._after_search.length;if (ln>0){var final=\'\';var index=0;var to_render=self._after_search;while (index<ln){var value=to_render[index];var part=value.button;final+=part;index+=1;}var line=$(\'unit_choises\');line.innerHTML=final;var index=0;var to_render=self._after_search;while (index<ln){if (to_render[index].id==self._last_clicked){break;}index+=1;}if (index==ln){self._last_clicked=to_render[0].id;}line=$(\'unit_button_\'+self._last_clicked.toString());line.style.backgroundColor=self.button_active_color;self.units[self._last_clicked].render();if (new_search!=\'\'){var line=$(\'unit_meta_input\');line.style.backgroundColor=self.entry_active_color;}return;}if (self._after_chapter.length>0){var line=$(\'unit_meta_input\');line.style.backgroundColor=self.entry_negative_color;}var line=$(\'unit_choises\');line.innerHTML=\'\';var line=$(\'unit_details\');line.innerHTML=\'\';}onclick(index){var self=this;if (index==self._last_clicked){return;}var line=$(\'unit_button_\'+self._last_clicked.toString());line.style.backgroundColor=self.button_passive_color;self._last_clicked=index;line=$(\'unit_button_\'+index.toString());line.style.backgroundColor=self.button_active_color;self.units[index].render();}}')
    write('class unit_object{constructor(arg0,arg1,arg2,arg3,arg4,arg5){var self=this;self.name=arg0;self.text=arg1;self.meta=arg2;self.boss=arg3;self.appearance=arg4;self.image=arg5;self.id=all_unit.length;all_unit.push(self);if (self.name.length>32){self.height=Math.floor((32/self.name.length)*16);}else{self.height=16;}var part="<button class=\'unit_button\' style=\'font-size:%spx\' id=\'unit_button_%s\' onclick=\'unitupdater.onclick(%s)\'>%s</button>";part=part.replace(\'%s\',self.height);part=part.replace(\'%s\',self.id.toString());part=part.replace(\'%s\',self.id.toString());part=part.replace(\'%s\',self.name);self.button=part;}render(){var self=this;var line=$(\'unit_details\');line.innerHTML=self.text;var line=$(\'unit_image\');if (self.image!=\'None\'){var img=images[self.image];line.innerHTML=\'<img src="\'+img.data+\'" width="\'+(img.size[0]*2).toString()+\'px" height="\'+(img.size[1]*2).toString()+\'px" >\';}else{line.innerHTML=\'\';}}}')
    for v in sorted(unit.all.values(),key=lambda v:v.name):
        write('new unit_object(\'')
        write(v.name.title())
        write('\',"')
        write(str(unitview(v)))
        write('",\'')
        write(v.name)
        write('\',')
        write(str(int(v.boss)))
        write(',')
        write(str(v.chaptermetas))
        write(',\'')
        if v.image:
            write(v.image.name)
        else:
            write('None')
        write('\');')
    write('var unitupdater=new unitupdater_object(')
    write(str(chapter_name_titles))
    write(',')
    write(str(chapter_metas))
    write(');')
    #page4
    write('''var line=$("quest_page");line.innerHTML="<div class='quest_column1'><div class='quest_so_line'><div class='quest_so_t_full'>Quest Type</div></div><div class='quest_so_line'><select name='quest_type' class='quest_select' id='quest_type_select' onchange='questupdater.update()'></select></div><div class='quest_so_space'></div><div class='quest_so_line'><div class='quest_so_t_p1'>Requiment</div><div class='quest_so_t_p2'>Times</div></div><div class='quest_so_line'><input class='quest_entry_p1' id='quest_input0n'></input><input class='quest_entry_p2' id='quest_input0a'></input></div><div class='quest_so_line'><input class='quest_entry_p1' id='quest_input1n'></input><input class='quest_entry_p2' id='quest_input1a'></input></div><div class='quest_so_space'></div><div class='quest_so_line'><div class='quest_so_t_full'>Rewards</div></div><div class='quest_so_line'><select name='quest_reward0' class='quest_select' id='quest_reward_select_0' onchange='questupdater.update()'></select></div><div class='quest_so_line'><select name='quest_reward1' class='quest_select' id='quest_reward_select_1' onchange='questupdater.update()'></select></div><div class='quest_so_line'><select name='quest_reward2' class='quest_select' id='quest_reward_select_2' onchange='questupdater.update()'></select></div><div class='quest_so_line'><select name='quest_reward3' class='quest_select' id='quest_reward_select_3' onchange='questupdater.update()'></select></div><div class='quest_so_line'><select name='quest_reward4' class='quest_select' id='quest_reward_select_4' onchange='questupdater.update()'></select></div><div class='quest_so_line'><select name='quest_reward5' class='quest_select' id='quest_reward_select_5' onchange='questupdater.update()'></select></div></div><div class='quest_column2' id='quest_listing'></div>";''')
    write('''var numbers=['0','1','2','3','4','5','6','7','8','9'];''')
    write('''function tonumeric(v){var ln=v.length;if (ln==0){return -1;}var index=0;while (index<ln){var c=numbers.indexOf(v[index]);if (c==-1){return -2;}index+=1;}return parseInt(v);}''')
    write('''function issame(a,b){var lna=a.length;var lnb=b.length;if (lna!=lnb){return 'False';}var index=0;while (index<lna){if (a[index]!=b[index]){return 'False';}index+=1;}return 'True';}''')
    write('''function all_negative(a){var ln=a.length;var index=0;while (index<ln){if (a[index]>=0){return 'False';}index+=1;}return 'True';}''')
    write('''var all_quests=[];''')
    write('''class questupdater_object{get entry_passive_color(){return '#fff1c5';}get entry_active_color(){return '#d6ffc5';}get entry_negative_color(){return '#ff9a9a';}get default_value(){return -1;}get default_value_t(){return 'Any';}get default_value_r(){return 'None';}get quests(){return all_quests;}constructor(quest_type_names,quest_type_metas,quest_reward_names,quest_reward_metas){var self=this;self.type_indexes=[-1];self.type_metas=['None'];self.type_names=[self.default_value_t];self.reward_indexes=[-1];self.reward_metas=['None'];self.reward_names=[self.default_value_r];var index=0;var ln=quest_type_names.length;while (index<ln){self.type_names.push(quest_type_names[index]);self.type_indexes.push(index);self.type_metas.push(quest_type_metas[index]);index+=1;}var index=0;var ln=quest_reward_names.length;while (index<ln){self.reward_names.push(quest_reward_names[index]);self.reward_indexes.push(index);self.reward_metas.push(quest_reward_metas[index]);index+=1;}var final='';index=0;ln=self.type_names.length;while (index<ln){var part='<option value="%s">%s</option>';part=part.replace('%s',self.type_indexes[index].toString());part=part.replace('%s',self.type_names[index]);index+=1;final+=part;}var line=$('quest_type_select');line.innerHTML=final;var final='';self.type_selected=-1;index=0;ln=self.reward_names.length;while (index<ln){var part='<option value="%s">%s</option>';part=part.replace('%s',self.reward_indexes[index].toString());part=part.replace('%s',self.reward_names[index]);index+=1;final+=part;}self.reward_selected=[];index=0;ln=6;while (index<ln){var line=$('quest_reward_select_'+index.toString());line.innerHTML=final;index+=1;self.reward_selected.push(-1);}var final='';index=0;ln=self.quests.length;while (index<ln){var value=self.quests[index];final+=value.visual;index+=1;}self._default_rendering=final;var line=$('quest_listing');line.innerHTML=final;self.search_0_name='';self.search_1_name='';self.search_0_amount=-1;self.search_1_amount=-1;self._after_type=self.quests.slice();self._after_reward=self.quests.slice();self._after_search=self.quests.slice();self._after_order=self.quests.slice();entryupdater.append(3,self);}update(){var self=this;var count=0;var line=$('quest_type_select');var new_type=parseInt(line.value);if (self.type_selected!=new_type){count+=1;if (new_type==self.default_value){self._after_type=self.quests.slice();}else{var index=0;var ori=self.quests;var new_=[];var ln=ori.length;while (index<ln){var value=ori[index];index+=1;if (value.type==new_type){new_.push(value);}}self._after_type=new_;}self.type_selected=new_type;}var new_rewards=[];var index=0;var filtered_rewards=[];while (index<6){var line=$('quest_reward_select_'+index.toString());new_rewards.push(parseInt(line.value));index+=1;}if (issame(self.reward_selected,new_rewards)=='False' || count>0){count+=1;if (all_negative(new_rewards)=='True'){self._after_reward=self._after_type;}else{var index=0;while(index<6){var value=new_rewards[index];if (value>=0){filtered_rewards.push(value);}index+=1;}var index=0;var ori=self.quests;var new_=[];var ln=ori.length;var index2,push,subvalue;var ln2=filtered_rewards.length;while (index<ln){var value=ori[index];index+=1;index2=0;push=1;while (index2<ln2){subvalue=filtered_rewards[index2];index2+=1;if (value.reward_types.indexOf(subvalue)==-1){push=0;break;}}if (push){new_.push(value);}}self._after_reward=new_;}self.reward_selected=new_rewards;}else{var index=0;while(index<6){var value=new_rewards[index];if (value>=0){filtered_rewards.push(value);}index+=1;}}var line=$('quest_input0n');var search_0_name=line.value.toLowerCase();var line=$('quest_input0a');var search_0_amount=tonumeric(line.value);if (search_0_amount==-2){line.value='';search_0_amount=-1;}var line=$('quest_input1n');var search_1_name=line.value.toLowerCase();var line=$('quest_input1a');var search_1_amount=tonumeric(line.value);if (search_1_amount==-2){line.value='';search_1_amount=-1;}if (self.search_0_name!=search_0_name || self.search_0_amount!=search_0_amount || self.search_1_name!=search_1_name || self.search_1_amount!=search_1_amount || count>0){count+=1;var ac=0;var new_=0;var ori=0;if (search_0_name=='' && search_0_amount==-1){}else{ac=1;var index=0;var ori=self._after_reward;var new_=[];var ln=ori.length;if (search_0_amount!=-1){while (index<ln){var value=ori[index];var index2=0;var ln2=value.requiments.length;while (index2<ln2){var req=value.requiments[index2];if (req.name.includes(search_0_name) && req.amount==search_0_amount){new_.push(value);break;}index2+=1;}index+=1;}}else{while (index<ln){var value=ori[index];var index2=0;var ln2=value.requiments.length;while (index2<ln2){var req=value.requiments[index2];if (req.name.includes(search_0_name)){new_.push(value);break;}index2+=1;}index+=1;}}self._after_search=new_;}if (search_1_name=='' && search_1_amount==-1){}else{debugger;if (ac==0){var ori=self._after_reward;}else{var ori=new_;}ac=2;var index=0;var new_=[];var ln=ori.length;if (search_1_amount!=-1){while (index<ln){var value=ori[index];var index2=0;var ln2=value.requiments.length;while (index2<ln2){var req=value.requiments[index2];if (req.name.includes(search_1_name) && req.amount==search_1_amount){new_.push(value);break;}index2+=1;}index+=1;}}else{while (index<ln){var value=ori[index];var index2=0;var ln2=value.requiments.length;while (index2<ln2){var req=value.requiments[index2];if (req.name.includes(search_1_name)){new_.push(value);break;}index2+=1;}index+=1;}}self._after_search=new_;}if (ac==0){self._after_search=self._after_reward;}self.search_0_name=search_0_name;self.search_0_amount=search_0_amount;self.search_1_name=search_1_name;self.search_1_amount=search_1_amount;}else{self._after_search=self._after_reward;}if (count==0){return;}if (new_type==self.default_value && all_negative(new_rewards)=='True' && ''==search_0_name && ''==search_1_name){var line=$('quest_listing');line.innerHTML=self._default_rendering;return;}var ln=self._after_search.length;if (ln>0){var ol=filtered_rewards.length;if (ol==0){self._after_order=self._after_search;}else{var to_order=self._after_search;var index=ol-1;while(index>-1){var to_sort=filtered_rewards[index];var __pyc__1=ln-1;while (__pyc__1>-1){var __pyc__2=0;while (__pyc__2<__pyc__1){var __pyc__3=to_order[__pyc__2];var __pyc__4=to_order[__pyc__2+1];if (__pyc__3.reward_values[__pyc__3.reward_types.indexOf(to_sort)]<__pyc__4.reward_values[__pyc__4.reward_types.indexOf(to_sort)]){to_order[__pyc__2]=__pyc__4;to_order[__pyc__2+1]=__pyc__3;}__pyc__2+=1;}__pyc__1-=1;}index-=1;}self._after_order=to_order;}var final='';var index=0;var to_render=self._after_order;while (index<ln){var value=to_render[index];var part=value.visual;final+=part;index+=1;}var line=$('quest_listing');line.innerHTML=final;return;}var line=$('quest_listing');line.innerHTML='';}}''')
    write('''class req_object{constructor(name,amount){var self=this;self.amount=amount;self.name=name;}}''')
    write('''class quest_object{constructor(type_,reqs,rt,rv,visual){var self=this;all_quests.push(self);self.type=type_;self.requiments=reqs;self.reward_types=rt;self.reward_values=rv;self.visual=visual;}}''')
    for v in quests:
        write('new quest_object(')
        write(str(quest_types.index(v.length)))
        write(',[')
        for s in v.requiment:
            write('new req_object("')
            write(s._rq.name)
            write('",')
            write(str(s.value))
            write('),')
        write('],[')
        for s in v.reward:
            write(str(quest_reward_metas.index(s.name)))
            write(',')
        write('],[')
        for s in v.reward:
            write(str(s.value))
            write(',')
        write('],"')
        write(str(v))
        write('");')
    write('''var questupdater=new questupdater_object(''')
    for v in (quest_type_names,quest_type_metas,quest_reward_names,quest_reward_metas,):
        write(str(v))
        write(',')
    write(''');''')
    #end
    write('entryupdater.swich(starting_page);')
    write('</script></html>')
    file.close()


quest(repeat,
      requiment('elite goblin archer',18),
      requiment('2-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('shard',30),)

quest(request,
      requiment('mana mass',20),
      requiment('artificial god avenir',3),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(repeat,
      requiment('goblin warrior',12),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(repeat,
      requiment('rudrat',3),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('lucky-box',1),)

quest(repeat,
      requiment('elite goblin warrior',12),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('dust',30),)

quest(repeat,
      requiment('challenge mode',5),
      reward('gold',25000),
      reward('honor',5000),
      reward('crystal',155),
      reward('old-weapon-box',2),)

quest(request,
      requiment('yellow shadow rose cavalry',9),
      requiment('yellow shadow rose marksman',12),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(repeat,
      requiment('huntrat',12),
      requiment('1-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(repeat,
      requiment('goblin archer',12),
      requiment('2-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(request,
      requiment('horrifying red fury shadowdemon',3),
      requiment('turbulent library poltergeist',3),
      reward('gold',4000),
      reward('honor',500),
      reward('lucky-box',1),)

quest(repeat,
      requiment('kitchen poltergeist',3),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('lucky-box',1),)

quest(repeat,
      requiment('shadow rose agent',3),
      requiment('1-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('lucky-box',1),)

quest(repeat,
      requiment('elite goblin warrior',12),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('dust',30),)

quest(repeat,
      requiment('artificial god avenir',3),
      requiment('1-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('lucky-box',1),)

quest(request,
      requiment('warrat',18),
      requiment('huntrat',15),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(request,
      requiment('kitchen poltergeist',6),
      requiment('library poltergeist',6),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(repeat,
      requiment('kitchen poltergeist',9),
      requiment('mana mass',20),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(request,
      requiment('heavens cavalry soldier',12),
      requiment('heavens cavalry sergeant',3),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(request,
      requiment('red chaos shadowdemon',6),
      requiment('red fury shadowdemon',6),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(repeat,
      requiment('horrifying blue chaos shadowdemon',3),
      requiment('1-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('lucky-box',1),)

quest(repeat,
      requiment('mini ogre',12),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(repeat,
      requiment('bigrat',9),
      requiment('2-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(repeat,
      requiment('warrat',24),
      requiment('bigrat',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(repeat,
      requiment('elite mini ogre',6),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('crystal',30),)

quest(repeat,
      requiment('horrifying yellow shadow rose calvalry',3),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('lucky-box',1),)

quest(repeat,
      requiment('goblin catapult',15),
      requiment('2-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(request,
      requiment('goblin warrior',12),
      requiment('goblin archer',18),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(request,
      requiment('goblin warrior',12),
      requiment('goblin archer',18),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(repeat,
      requiment('horrifying blue shadow rose cavalry',3),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('lucky-box',1),)

quest(request,
      requiment('raid',5),
      reward('gold',25000),
      reward('honor-box',4),
      reward('lucky-box',3),
      reward('shard',120),)

quest(request,
      requiment('red shadow rose charger',24),
      requiment('red shadow rose marksman',6),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(repeat,
      requiment('challenge mode',2),
      reward('gold',10000),
      reward('honor',2000),
      reward('old-weapon-box',2),
      reward('dust',380),)     

quest(repeat,
      requiment('warrat',30),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(emergency,
      requiment('1-chain',20),
      requiment('goblin battlegorunds',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

quest(emergency,
      requiment('in the fellwood forest',3),
      reward('gold',42000),
      reward('honor',2300),
      reward('iron',1300),
      reward('lucky-box',3),)

quest(emergency,
      requiment('entyre team alive'),
      requiment('city of turmoil',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

quest(emergency,
      requiment('a hasty escape',3),
      reward('gold',40000),
      reward('honor',2000),
      reward('iron',1200),
      reward('lucky-box',3),)

###############  week 2 ##################

quest(repeat,
      requiment('red fury shadowdemon',6),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(emergency,
      requiment('2-chain',10),
      requiment('city of turmoil',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

quest(emergency,
      requiment('1-chain',20),
      requiment('city of turmoil',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

quest(emergency,
      requiment('entyre team alive'),
      requiment('goblin battlegorunds',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

quest(emergency,
      requiment('3-chain',15),
      requiment('city of turmoil',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

quest(request,
      requiment('bigrat',12),
      requiment('bombrat',9),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(request,
      requiment('mini ogre',18),
      requiment('goblin chief',3),
      reward('gold',4000),
      reward('honor',500),
      reward('lucky-box',1),)
      
quest(repeat,
      requiment('horrifying red shadow rose marksman',3),
      requiment('2-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('lucky-box',1),)

quest(request,
      requiment('mana mass',30),
      requiment('special skill',30),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(emergency,
      requiment('lord of the sewern',3),
      reward('gold',48000),
      reward('honor',2600),
      reward('iron',1800),
      reward('lucky-box',3),)

quest(emergency,
      requiment('1-chain',20),
      requiment('goblin battlegorunds',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

quest(emergency,
      requiment('the false creator',3),
      reward('gold',44000),
      reward('honor',2000),
      reward('iron',1400),
      reward('lucky-box',3),)

quest(repeat,
      requiment('library poltergeist',6),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(emergency,
      requiment('3-chain',15),
      requiment('goblin battlegorunds',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

quest(emergency,
      requiment('2-chain',10),
      requiment('goblin battlegorunds',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

quest(repeat,
      requiment('red shadow rose charger',12),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(request,
      requiment('colosseum',10),
      reward('gold',11000),
      reward('honor-box',4),
      reward('lucky-box',3),
      reward('ring-box',3),)

quest(request,
      requiment('rotting mutarat',18),
      requiment('giant mutarat',15),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(request,
      requiment('bewitched priest',3),
      requiment('bewitched magician',3),
      reward('gold',4000),
      reward('honor',500),
      reward('lucky-box',1),)

quest(request,
      requiment('goblin champion',6),
      requiment('mini ogre',6),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(request,
      requiment('warrat',18),
      requiment('dangerous warrat',3),
      reward('gold',4000),
      reward('honor',500),
      reward('lucky-box',1),)

quest(repeat,
      requiment('hybrid shadowdemon',3),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('lucky-box',1),)

quest(request,
      requiment('rotting mutarat',18),
      requiment('rudrat',3),
      reward('gold',4000),
      reward('honor',500),
      reward('lucky-box',1),)

quest(request,
      requiment('mana mass',20),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(request,
      requiment('mini ogre',18),
      requiment('goblin catapult',15),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(request,
      requiment('colosseum',15),
      reward('gold',15000),
      reward('honor-box',4),
      reward('lucky-box',3),
      reward('crystal',80),)

quest(repeat,
      requiment('mana mass',33),
      requiment('kitchen poltergeist',9),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(repeat,
      requiment('giant mutarat',18),
      requiment('2-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(request,
      requiment('raid',3),
      reward('gold',15000),
      reward('honor-box',4),
      reward('lucky-box',3),
      reward('dust',200),)

quest(repeat,
      requiment('challenge mode',4),
      reward('gold',20000),
      reward('honor',3000),
      reward('old-weapon-box',2),
      reward('shard',230),)

quest(repeat,
      requiment('horrifying red shadow rose cavalry',3),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('lucky-box',1),)

quest(request,
      requiment('yellow chaos shadowdemon',6),
      requiment('yellow fury shadowdemon',6),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

###############  week 3 ##################

quest(repeat,
      requiment('goblin chief',3),
      requiment('2-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('lucky-box',1),)

quest(repeat,
      requiment('library poltergeist',6),
      requiment('1-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(repeat,
      requiment('rudrat',3),
      requiment('2-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('lucky-box',1),)

quest(repeat,
      requiment('blue shadow rose cavalry',15),
      requiment('1-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(request,
      requiment('goblin warrior',6),
      requiment('goblin catapult',12),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(repeat,
      requiment('blue shadow rose marksman',15),
      requiment('1-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(repeat,
      requiment('red shadow rose cavalry',12),
      requiment('3-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(repeat,
      requiment('shadow rose priest',3),
      requiment('2-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('lucky-box',1),)

###############  week 4 ##################

quest(repeat,
      requiment('elite goblin catapult',6),
      requiment('1-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('shard',30),)

quest(request,
      requiment('red chaos shadowdemon',3),
      requiment('red fury shadowdemon',3),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(repeat,
      requiment('red chaos shadowdemon',9),
      requiment('2-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(request,
      requiment('yellow shadow rose cavalry',9),
      requiment('yellow shadow rose marksman',12),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

quest(repeat,
      requiment('blue shadow rose marksman',15),
      requiment('2-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(repeat,
      requiment('goblin champion',6),
      requiment('1-chain',30),
      reward('gold',4000),
      reward('honor',650),
      reward('iron',500),)

quest(request,
      requiment('blue shadow rose charger',12),
      requiment('blue shadow rose marksman',15),
      reward('gold',4000),
      reward('honor',500),
      reward('iron',500),)

#scout

quest(scout,
      requiment('enemies',50,'S2-E1-N-1'),
      reward('gold',5000),
      reward('honor',400),
      reward('iron',500),)

quest(scout,
      requiment('enemies',50,'S2-E1-N-2'),
      reward('gold',5000),
      reward('honor',400),
      reward('iron',500),)

quest(scout,
      requiment('enemies',50,'S2-E1-N-3'),
      reward('gold',5000),
      reward('honor',400),
      reward('iron',500),)

quest(scout,
      requiment('enemies',50,'S2-E1-N-4'),
      reward('gold',5000),
      reward('honor',400),
      reward('iron',500),)

#ubers

quest(emergency,
      requiment('1-chain',20),
      requiment('a plague in the detphs',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

quest(emergency,
      requiment('2-chain',10),
      requiment('a plague in the detphs',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

quest(emergency,
      requiment('3-chain',15),
      requiment('a plague in the detphs',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

quest(emergency,
      requiment('entyre team alive'),
      requiment('a plague in the detphs',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

#brainlord/bibi

quest(emergency,
      requiment('1-chain',20),
      requiment('the hidden palace',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

quest(emergency,
      requiment('2-chain',10),
      requiment('the hidden palace',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

quest(emergency,
      requiment('3-chain',15),
      requiment('the hidden palace',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

quest(emergency,
      requiment('entyre team alive'),
      requiment('the hidden palace',1),
      reward('gold',5000),
      reward('honor',1000),
      reward('lucky-box',1),)

if __name__=='__main__':
    createdocument()
