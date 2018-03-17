# -*- coding: utf-8 -*-
from os.path import splitext
from PIL import Image as PIL
from base64 import b64encode
from io import BytesIO
from types import FunctionType as function, MethodType as method

def iterable(v):
    return hasattr(v,'__iter__') or (isinstance(v,(function,method)) and v.__code__.co_flags&32)

class oemg(object):
    '''operand error message generator'''
    __add__     =lambda a,b :TypeError("unsupported operand type(s) for +: '%s' and '%s'"        %(type(a).__name__,type(b).__name__))
    __radd__    =lambda a,b :TypeError("unsupported operand type(s) for +: '%s' and '%s'"        %(type(b).__name__,type(a).__name__))
    __iadd__    =lambda a,b :TypeError("unsupported operand type(s) for +=: '%s' and '%s'"       %(type(a).__name__,type(b).__name__))
    __sub__     =lambda a,b :TypeError("unsupported operand type(s) for -: '%s' and '%s'"        %(type(a).__name__,type(b).__name__))
    __rsub__    =lambda a,b :TypeError("unsupported operand type(s) for -: '%s' and '%s'"        %(type(b).__name__,type(a).__name__))
    __isub__    =lambda a,b :TypeError("unsupported operand type(s) for -=: '%s' and '%s'"       %(type(a).__name__,type(b).__name__))
    __eq__      =lambda a,b :TypeError("'==' not supported between instances of '%s' and '%s'"   %(type(a).__name__,type(b).__name__))
    __gt__      =lambda a,b :TypeError("'>' not supported between instances of '%s' and '%s'"    %(type(a).__name__,type(b).__name__))
    __st__      =lambda a,b :TypeError("'<' not supported between instances of '%s' and '%s'"    %(type(a).__name__,type(b).__name__))
    __ge__      =lambda a,b :TypeError("'>=' not supported between instances of '%s' and '%s'"   %(type(a).__name__,type(b).__name__))
    __se__      =lambda a,b :TypeError("'<=' not supported between instances of '%s' and '%s'"   %(type(a).__name__,type(b).__name__))
    __mul__     =lambda a,b :TypeError("unsupported operand type(s) for *: '%s' and '%s'"        %(type(a).__name__,type(b).__name__))
    __rmul__    =lambda a,b :TypeError("unsupported operand type(s) for *: '%s' and '%s'"        %(type(b).__name__,type(a).__name__))
    __imul__    =lambda a,b :TypeError("unsupported operand type(s) for *=: '%s' and '%s'"       %(type(a).__name__,type(b).__name__))
    
    __reversed__=lambda     :TypeError("'reversed' object is not reversible")
    missingattr =lambda a,b :AttributeError("'%s' object has no attribute '%s'"                 %(type(a).__name__,b))
    missingindex=lambda a   :ValueError(" %s is not in list"                                     %a)

def repeat_iterable(it,t):
    r=range(t)
    for v in it:
        for t in r:
            yield v
            
class removemeta(type):
    def __new__(meta,name,bases,values):
        hide={'__hide__','__overhide__'}
        overhide=set()        
        for cls in bases:
            if type(cls)==meta:
                hide=hide.union(cls.__hide__)
                overhide=overhide.union(cls.__overhide__)
        keys=tuple(values.keys())
        for key in keys:
            try:
                value=values[key]
            except KeyError:
                continue
            if type(value)==remove:
                del values[key]
                for thing in value:
                    hide.add(thing)
                    values[thing]=removed(thing)
            elif key in hide:
                hide.remove(key)
            elif key in overhide:
                overhide.remove(key)
        def __dir__(self):
            result=object.__dir__(self)
            rem=result.remove
            for value in self.__hide__:
                rem(value)
            return result
        __dir__.__module__=values['__module__']
        __dir__.__qualname__=values['__qualname__']+'.__dir__'
        values['__dir__']=__dir__
        values['__hide__']=hide
        values['__overhide__']=overhide
        return type.__new__(meta,name,bases,values)
    def __dir__(cls):
        result=type.__dir__(cls)
        rem=result.remove
        for value in cls.__hide__:
            rem(value)
        return result
    def __setattr__(cls,name,value):
        if name in cls.__hide__:
            hide=cls.__hide__
            hide.remove(name)
            cls.__overhide__.add(name)
        type.__setattr__(cls,name,value)
    def __delattr__(cls,name):
        if name in cls.__overhide__:
            cls.__hide__.add(name)
            cls.__overhide__.remove(name)
            type.__setattr__(cls,name,removed(name))
        else:
            type.__delattr__(cls,name)
            
class removed(property):
    overwritemeta='_@%s'
    def __init__(self,name):
        self.name=name
        self.overwrite=self.overwritemeta%name
    def __get__(self,obj,objtype=None):
        if obj is None:
            raise AttributeError("type object '%s' has no attribute '%s'"%(objtype.__name__,self.name))
        try:
            return getattr(obj,self.overwrite)
        except AttributeError as err:
            err.args=("'%s' object has no attribute '%s'"%(type(obj).__name__,self.name),)
            raise err
    def __set__(self,obj,value):
        overwrite=type(obj).__hide__.copy()
        overwrite.remove(self.name)
        overwrite.add(self.overwrite)
        object.__setattr__(obj,'__hide__',overwrite)
        setattr(obj,self.overwrite,value)
    def __delete__(self,obj):
        try:
            delattr(obj,self.overwrite)
            overwrite=obj.__hide__
            overwrite.remove(self.overwrite)
            overwrite.add(self.name)
            if overwrite==type(obj).__hide__:
                del obj.__hide__
        except AttributeError as err:
            err.args=(self.name,)
            raise
        
class remove(set):
    def __init__(self,*args):
        set.__init__(self,args)

class sortedlist(list,metaclass=removemeta):
    def __init__(self,it=None,reverse=False):
        if it is None:
            list.__init__(self,)
        else:
            list.__init__(self,it)
        list.sort(self,reverse=reverse)
        self._r=reverse
    def __getstate__(self):
        return self._r
    def __setstate__(self,state):
        self._r=state
    def get_reverse(self):
        return self._r
    def set_reverse(self,v):
        if self._r==v:
            return
        self._r=v
        list.reverse(self)
    reverse=property(get_reverse,set_reverse)
    del get_reverse,set_reverse
    def append(s,v):
        t=len(s)
        b=-1
        h=(b+t)>>1
        if s._r:
            while b!=h:
                if s[h]>v:
                    b=h
                    h=(b+t)>>1
                else:
                    t=h
                    h=(b+t)>>1
        else:
            while b!=h:
                if s[h]>v:
                    t=h
                    h=(b+t)>>1
                else:
                    b=h
                    h=(b+t)>>1
        list.insert(s,t,v)
    def extend(s,o):
        ln=len(s)
        insert=method(list.insert,s)
        b=-1
        
        if s._r:
            if type(s)!=type(o):
                o=sorted(o,reverse=True)
            elif not o._r:
                o=reversed(o)

            for v in o:
                t=ln
                ln+=1
                h=(t+b)>>1
                while b!=h:
                    if s[h]<v:
                        t=h
                        h=(b+t)>>1
                    else:
                        b=h
                        h=(b+t)>>1
                b-=1
                insert(t,v)
        else:
            if type(s)!=type(o):
                o=sorted(o)
            elif o._r:
                o=reversed(o)

            for v in o:
                t=ln
                ln+=1
                h=(t+b)>>1
                while b!=h:
                    if s[h]>v:
                        t=h
                        h=(b+t)>>1
                    else:
                        b=h
                        h=(b+t)>>1
                b-=1
                insert(t,v)
    def __contains__(s,v):
        t=len(s)
        if t==0:
            return False
        b=-1
        h=t>>1
        if s._r:
            while b!=h:
                if s[h]<v:
                    t=h
                    h=(b+t)>>1
                else:
                    b=h
                    h=(b+t)>>1
        else:
            while b!=h:
                if s[h]>v:
                    t=h
                    h=(b+t)>>1
                else:
                    b=h
                    h=(b+t)>>1
        if s[b]==v:
            return True
        return False
    def index(s,v):
        t=len(s)
        if t<2:
            if t==0:
                raise oemg.missingindex(v)
            elif s[0]==v:
                return 0
        else:
            b=-1
            h=(t>>1)-1
            if s._r:
                while b!=h:
                    if s[h]>v:
                        b=h
                        h=(b+t)>>1
                    else:
                        t=h
                        h=(b+t)>>1
            else:
                while b!=h:
                    if s[h]<v:
                        b=h
                        h=(b+t)>>1
                    else:
                        t=h
                        h=(b+t)>>1
            if s[t]==v:
                return t
        raise oemg.missingindex(v)
    def relativeindex(s,v):
        t=len(s)
        b=-1
        h=(t>>1)-1
        if s._r:
            while b!=h:
                if s[h]>v:
                    b=h
                    h=(b+t)>>1
                else:
                    t=h
                    h=(b+t)>>1
        else:
            while b!=h:
                if s[h]<v:
                    b=h
                    h=(b+t)>>1
                else:
                    t=h
                    h=(b+t)>>1
        return t
    def count(s,v):
        td=tu=len(s)
        if td==0:
            return False
        bd=bu=-1
        hd=hu=td>>1
        if s._r:
            while bd!=hd:
                if s[hd]>v:
                    bd=hd
                    hd=(bd+td)>>1
                else:
                    td=hd
                    hd=(bd+td)>>1
                if s[hu]<v:
                    tu=hu
                    hu=(bu+tu)>>1
                else:
                    bu=hu
                    hu=(bu+tu)>>1
        else:
            while bd!=hd:
                if s[hd]<v:
                    bd=hd
                    hd=(bd+td)>>1
                else:
                    td=hd
                    hd=(bd+td)>>1
                if s[hu]>v:
                    tu=hu
                    hu=(bu+tu)>>1
                else:
                    bu=hu
                    hu=(bu+tu)>>1
        return bu-bd
    def copy(self):
        new=list.__new__(type(self))
        list.__init__(new,self)
        new._r=self._r
        return new
    
    delete=remove('__setitem__','insert','sort')

    def __add__(s,o):
        if type(s)==type(o):
            if len(s)==0:
                return type(s)(o,s._r)
            if len(o)==0:
                return type(s)(s,s._r)
            
            new=type(s)(reverse=o._r)
            append=method(list.append,new)
            
            if s._r:
                s=iter(s)
                if o._r:
                    o=iter(o)
                else:
                    o=reversed(o)
                a=next(s)
                b=next(o)
                while True:
                    if b>a:
                        append(b)
                        try:
                            b=next(o)
                        except:
                            append(a)
                            for a in s:
                                append(a)
                            break
                    else:
                        append(a)
                        try:
                            a=next(s)
                        except:
                            append(b)
                            for b in o:
                                append(b)
                            break
            else:
                s=iter(s)
                if o._r:
                    o=reversed(o)
                else:
                    o=iter(o)
                a=next(s)
                b=next(o)
                while True:
                    if b<a:
                        append(b)
                        try:
                            b=next(o)
                        except:
                            append(a)
                            for a in s:
                                append(a)
                            break
                    else:
                        append(a)
                        try:
                            a=next(s)
                        except:
                            append(b)
                            for b in o:
                                append(b)
                            break
            return new

        ln=len(s)
        if ln==0:
            return type(s)(o,s._r)
        new=s.copy()
        insert=method(list.insert,new)
        if s._r:
            for v in o:
                t=ln
                ln+=1
                b=-1
                h=t>>1
                while b!=h:
                    if new[h]<v:
                        t=h
                        h=(b+t)>>1
                    else:
                        b=h
                        h=(b+t)>>1
                insert(t,v)
        else:
            for v in o:
                t=ln
                ln+=1
                b=-1
                h=t>>1
                while b!=h:
                    if new[h]>v:
                        t=h
                        h=(b+t)>>1
                    else:
                        b=h
                        h=(b+t)>>1
                insert(t,v)
        return new
    def __radd__(s,o):
        if type(s)==type(o):
            if len(s)==0:
                return type(s)(o,o._r)
            if len(o)==0:
                return type(s)(s,o._r)
            
            new=type(s)(reverse=o._r)
            append=method(list.append,new)

            if o._r:
                if s._r:
                    s=iter(s)
                else:
                    s=reversed(s)
                o=iter(o)
                a=next(s)
                b=next(o)
                while True:
                    if a>b:
                        append(a)
                        try:
                            a=next(s)
                        except:
                            append(b)
                            for b in o:
                                append(b)
                            break
                    else:
                        append(b)
                        try:
                            b=next(o)
                        except:
                            append(a)
                            for a in s:
                                append(a)
                            break
            else:
                if s._r:
                    s=reversed(s)
                else:
                    s=iter(s)
                o=iter(o)
                a=next(s)
                b=next(o)
                while True:
                    if a<b:
                        append(a)
                        try:
                            a=next(s)
                        except:
                            append(b)
                            for b in o:
                                append(b)
                            break
                    else:
                        append(b)
                        try:
                            b=next(o)
                        except:
                            append(a)
                            for a in s:
                                append(a)
                            break
            return new
        
        ln=len(s)
        if ln==0:
            return type(s)(o,s._r)
        new=s.copy()
        insert=method(list.insert,new)

        if s._r:
            for v in reversed(o):
                t=ln
                ln+=1
                b=-1
                h=t>>1
                while b!=h:
                    if new[h]>v:
                        b=h
                        h=(b+t)>>1
                    else:
                        t=h
                        h=(b+t)>>1
                insert(t,v)
        else:
            for v in reversed(o):
                t=ln
                ln+=1
                b=-1
                h=t>>1
                while b!=h:
                    if new[h]<v:
                        b=h
                        h=(b+t)>>1
                    else:
                        t=h
                        h=(b+t)>>1
                insert(t,v)
        return new
    def __iadd__(s,o):
        ln=len(s)
        if s._r:
            if ln==0:
                if type(s)!=type(o):
                    list.extend(s,sorted(o,reverse=True))
                elif o._r:
                    list.extend(s,o)
                else:
                    list.extend(s,reversed(o))
                return s
            if type(s)!=type(o):
                o=sorted(o,reverse=True)
            elif not o._r:
                o=reversed(o)
            insert=method(list.insert,s)

            b=0
            for v in o:
                t=ln
                b-=1
                h=(t+b)>>1
                ln+=1
                while b!=h:
                    if s[h]<v:
                        t=h
                        h=(b+t)>>1
                    else:
                        b=h
                        h=(b+t)>>1
                insert(t,v)
        else:
            if ln==0:
                if type(s)!=type(o):
                    list.extend(s,sorted(o))
                elif o._r:
                    list.extend(s,reversed(o))
                else:
                    list.extend(s,o)
                return s
            if type(s)!=type(o):
                o=sorted(o)
            elif o._r:
                o=reversed(o)
            insert=method(list.insert,s)
            
            b=0
            for v in o:
                t=ln
                b-=1
                h=(t+b)>>1
                ln+=1
                while b!=h:
                    if s[h]>v:
                        t=h
                        h=(b+t)>>1
                    else:
                        b=h
                        h=(b+t)>>1
                insert(t,v)
        return s
    def __mul__(s,o):
        new=type(s)(reverse=s._r)
        list.extend(new,repeat_iterable(s,o))
        return new
    __rmul__=__mul__
    def __imul__(s,o):
        r=range(o)
        insert=method(list.insert,s)
        o+=1
        for i in range(0,len(s)*o,o):
            v=s[i]
            for t in r:
                insert(i,v)
        return s

def _it_con_builder(it,start,end):
    it=iter(it)
    _next=it.__next__
    try:
        v0=_next()
    except:
        yield start+end
        return
    try:
        v1=_next()
        yield start+str(v0)
    except:
        yield start+str(v0)+end
        return
    while True:
        try:
            v0=_next()
            yield str(v1)
        except:
            yield str(v1)+end
            return
        try:
            v1=_next()
            yield str(v0)
        except:
            yield str(v0)+end
            return
    
def it_con(it,sep=', ',start='[',end=']'):
    return sep.join(_it_con_builder(it,start,end))

def deconverter(name,colors):
    filename,extension=splitext(name)
    image=PIL.open(name)
    extension=extension[1:]
    start=b'data:image/%s;base64,'%extension.encode()
    def f():
        nonlocal colors
        step=255/(colors-1)
        actvalue=0
        output=0
        limit=step/2
        for i in range(256):
            if i>limit:
                limit+=step
                actvalue+=step
                output=round(actvalue)
            yield output
    array=bytes(f())
    image=PIL.eval(image,lambda x:array[x])
    buffer=BytesIO()
    image.save(buffer,extension)
    image=b64encode(buffer.getvalue())
    return start+image
