import requests
import json

class QueryResultItem:
    type=""
    value=""
    def __init__(self,type,value):
        self.type=type
        self.value=value
class gStoreCloud:
    api_url="http://cloud.gstore.cn/api"
    api_key=""
    api_secret=""

    def __init__(self,api_key,api_secret,api_url="http://cloud.gstore.cn/api"):
        self.api_key=api_key
        self.api_secret=api_secret
        self.api_url=api_url

    def postData(self,data):
        data_json = json.dumps(data)  # dumps：将python对象解码为json数据
        headers = {'content-type': 'application/json;charset=UTF-8'}
        # 发送POST请求
        response = requests.post(self.api_url, data=data_json, headers=headers)
        json_result = json.loads(response.text)
        return json_result
    def showDB(self):

        # 表单数据
        data = {
            'action':'showDB',
            'accesskeyid': self.api_key,
            'access_secret': self.api_secret
        }
        result=self.postData(data=data)
        return result


    def monitorDB(self,db_name):
        # 表单数据
        data = {
            'action': 'monitorDB',
            'dbName':db_name,
            'accesskeyid': self.api_key,
            'access_secret': self.api_secret
        }
        result = self.postData(data=data)
        return result

    def queryDB(self,db_name,sparql):
        data = {
            'action': 'queryDB',
            'dbName': db_name,
            'accesskeyid': self.api_key,
            'access_secret': self.api_secret,
            'sparql':sparql
        }
        result = self.postData(data=data)
        return result

if __name__ == '__main__':
    api=gStoreCloud("a681475ce81611e9abc600163e08435e","a6814763e81611e9abc600163e08435e")
    result=api.showDB()
    print(json.dumps(result,indent=4,ensure_ascii=False))

