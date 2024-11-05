import numpy as np

import warnings

class W_Ref_Warnings( UserWarning ):
    pass
class W_Ref_Iterator( W_Ref_Warnings ):
    pass
class W_Ref_IteratorLimits( W_Ref_Iterator ):
    pass

class DimIterator:
    def __init__( self, min, max, step ):
        self.min = min
        self.max = max
        self.step= step

    def __iter__( self ):
        self.val = self.min
        return self
    
    def __next__(self):
        if self.val >= self.max and self.val > self.min:    #   Se self.min == self.max eseguo almeno una volta 
            raise StopIteration
        else:
            ret = self.val
            self.val += self.step
            return ret
        
class Dimension:
    def __init__( self, dn="", dl=[0.0, 1.0], dd=0.1 ):
        self.name   = dn    #   Nome dimensione
        self.limits = dl    #   Limiti (minimo, massimo) nel sistema di riferimento locale
        self.d      = dd    #   step "infinitesimo" per iterare tra self.limits[0] e self.limits[1]
        self.iter   = iter( DimIterator( dl[0], dl[1], dd) )

    def __str__( self ):
        return "{0:3s}: Min: {1:>8.5f} Max: {2:>8.5f} d: {3:>8.5f}".format( self.name, self.limits[0], self.limits[1], self.d )

    def set( self, dn=None, dl=None, dd=None ):
        if dn != None:
            self.name  = dn
        if dl != None:
            self.limits= dl
            self.iter   = iter( DimIterator( dl[0], dl[1], self.d ) )
        if dd != None:
            self.d     = dd
            self.iter   = iter( DimIterator( self.limits[0], self.limits[1], dd ) )
    
    def get_iterator( self, min = 0.0, max = 0.0, step = 0.0 ):
        if min < self.limits[ 0 ]:
            warnings.warn("Valore min inferiore al limite per la dimensione {}.".format( self.name ), W_Ref_IteratorLimits)
        if max > self.limits[ 1 ]:
            warnings.warn("Valore max superiore al limite per la dimensione {}.".format( self.name ), W_Ref_IteratorLimits)
        if min < max and step < 0:
            warnings.warn("Errore nei valori min, max e step per la dimensione {}.".format( self.name ), W_Ref_IteratorLimits)
        if min > max and step > 0:
            warnings.warn("Errore nei valori min, max e step per la dimensione {}.".format( self.name ), W_Ref_IteratorLimits)

        return iter( DimIterator( min, max, step ) )
    
class SysReference:
    def __init__( self, s_dim=1, s_name="", d_name=None ):
        #   s_dim:      Numero di dimensioni del sistema di riferimento
        #   s_name:     Nome del sistema di riferimento
        #   d_name:     Array con i nomi di ciascuna dimensione del sistema di riferimento
        self.space_dim      = s_dim         #   Numero di dimensioni del sistema di riferimento
        self.space_name     = s_name        #   Nome del sistema di riferimento
        self.dimension      = [None]*s_dim  #   Array delle dimensioni del sistema di riferimento
        for i in range( s_dim ):
            if d_name != None:
                s = d_name[ i ]
            else:
                s = "{0}{1}".format( s_name, i )
            self.dimension[ i ] = Dimension( dn=s )
        self.sysref_from    = []            #   Lista di isomorfismi che trasformano in questo sistema di riferimento
        self.sysref_to      = []            #   Lista di isomorfismi che trasformano da questo sistema di riferimento

    def __repr__( self ):
        return "SysReference"

    def __str__( self ):
        s = "Sistema di riferimento:\n"
        s = s + "{0}Nome: {1:8s}\n".format( "\t"*1, self.space_name )
        s = s + "{0}Dimensioni: {1:3d}\n".format( "\t"*1, self.space_dim )
        for i in range( len( self.dimension ) ):
            s = s + "{0}{1}\n".format( "\t"*2, self.dimension[ i ] )
        s = s + "Isomorfismi entranti:\n"
        for i in range( len( self.sysref_from ) ):
            s = s + "{0}{1:3d}: {2}\n".format( "\t"*1, i, self.sysref_from[ i ] )
        s = s + "Isomorfismi uscenti:\n"
        for i in range( len( self.sysref_to ) ):
            s = s + "{0}{1:3d}: {2}\n".format( "\t"*1, i, self.sysref_to[ i ] )
        
        return s
    
    def vect_to_string( self, v ):
        s = ""
        l = len( v )
        for i in range( l ):
            s = s + "{0:>8.5f}".format( v[ i ] )
            if self.dimension[ i ].name != "":
                s = s + " {0}".format( self.dimension[ i ].name )
            if i < l - 1:
                s = s + ", "
        return " ( {0} )".format( s )
