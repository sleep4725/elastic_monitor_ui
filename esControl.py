from serverInfo import ServerInfo
from threading import Thread

class EsControl:

    def __init__(self):
        self.es_config = self.data_setting()

    def data_setting(self):
        ret_es_config = ServerInfo.get_config()
        if ret_es_config["result"]:
            es_config = ret_es_config["data"]
            ServerInfo.is_server_alive(es_config=es_config)
            ServerInfo.is_service_alive(es_config=es_config)
            return es_config

    def es_all_service_close(self):
        ServerInfo.all_elastic_node_stop(es_config=self.es_config)

    def es_all_service_start(self):
        ServerInfo.all_elastic_node_start(es_config= self.es_config)

if __name__ == "__main__":
    esNode = EsControl()
    #esNode.es_all_service_close()
    esNode.es_all_service_start()
