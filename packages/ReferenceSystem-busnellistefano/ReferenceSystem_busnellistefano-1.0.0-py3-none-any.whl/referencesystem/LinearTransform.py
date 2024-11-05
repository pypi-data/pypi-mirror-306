from .BaseTransform import *
import numpy as np

#   Estendo classe base di eccezione per le parametrizzazioni
class E_LTr_Exceprion( E_Btr_Exception ):
    def __init__( self ):
        self.message = "Errore generico di parametrizzazione."
        
#   Eccezioni custom
class E_LTr_WrongMatrix( E_LTr_Exceprion ):
    def __init__( self ):
        self.message = "Struttura della matrice errata."

class E_LTr_MatrixNull( E_LTr_Exceprion ):
    def __init__( self ):
        self.message = "Matrice della trasformazione lineare non definita."

class LinearTransform( BaseTransForm ):
    # dom_space:    dominio della trasformazione lineare
    # img_space:    immagine della trasformazione lineare
    def __init__( self, dom_space = None, img_space = None ):
        super().__init__( dom_space, img_space )

        self.matrix     = []
        self.parameters = 0

    def set_matrix( self, mat = None, parameters = 0 ):
        i_shp = ( parameters, )
        o_shp = ( self.domain_space.space_dim, self.image_space.space_dim , )
        try:
            v_vec   = np.zeros( i_shp )
            ret     = mat( v_vec )
        except:
            raise E_LTr_WrongMatrix
        
        #   Test dimensione degli spazi dominio ed immagine della trasformazione lineare definita da mat
        if ret.shape != o_shp:
            raise E_LTr_WrongMatrix

        self.matrix     = mat
        self.parameters = parameters


    def get_matrix( self, v_vec = [] ):
        o_shp = ( self.domain_space.space_dim, self.image_space.space_dim )
        if self.matrix == None:
            raise E_LTr_MatrixNull

        try:
            ret = self.matrix( v_vec )
        except:
            raise E_LTr_WrongMatrix
        
        #   Test dimensione degli spazi dominio ed immagine della trasformazione lineare definita da mat
        if ret.shape != o_shp:
            raise E_LTr_WrongMatrix
        
        return ret
