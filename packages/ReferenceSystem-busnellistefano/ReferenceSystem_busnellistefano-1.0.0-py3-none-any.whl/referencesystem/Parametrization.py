from .BaseTransform import *
import numpy as np

#   Estendo classe base di eccezione per le parametrizzazioni
class E_Par_Exceprion( E_Btr_Exception ):
    def __init__( self ):
        self.message = "Errore generico di parametrizzazione."

#   Eccezioni custom
class E_Par_ParametrizationNull( E_Par_Exceprion ):
    def __init__( self ):
        self.message = "Parametrizzazione non definita."
class E_Par_ParametrizationWrong( E_Par_Exceprion ):
    def __init__( self ):
        self.message = "Struttura dell'array restituito della parametrizzazione errata."

class E_Par_TangentSpaceNull( E_Par_Exceprion ):
    def __init__( self ):
        self.message = "Spazio tangente non definito."
class E_Par_TangentSpaceWrong( E_Par_Exceprion ):
    def __init__( self ):
        self.message = "Struttura dell'array restituito per lo spazio tangente errata."

class E_Par_CotangentSpaceNull( E_Par_Exceprion ):
    def __init__( self ):
        self.message = "Spazio cotangente non definito."
class E_Par_CotangentSpaceWrong( E_Par_Exceprion ):
    def __init__( self ):
        self.message = "Struttura dell'array restituito per lo spazio cotangente errata."

class E_Par_MetricNull( E_Par_Exceprion ):
    def __init__( self ):
        self.message = "Metrica non definita."
class E_Par_MetricWrong( E_Par_Exceprion ):
    def __init__( self ):
        self.message = "Struttura dell'array restituito per la metrica errata."

class E_Par_HessianNull( E_Par_Exceprion ):
    def __init__( self ):
        self.message = "Hessiana non definita."
class E_Par_HessianWrong( E_Par_Exceprion ):
    def __init__( self ):
        self.message = "Struttura dell'array restituito per l'Hessiana errata."

class E_Par_ChristoffelNull( E_Par_Exceprion ):
    def __init__( self ):
        self.message = "Connessione affine non definita."
class E_Par_ChristoffelWrong( E_Par_Exceprion ):
    def __init__( self ):
        self.message = "Struttura dell'array restituito per la connessione affine errata."

class E_Par_GeodesicNull( E_Par_Exceprion ):
    def __init__( self ):
        self.message = "Geodetica non definita."
class E_Par_GeodesicWrong( E_Par_Exceprion ):
    def __init__( self ):
        self.message = "Struttura dell'array restituito per la geodetica errata."

class Parametrization( BaseTransForm ):
    def __init__( self, dom_space = None, img_space = None ):
        super().__init__( dom_space, img_space )

        self.position_vector    = None  #   Funzione che restituisce il vettore posizione
        self.tangent_space      = None  #   Funzione che restituisce i vettori tangenti alla parametrizzazione. Derivate parziali d( img_space )/d( dom_space )
        self.cotangent_space    = None  #   Funzione che restituisce i vettori dello spazio co-tangente
        self.metric             = None  #   Funzione che restituisce il tensore metrico
        self.hessian            = None  #   Funzione che restituisce l' hessiana
        self.christoffel        = None  #   Funzione che restituisce la matrice della connessione affine
        self.geodesic           = None  #   Funzione che restituisce la matrice dell' accelerazione della geodetica

    #   Metodi set
    
    def set_position_vector( self, mat = None ):
        i_shp = ( self.domain_space.space_dim, )
        o_shp = ( self.image_space.space_dim , )
        try:
            #   Test dimensione degli spazi dominio ed immagine della parametrizzazione definita da mat
            v_vec   = np.zeros( i_shp )
            ret     = mat( v_vec )
        except:
            raise E_Par_ParametrizationWrong
        if ret.shape != o_shp:
            raise E_Par_ParametrizationWrong

        self.position_vector    = mat
        self.tangent_space      = None
        self.cotangent_space    = None
        self.metric             = None
        self.hessian            = None
        self.christoffel        = None
        self.geodesic           = None
        
    def set_tangent_space( self, mat = None ):
        i_shp = ( self.domain_space.space_dim, )
        o_shp = ( self.domain_space.space_dim, self.image_space.space_dim )
        try:
            v_vec   = np.zeros( i_shp )
            ret     = mat( v_vec )
        except:
            raise E_Par_TangentSpaceWrong
        if ret.shape != o_shp:
            raise E_Par_TangentSpaceWrong
        
        self.tangent_space      = mat
        self.cotangent_space    = None
        self.metric             = None
        self.hessian            = None
        self.christoffel        = None
        self.geodesic           = None

    def set_cotangent_space( self, mat = None ):
        i_shp = ( self.domain_space.space_dim, )
        o_shp = ( self.domain_space.space_dim, self.image_space.space_dim )
        try:
            v_vec   = np.zeros( i_shp )
            ret     = mat( v_vec )
        except:
            raise E_Par_CotangentSpaceWrong
        if ret.shape != o_shp:
            raise E_Par_CotangentSpaceWrong
        
        self.cotangent_space    = mat

    def set_metric( self, mat = None ):
        i_shp = ( self.domain_space.space_dim, )
        o_shp = ( self.domain_space.space_dim, self.domain_space.space_dim )
        try:
            v_vec   = np.zeros( i_shp )
            ret     = mat( v_vec )
        except:
            raise E_Par_MetricWrong
        if ret.shape != o_shp:
            raise E_Par_MetricWrong
        
        self.metric             = mat
        self.hessian            = None
        self.christoffel        = None
        self.geodesic           = None

    def set_hessian( self, mat = None ):
        i_shp = ( self.domain_space.space_dim, )
        o_shp = ( self.domain_space.space_dim, self.domain_space.space_dim, self.image_space.space_dim )
        try:
            v_vec   = np.zeros( i_shp )
            ret     = mat( v_vec )
        except:
            raise E_Par_HessianWrong
        if ret.shape != o_shp:
            raise E_Par_HessianWrong
        
        self.hessian            = mat
        self.christoffel        = None
        self.geodesic           = None

    def set_christoffel( self, mat = None ):
        i_shp = ( self.domain_space.space_dim, )
        o_shp = ( self.domain_space.space_dim, self.domain_space.space_dim, self.domain_space.space_dim )
        try:
            v_vec   = np.zeros( i_shp )
            ret     = mat( v_vec )
        except:
            raise E_Par_ChristoffelWrong
        if ret.shape != o_shp:
            raise E_Par_ChristoffelWrong
        
        self.christoffel        = mat
        self.geodesic           = None

    def set_geodesic( self, mat = None ):
        i_shp = ( self.domain_space.space_dim, )
        o_shp = ( self.domain_space.space_dim, )
        try:
            v_vec   = np.zeros( i_shp )
            ret     = mat( v_vec, v_vec )
        except:
            raise E_Par_GeodesicWrong
        if ret.shape != o_shp:
            raise E_Par_GeodesicWrong
        
        self.geodesic           = mat
    
    #   Metodi get

    def get_position_vector( self, v_vec = [] ):
        i_shp = ( self.domain_space.space_dim, )
        o_shp = ( self.image_space.space_dim , )
        if self.position_vector == None:
            raise E_Par_ParametrizationNull
        if v_vec.shape != i_shp:
            raise E_Par_ParametrizationWrong

        try:
            ret = self.position_vector( v_vec )
        except:
            raise E_Par_ParametrizationWrong
        if ret.shape != o_shp:
            raise E_Par_ParametrizationWrong
        return ret

    def get_tangent_space( self, v_vec = [] ):
        i_shp = ( self.domain_space.space_dim, )
        o_shp = ( self.domain_space.space_dim, self.image_space.space_dim )
        if self.tangent_space == None:
            raise E_Par_TangentSpaceNull
        if v_vec.shape != i_shp:
            raise E_Par_ParametrizationWrong

        try:
            ret = self.tangent_space( v_vec )
        except:
            raise E_Par_TangentSpaceWrong
        if ret.shape != o_shp:
            raise E_Par_TangentSpaceWrong
        return ret

    def get_cotangent_space( self, v_vec = [] ):
        i_shp = ( self.domain_space.space_dim, )
        o_shp = ( self.domain_space.space_dim, self.image_space.space_dim )
        # if self.cotangent_space == None:
        #     raise E_Par_CotangentSpaceNull
        if v_vec.shape != i_shp:
            raise E_Par_ParametrizationWrong

        if self.cotangent_space != None:
            try:
                ret = self.cotangent_space( v_vec )
            except:
                raise E_Par_CotangentSpaceWrong
        else:
            #   Provo a calcolare spazio cotangente
            try:
                G = self.get_metric( v_vec )
                g = np.linalg.inv( G )
                T = self.get_tangent_space( v_vec )
                ret = np.dot( g, T )
            except E_Par_Exceprion as e:
                print( "Errore: {}\n".format( e.message ) )
                raise E_Par_CotangentSpaceNull
        if ret.shape != o_shp:
            raise E_Par_CotangentSpaceWrong
        return ret
    
    def get_tangent_vector( self, n_dim = 0, v_vec = [] ):
        i_shp = ( self.domain_space.space_dim, )
        o_shp = ( self.image_space.space_dim , )
        if self.tangent_space == None:
            raise E_Par_TangentSpaceNull
        if v_vec.shape != i_shp:
            raise E_Par_ParametrizationWrong

        ret = self.tangent_space( v_vec )
        if ret[ n_dim ].shape != o_shp:
            raise E_Par_TangentSpaceWrong
        return ret[ n_dim ]

    # def get_normal_vector( self, v_vec = [] ):
    #     i_shp = ( self.domain_space.space_dim, )
    #     o_shp = ( self.image_space.space_dim , )
    #     if v_vec.shape != i_shp:
    #         raise E_Par_ParametrizationWrong

    #     T   = self.get_tangent_space( v_vec )
    #     ret = np.cross( T[ 0 ], T[ 1 ] )

    #     if ret.shape != o_shp:
    #         raise E_Par_MetricWrong
    #     return ret

    def get_metric( self, v_vec = [] ):
        i_shp = ( self.domain_space.space_dim, )
        o_shp = ( self.domain_space.space_dim, self.domain_space.space_dim )
        if v_vec.shape != i_shp:
            raise E_Par_ParametrizationWrong

        if self.metric != None:
            try:
                ret = self.metric( v_vec )
            except:
                raise E_Par_MetricWrong
        else:
            #   provo ad calcolare la matrice
            try:
                ts = self.get_tangent_space( v_vec )
                tts= np.transpose( ts )
                ret = np.dot( ts, tts )
            except E_Par_Exceprion as e:
                print( "Errore: {}\n".format( e.message ) )
                raise E_Par_MetricNull
        if ret.shape != o_shp:
            raise E_Par_MetricWrong
        return ret

    def get_hessian( self, v_vec = [] ):
        i_shp = ( self.domain_space.space_dim, )
        o_shp = ( self.domain_space.space_dim, self.domain_space.space_dim, self.image_space.space_dim )
        if self.hessian == None:
            raise E_Par_HessianNull
        if v_vec.shape != i_shp:
            raise E_Par_ParametrizationWrong

        try:
            ret = self.hessian( v_vec )
        except:
            raise E_Par_HessianWrong
        if ret.shape != o_shp:
            raise E_Par_HessianWrong
        return ret

    def get_christoffel( self, v_vec = [] ):
        i_shp = ( self.domain_space.space_dim, )
        o_shp = ( self.domain_space.space_dim, self.domain_space.space_dim, self.domain_space.space_dim )
        if v_vec.shape != i_shp:
            raise E_Par_ParametrizationWrong

        if self.christoffel != None:
            try:
                ret = self.christoffel( v_vec )
            except:
                raise E_Par_ChristoffelWrong
        else:
            #   provo ad calcolare la matrice
            try:
                ret = np.zeros( o_shp )
                H = self.get_hessian( v_vec )
                C = self.get_cotangent_space( v_vec )
                for i in range( o_shp[ 0 ] ):
                    for j in range( o_shp[ 1 ] ):
                        for k in range( o_shp[ 2 ] ):
                            ret[ i, j, k ] = np.dot( C[ i ], H[ j, k ] )
            except E_Par_Exceprion as e:
                print( "Errore: {}\n".format( e.message ) )
                raise E_Par_ChristoffelNull
        if ret.shape != o_shp:
            raise E_Par_ChristoffelWrong
        return ret
        
    def get_geodesic( self, p_vec = [], v_vec = [] ):
        #   p_vec:  vettore posizione sulla curva
        #   v_vec:  vettore tangente alla curva
        #   ret:    vettore accelerazione lungo la curva
        i_shp = ( self.domain_space.space_dim, )
        o_shp = ( self.domain_space.space_dim, )

        if v_vec.shape != i_shp:
            raise E_Par_ParametrizationWrong
        if p_vec.shape != i_shp:
            raise E_Par_ParametrizationWrong

        if self.geodesic != None:
            try:
                ret = self.geodesic( p_vec, v_vec )
            except:
                raise E_Par_GeodesicWrong
        else:
            #   provo ad calcolare la matrice
            try:
                ret = np.zeros( o_shp )
                G = self.get_christoffel( p_vec )
                for i in range( o_shp[ 0 ] ):
                    for j in range( i_shp[ 0 ] ):
                        for k in range( i_shp[ 0 ] ):
                            ret[ i ] = ret[ i ] - G[ i, j, k] * v_vec[ j ] * v_vec[ k ]
            except E_Par_Exceprion as e:
                print( "Errore: {}\n".format( e.message ) )
                raise E_Par_GeodesicNull
        if ret.shape != o_shp:
            raise E_Par_GeodesicWrong
        return ret