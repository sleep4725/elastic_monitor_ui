from esProj.serverInfo import ServerInfo

#
#
#

class EsControl:

    def __init__(self):
        self.es_config = self.data_setting()

    def data_setting(self):
        ret_es_config = ServerInfo.get_config()
        if ret_es_config["result"]:
            es_config = ret_es_config["data"]
            ServerInfo.is_server_alive(es_config=es_config)
            ServerInfo.is_service_alive(es_config=es_config)
            print (es_config)
            return es_config

    # 운영중인 모든 elastic node를 run
    def es_all_service_close(self):
        ServerInfo.all_elastic_node_stop(es_config=self.es_config)

    # 운영중인 모든 elastic node를 close
    def es_all_service_start(self):
        ServerInfo.all_elastic_node_start(es_config= self.es_config)

    # 운영중인 모든 kibana node를 run
    def kibana_all_service_close(self):
        print (self.es_config)
        ServerInfo.all_kibana_node_stop(es_config=self.es_config)

    # 운영중인 모든 kibana node를 close
    def kibana_all_service_start(self):
        ServerInfo.all_kibana_node_start(es_config=self.es_config)

"""
if __name__ == "__main__":
    esNode = EsControl()
    #esNode.es_all_service_close()
    #esNode.es_all_service_start()
    esNode.kibana_all_service_close()"""