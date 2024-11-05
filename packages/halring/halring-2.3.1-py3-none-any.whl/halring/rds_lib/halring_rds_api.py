import os
import sys
import time
import rsa
import base64
import requests
import json
PUBLIC_KEY = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCDmmoJymMvEBb/YM9n4lSi5IMoBID764l9EtL8ogIK7VeFlUoAXGoRnJAE87LzH4p5QSHgmZJUiZLlmcUF+ujvhC8VTUgUiWuxOmhi6hHnp9rj+O+ePK2RH7QlbVR2X/5pfHaunJrqf43QVZyTECNYQ10WW0+z5N8f21OL9EDC2wIDAQAB"
HASH_KEY = "wedr3"


class RdsApiUtil(object):
    def __init__(self, api_url, user, api_secret, rds_id):
        self._api_url = api_url
        self._user = user
        self._api_secret = api_secret
        self._rds_id = rds_id

    def getPreToken(self, user, secretKey):
        hashKey = HASH_KEY
        publicKey = PUBLIC_KEY
        t = time.time()
        nowTime = str(int(round(t * 1000)))
        message = user + '&' + secretKey + '&' + nowTime + '&' + hashKey
        crypto = self.rsaEncrypt(message, publicKey)
        return str(crypto, "UTF-8")

    def rsaEncrypt(self, message, key):
        key = self.str2key(key)
        modules = int(key[0], 16)
        exponent = int(key[1], 16)
        rsaPubkey = rsa.PublicKey(modules, exponent)
        crypto = rsa.encrypt(message.encode(), rsaPubkey)
        b64str = base64.b64encode(crypto)
        return b64str

    @staticmethod
    def str2key(s):
        # 对字符串解码
        b_str = base64.b64decode(s)

        if len(b_str) < 162:
            return False

        hex_str = ''

        # 按位转换成16进制
        for x in b_str:
            h = hex(x)[2:]
            h = h.rjust(2, '0')
            hex_str += h

        # 找到模数和指数的开头结束位置
        m_start = 29 * 2
        e_start = 159 * 2
        m_len = 128 * 2
        e_len = 3 * 2

        modulus = hex_str[m_start:m_start + m_len]
        exponent = hex_str[e_start:e_start + e_len]

        return modulus, exponent

    def sub_create_backup(self, db_name, backup_type, retention_days, is_alldbs):
        pre_token = self.getPreToken(self._user, self._api_secret)

        url = self._api_url + "rds/backup/create"
        querystring = {
            "dbs": db_name,
            "rdsId": self._rds_id,
            "backupType": backup_type,
            "fileRetentionDays": retention_days,
            "isalldbs": is_alldbs}

        payload = ""
        headers = {
            'preToken': pre_token,
            'cache-control': "no-cache",
        }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        return response

    def sub_list_db_all_backup(self, db_name, is_alldbs):
        """
        :param db_name:数据库名字
        :param is_alldbs:是否为全部数据库,0:否,1:是
        :return: response
        """

        pre_token = self.getPreToken(self._user, self._api_secret)

        url = self._api_url + "rds/recovery/points"

        querystring = {
            "rdsId": self._rds_id,
            "dbs": db_name,
            "isalldbs": is_alldbs}

        payload = ""
        headers = {
            'preToken': pre_token,
            'cache-control': "no-cache"
        }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        return response

    def sub_create_recovery(self, db_name, recovery_id, isalldbs):

        pre_token = self.getPreToken(self._user, self._api_secret)

        url = self._api_url + "rds/recovery/create"

        querystring = {
            "rdsId": self._rds_id,
            "pointId": recovery_id,
            "isalldbs": isalldbs,
            "dbs": db_name
        }

        payload = ""
        headers = {
            'preToken': pre_token,
            'cache-control': "no-cache",
        }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        return response

    def sub_handle_rds_response(self, request_response):
        try:
            response_status = request_response.raw.status
            response_data = json.loads(request_response.text)

            if str(response_status) == "200":
                # 成功
                return_dict_status = True
            else:
                # 不成功
                return_dict_status = False
            returndict = {
                "status": return_dict_status,
                "value": response_data
            }
            return returndict
        except Exception as e:
            print(e)

    def create_backup(self, db_name, backup_type="0", retention_days="7", is_alldbs="0"):
        """ 创建备份
        :param db_name: 数据库名字
        :param backup_type: 0为完整备份,1为增量备份,2为完整备份且备份binlog
        :param retention_days: 备份留存天数,默认为7天
        :param is_alldbs: 是否为全部数据库,0:否,1:是
        :return: status:True/False,value:json.loads(response.text)
        """

        res = self.sub_create_backup(db_name, backup_type, retention_days, is_alldbs)
        result = self.sub_handle_rds_response(res)
        return result

    def list_db_all_backup(self, db_name, is_alldbs="0"):
        """  列出数据库所有备份
        :param db_name:数据库名字,不指定时填"",代表查询所有数据库
        :param is_alldbs: 是否为全部数据库,0:否,1:是
        :return: status:True/False,value:json.loads(response.text)
        """
        res = self.sub_list_db_all_backup(db_name, is_alldbs)
        result = self.sub_handle_rds_response(res)
        return result

    def create_recovery(self, db_name, recovery_id, isalldbs="0"):
        """
        创建备份
        :param db_name:
        :param recovery_id:
        :param isalldbs:
        :return:
        """
        res = self.sub_create_recovery(db_name, recovery_id, isalldbs)
        result = self.sub_handle_rds_response(res)
        return result


if __name__ == '__main__':
    pass
    # user = "ygong_uums"
    # apisecret = "35ccbe94-f528-4f0f-86af-bb816056e15f"
    # rdsid = "295"
    #
    # rds_util = RdsApiUtil("http://10.112.4.161:5526/api/", user, apisecret, rdsid)
    # # a=rds_util.create_backup("fxc")
    #
    # print(rds_util.create_recovery("fxctest", "55364", "0"))
