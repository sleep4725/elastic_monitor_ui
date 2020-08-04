import paramiko

class EsSShRet():

    @classmethod
    def ret_es_client_node(cls, es_node):
        ret_cli = paramiko.SSHClient()
        ret_cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        ret_cli.connect(hostname   = es_node["server"],
                        port =22,
                        username = es_node["user"]["id"],
                        password = es_node["user"]["pw"])

        return ret_cli