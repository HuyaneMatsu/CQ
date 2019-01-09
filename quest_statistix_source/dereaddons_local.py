# -*- coding: utf-8 -*-
from os.path import splitext
from PIL import Image as PIL
from base64 import b64encode
from io import BytesIO
from types import MethodType as method

def repeat_iterable(it,t):
    r=range(t)
    for v in it:
        for t in r:
            yield v
            
class removemeta(type):
    def __new__(meta,name,bases,values):
        hide={'__hide__'}
        for cls in bases:
            if type(cls)==meta:
                hide=hide.union(cls.__hide__)
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
        
        for key in keys:
            if key in hide:
                hide.remove(key)
                values[key]=removed(key)
        def __dir__(self):
            result=object.__dir__(self)
            for value in self.__hide__:
                result.remove(value)
            return result
        __dir__.__module__=values['__module__']
        __dir__.__qualname__=values['__qualname__']+'.__dir__'
        values['__dir__']=__dir__
        values['__hide__']=hide

        return type.__new__(meta,name,bases,values)
    def __dir__(cls):
        result=type.__dir__(cls)
        for value in cls.__hide__:
            result.remove(value)
        return result
    def __setattr__(cls,name,value):
        if name in cls.__hide__:
            cls.__hide__.remove(name)
        type.__setattr__(cls,name,value)
            
class removed:
    __slots__=['name']
    def __init__(self,name):
        self.name=name
    def __get__(self,obj,objtype=None):
        if obj is None:
            raise AttributeError(f"type object '{objtype.__name__}' has no attribute '{self.name}'")
        raise AttributeError(f"'{obj.__class__.__name__}' object has no attribute '{self.name}'")
    def __set__(self,obj,value):
        raise AttributeError
    def __delete__(self,obj):
        raise AttributeError
        
class remove(set):
    __slots__=[]
    def __init__(self,*args):
        set.__init__(self,args)
        
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
    return sep.join(list(_it_con_builder(it,start,end)))

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
    def append(self,value):
        list.insert(self,self.relativeindex(value),value)
    def extend(self,other):
        top=ln=len(self)
        insert=list.insert
        bot=0
        if self._r:
            if type(self)!=type(other):
                other=sorted(other,reverse=True)
            elif not other._r:
                other=reversed(other)
            for value in other:
                top=ln
                while True:
                    if bot<top:
                        half=(bot+top)>>1
                        if self[half]>value:
                            bot=half+1
                        else:
                            top=half
                        continue
                    break
                insert(self,bot,value)
                ln+=1
                top=ln
        else:
            if type(self)!=type(other):
                other=sorted(other)
            elif other._r:
                other=reversed(other)
            for value in other:
                top=ln
                while True:
                    if bot<top:
                        half=(bot+top)>>1
                        if self[half]<value:
                            bot=half+1
                        else:
                            top=half
                        continue
                    break
                insert(self,bot,value)
                ln+=1
                top=ln
    def __contains__(self,value):
        if len(self)==0:
            return False
        return self[self.relativeindex(value)]==value
    def index(self,value):
        index=self.ralitiveindex(value)
        if len(self)==0 or self[index]!=value:
            raise ValueError('%s is not in list'%value)
        return index
    def relativeindex(self,value):
        bot=0
        top=len(self)
        if self._r:
            while True:
                if bot<top:
                    half=(bot+top)>>1
                    if self[half]>value:
                        bot=half+1
                    else:
                        top=half
                    continue
                break
        else:
            while True:
                if bot<top:
                    half=(bot+top)>>1
                    if self[half]<value:
                        bot=half+1
                    else:
                        top=half
                    continue
                break
        return bot
    def count(self,value):
        top_down=top_up=len(self)
        bot_down=bot_up=0
        if self._r:
            while True:
                if bot_down<top_down:
                    half_down=(bot_down+top_down)>>1
                    if self[half_down]>value:
                        bot_down=half_down+1
                    else:
                        top_down=half_down
                    half_up=(bot_up+top_up)>>1
                    if self[half_up]<value:
                        top_up=half_up
                    else:
                        bot_up=half_up+1
                    continue
                break
        else:
            while True:
                if bot_down<top_down:
                    half_down=(bot_down+top_down)>>1
                    if self[half_down]<value:
                        bot_down=half_down+1
                    else:
                        top_down=half_down
                    half_up=(bot_up+top_up)>>1
                    if self[half_up]>value:
                        top_up=half_up
                    else:
                        bot_up=half_up+1
                    continue
                break
        return bot_up-bot_down
    def copy(self):
        new=list.__new__(type(self))
        list.__init__(new,self)
        new._r=self._r
        return new
    def re_sort(self):
        list.sort(self,self._r)
    delete=remove('__setitem__','insert','sort')

    def __add__(self,other):
        if type(self)==type(other):
            if len(self)==0:
                return type(self)(other,self._r)
            if len(other)==0:
                return type(self)(self,self._r)
            
            new=type(self)(reverse=other._r)
            append=list.append
            
            if self._r:
                self=iter(self)
                if other._r:
                    other=iter(other)
                else:
                    other=reversed(other)
                a=next(self)
                b=next(other)
                while True:
                    if b>a:
                        append(new,b)
                        try:
                            b=next(other)
                        except:
                            append(new,a)
                            for a in self:
                                append(new,a)
                            break
                    else:
                        append(new,a)
                        try:
                            a=next(self)
                        except:
                            append(new,b)
                            for b in other:
                                append(new,b)
                            break
            else:
                self=iter(self)
                if other._r:
                    other=reversed(other)
                else:
                    other=iter(other)
                a=next(self)
                b=next(other)
                while True:
                    if b<a:
                        append(new,b)
                        try:
                            b=next(other)
                        except:
                            append(new,a)
                            for a in self:
                                append(mew,a)
                            break
                    else:
                        append(new,a)
                        try:
                            a=next(self)
                        except:
                            append(new,b)
                            for b in other:
                                append(new,b)
                            break
            return new

        ln=len(self)
        if ln==0:
            return type(self)(other,self._r)
        new=self.copy()
        new.exten(other)
        return new
    def __radd__(self,other):
        if type(self)==type(other):
            if len(self)==0:
                return type(self)(other,other._r)
            if len(other)==0:
                return type(self)(self,other._r)
            
            new=type(self)(reverse=other._r)

            if other._r:
                if self._r:
                    self=iter(self)
                else:
                    self=reversed(self)
                other=iter(other)
                a=next(self)
                b=next(other)
                while True:
                    if a>b:
                        append(new,a)
                        try:
                            a=next(self)
                        except:
                            append(new,b)
                            for b in other:
                                append(new,b)
                            break
                    else:
                        append(new,b)
                        try:
                            b=next(other)
                        except:
                            append(new,a)
                            for a in self:
                                append(new,a)
                            break
            else:
                if self._r:
                    self=reversed(self)
                else:
                    self=iter(self)
                other=iter(other)
                a=next(self)
                b=next(other)
                while True:
                    if a<b:
                        append(new,a)
                        try:
                            a=next(self)
                        except:
                            append(new,b)
                            for b in other:
                                append(new,b)
                            break
                    else:
                        append(new,b)
                        try:
                            b=next(other)
                        except:
                            append(new,a)
                            for a in self:
                                append(new,a)
                            break
            return new
        
        ln=len(self)
        if ln==0:
            return type(self)(other,self._r)
        new=self.copy()
        new.extend(other)
    __iadd__=extend
    def __mul__(self,other):
        new=type(self)(reverse=self._r)
        if other<1:
            return new
        append=list.append
        r=range(3)
        for value in self:
            for x in r:
                append(new,value)
        return new
    __rmul__=__mul__
    def __imul__(self,other):
        if other<1:
            return self
        r=range(other-1)
        insert=list.insert
        for index in range(len(self)-1,-1,-1):
            value=self[index]
            for x in r:
                insert(self,index,value)
        return self

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
