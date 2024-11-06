# -*- coding: utf-8 -*-
from chibi_requests import Chibi_url
from chibi_hybrid import Class_property


class Chibi_inner_api( Chibi_url ):
    def __getattr__( self, name ):
        try:
            return super().__getattribute__( name )
        except AttributeError:
            result = self._build_url( name )
            return result

    def _build_url( self, name, *args, **kw ):
        result = type( self )( self, parent=self, **kw ) + name
        return result


class Chibi_api( Chibi_url ):
    schema = 'http'
    host = None
    inner_api_class = None

    def __new__( cls, *args, **kw ):
        if cls.host is None:
            raise NotImplementedError
        if cls.schema is None:
            raise NotImplementedError
        if not args:
            obj = super().__new__( cls, f'{cls.schema}://{cls.host}', **kw )
        else:
            obj = super().__new__( cls, *args, **kw )

        if not cls.inner_api_class:
            obj._API = Chibi_inner_api( obj, parent=obj )
        else:
            obj._API = cls.inner_api_class( obj, parent=obj )
        return obj

    @Class_property
    def API( cls ):
        instance = cls()
        return instance.API

    @API.instance
    def API( self ):
        return self._API
