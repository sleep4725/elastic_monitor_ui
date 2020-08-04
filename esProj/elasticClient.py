from esProj.esControl import EsControl

class ElasticClient(EsControl):

    def __init__(self):
        EsControl.__init__(self)
        self.es_conn = ""

    def ret_elastic_client(self):
        pass