#   Estendo classe base di eccezione per le trasformazioni
class E_Btr_Exception( BaseException ):
    def __init__( self ):
        self.message = "Errore generico trasformazioni."

#   Eccezioni custom base per le trasformazioni di distemi di riferimento
class E_BTr_SysRefNull( E_Btr_Exception ):
    def __init__( self ):
        self.message = "Non posso trasformare uno spazio vuoto."
        
class E_BTr_PametrizationNull( E_Btr_Exception ):
    def __init__( self ):
        self.message = "Non posso trasformare senza una funzione."

class BaseTransForm:
    def __init__( self, loc_sys = None, dst_sys = None ):
        self.name           = ""
        self.domain_space   = None      # Spazio dominio della funzione
        self.image_space    = None      # Spazio immagine della funzione

        if loc_sys == None:
            raise E_BTr_SysRefNull
        else:
            self.domain_space   = loc_sys
        
        if dst_sys == None:
            raise E_BTr_SysRefNull
        else:
            self.image_space    = dst_sys
        
        self.name               = self.domain_space.space_name + "-" + self.image_space.space_name

        self.domain_space.sysref_to.append( self )              #   Aggiungo questa parametrizzazione al sistema di riferimento di partenza
        self.image_space.sysref_from.append( self )             #   Aggiungo questa parametrizzazione al sistema di riferimento di destinazione
    
    def __str__( self ):
        s = ""
        s = s + "{}\n".format( self.name )
        return s
