import yaml
import os
import subprocess as sp
import requests
from esProj.esSShRet import EsSShRet

CATEGORY = ["elastic", "kibana"]

class ServerInfo:

    @classmethod
    def get_config(cls):
        """
        :param:
        :return:
        """
        #elk_conn_path = "../esProj/serverConfig/info.yml"
        elk_conn_path = "/Users/kimjunhyeon/PycharmProjects/stu_proj_elastic/esProj/serverConfig/info.yml"
        response = os.path.isfile(elk_conn_path)
        if response:
            with open(elk_conn_path, "r", encoding="utf-8") as fr:
                es_info = yaml.safe_load(fr)
                fr.close()
            return {"result": True, "data": es_info}
        else:
            return {"result": False, "data": None}


    # 서버가 살아 있는지 확인하자 ( by ping )
    @classmethod
    def is_server_alive(cls, es_config):
        """
        :param es_config:
        :return:
        """
        for c in CATEGORY:
            elastic_process = dict(es_config[c])
            for k in elastic_process.keys():
                status, result = sp.getstatusoutput("ping -c1 " + str(elastic_process[k]["server"]))
                if status == 0:
                    elastic_process[k]["isServerAlive"] = True
                else:
                    elastic_process[k]["isServerAlive"] = False

    #
    @classmethod
    def is_service_alive(cls, es_config):
        """
        :param es_config:
        :return:
        """
        for c in CATEGORY:
            elastic_process = dict(es_config[c])
            for k in elastic_process.keys():
                sess = requests.Session()

                req_url= "http://{server_}:{port_}".format(server_ = elastic_process[k]["server"],
                                                           port_   = elastic_process[k]["port"])

                try:

                    html = sess.get(req_url)

                    if html.status_code == 200 and html.ok:
                        elastic_process[k]["isServiceAlive"] = True
                    else:
                        elastic_process[k]["isServiceAlive"] = False

                except requests.exceptions.ConnectionError as err:
                    print(err)
                    elastic_process[k]["isServiceAlive"] = False
                    sess.close()
                finally:
                    sess.close()


    # 운영중인 elastic node 를 모두 닫는다.
    @classmethod
    def all_elastic_node_stop(cls, es_config):
        """
        :param es_config:
        :return:
        """
        for k in es_config["elastic"].keys():
            ##
            if es_config["elastic"][k]["isServiceAlive"]:
                sshObj = EsSShRet.ret_es_client_node(es_node=es_config["elastic"][k])
                ## 명령 송신
                stdin, stdout, stderr = sshObj.exec_command("jps")
                lines = stdout.readlines()
                if lines:
                    response = "".join(lines).rstrip("\n").split("\n")
                    response = {y[1]: y[0] for y in [x.split(" ") for x in response]}
                    if "Elasticsearch" in [ t for t in response.keys() ]:
                        ## 명령 송신
                        stdin, stdout, stderr = sshObj.exec_command("kill -9 {}".format(response["Elasticsearch"]))
                        es_config["elastic"][k]["isServiceAlive"] = False
                sshObj.close()


    # 운영중인 elastic node 를 모두 open
    @classmethod
    def all_elastic_node_start(cls, es_config):
        """
        :param es_config:
        :return:
        """
        for k in es_config["elastic"].keys():
            ##
            if not es_config["elastic"][k]["isServiceAlive"]:
                print("call")
                sshObj = EsSShRet.ret_es_client_node(es_node=es_config["elastic"][k])
                ## 명령 송신
                command = "nohup " + es_config["elastic"][k]["runPath"] + "/elasticsearch > /dev/null 2>&1 &"
                stdin, stdout, stderr = sshObj.exec_command(command)
                es_config["elastic"][k]["isServiceAlive"] = True
                sshObj.close()
            else:
                print("이미 동작중입니다.")


    # 운영중인 kibana node 를 모두 open
    @classmethod
    def all_kibana_node_start(cls, es_config):
        for k in es_config["kibana"].keys():
            ##
            if not es_config["kibana"][k]["isServiceAlive"]:
                print("kibana run call")
                sshObj = EsSShRet.ret_es_client_node(es_node=es_config["kibana"][k])
                ## 명령 송신
                command = "nohup " + es_config["kibana"][k]["runPath"] + "/kibana > /dev/null 2>&1 &"
                stdin, stdout, stderr = sshObj.exec_command(command)
                es_config["kibana"][k]["isServiceAlive"] = True
                print("{} kibana process open".format(k))
                sshObj.close()
            else:
                print("이미 동작중입니다.")


    # 운영중인 kibana node 를 모두 stop
    @classmethod
    def all_kibana_node_stop(cls, es_config):
        ##
        for k in es_config["kibana"].keys():
            if es_config["kibana"][k]["isServiceAlive"]:
                sshObj = EsSShRet.ret_es_client_node(es_node=es_config["kibana"][k])
                ## 명령 송신
                stdin, stdout, stderr = sshObj.exec_command("netstat -pln | grep 5601")

                lines = stdout.readlines()
                if lines:
                    response = "".join(lines).rstrip("\n")
                    response = response.split(" ")
                    response = [x for x in response if x != ''][6]
                    kibana_process_id = response.split("/")[0]
                    ## 명령 송신
                    stdin, stdout, stderr = sshObj.exec_command("kill -9 {}".format(kibana_process_id))
                    es_config["kibana"][k]["isServiceAlive"] = False
                    print("{} kibana process close".format(k))
                    sshObj.close()
            else:
                print("이미 동작하지 않는 프로세스 입니다.")