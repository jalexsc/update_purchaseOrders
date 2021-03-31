import argparse
import pathlib
import json
import requests
import sys
from requests.exceptions import HTTPError
import time

#from folioclient.FolioClient import FolioClient

class backup:
    def __ini__(path,x_okapi_url, x_okapi_tenant, x_okapi_token):
        x_okapi_url = x_okapi_url
        x_okapi_tenant = x_okapi_tenant
        x_okapi_token = x_okapi_token
        content_type = "application/json"
        print('initializing Backup')
        #self.user = user
        #self.password = password
        #self.x_okapi_version = x-okapi-version
        #self.x_okapi_release = x-okapi-release
        #self.x_okapi_status = x-okapi-status

    def make_get(pathPattern,okapi_url, okapi_tenant, okapi_token,json_file):
        try:
            pathPattern=pathPattern
            okapi_url=okapi_url
            json_file=json_file
            okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
            #username="folio"
            #password="Madison"
            #payload = {'username': username, 'password': password}
            length="9999"
            #typein="General note Orders"
            ##fc="&metadata.createdByUserId='2bd750b9-1362-4807-bd73-2be9d8d63436'"
            start="0"
            paging_q = f"?limit={length}&query=workflowStatus=Pending"
            #paging_q = f"?limit={length}#&offset={start}"
            #paging_q = f"/notes?query=type=="General note Orders""
            #paging_q = f"?limit={length}&query=type=={typein}"
            #paging_q = f"?limit={length}"
            path = pathPattern+paging_q
            #data=json.dumps(payload)
            url = okapi_url + path
            req = requests.get(url, headers=okapi_headers,timeout=40)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))            
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
        except KeyboardInterrupt:
            print("Someone closed the program")
        else:
            if req.status_code != 201:
                print(req)
                print(req.encoding)
                #print(req.text)
                print(req.headers)
                if req.status_code==200:
                    archivo=open(json_file, 'w',encoding='utf8')
                    json_str = json.loads(req.text)
                    #total_recs = int(json_str["totalRecords"])
                    archivo.write(json.dumps(json_str, indent=2))
                    #archivo.write(json.dumps(json_str)+"\n")
                    #print('Datos en formato JSON',json.dumps(json_str, indent=2))
                    archivo.close()
                    print('Success!')
                elif req.status_code==201:
                    print(req.text) 
                elif req.status_code==500:
                    print(req.text)
                elif req.status_code==502:
                    print(req.text)
                elif req.status_code==504:
                    print(req.text)
                elif req.status_code==403:
                    print(req.text)
                    
    def make_get_and_put(pathPattern,okapi_url, okapi_tenant, okapi_token,json_file,schname,workflowStatusTochange,client):
        try:
            pathPattern=pathPattern
            idRecord=""
            okapi_url=okapi_url
            json_file=json_file
            okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
            length="9999"
            start="0"
            paging_q = f"?limit={length}&query=workflowStatus=Pending"
            path = pathPattern+paging_q
            #data=json.dumps(payload)
            url = okapi_url + path
            req = requests.get(url, headers=okapi_headers,timeout=40)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))            
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
        except KeyboardInterrupt:
            print("Someone closed the program")
        else:
            if req.status_code != 201:
                print(req)
                print(req.encoding)
                #print(req.text)
                print(req.headers)
                if req.status_code==200:
                    json_str = json.loads(req.text)
                    total_recs = int(json_str["totalRecords"])
                    print('all look like good!\nRecords founds:'+str(total_recs))
                    countrecord=0
                    for recordtoUpdate in json_str[schname]:
                        print(recordtoUpdate)
                        countrecord=countrecord+1
                        idRecord=recordtoUpdate['id']
                        workflowStatus=recordtoUpdate['workflowStatus']
                        if workflowStatus=="Pending":
                            recordtoUpdate['workflowStatus']=workflowStatusTochange
                            #print("")
                            #print(recordtoUpdate)
                            tini = time.perf_counter()
                            backup.make_put(pathPattern,okapi_url,okapi_tenant,okapi_token,idRecord,recordtoUpdate,client)
                            tend = time.perf_counter()
                            print(str(countrecord)+" Record: "+str(idRecord)+f"({tini - tend:0.4f}) seconds")                            
                elif req.status_code==500:
                    print(req.text)
                elif req.status_code==502:
                    print(req.text)
                elif req.status_code==504:
                    print(req.text)
                elif req.status_code==403:
                    print(req.text)
                    
    def make_del(pathPattern,okapi_url, okapi_tenant, okapi_token,json_file, schema,client):
        try:
            countrecord=0
            countdel=0
            countnodel=0
            deletedRecords=open(client+"_"+schema+"_recordDeleted.txt", 'w')
            Recordsnodeleted=open(client+"_"+schema+"_record_to_delete_not_found.txt", 'w')
            pathPattern=pathPattern
            okapi_url=okapi_url
            json_file=json_file
            okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
            id=""
            paging_q="/"
            path = pathPattern+paging_q
            #data=json.dumps(payload)
            url = okapi_url + path
            d = open(json_file)
            data = json.load(d)
            tini=0
            for i in data[schema]:
                countrecord=countrecord+1
                id=i['id']
                #po=i['poNumber']
                #print("==================================")
                #print("Record no: "+str(countrecord)+" searching POnumber:"+str(po)+"            id:"+id)
                url = okapi_url + path+id
                tini = time.perf_counter()
                req = requests.delete(url, headers=okapi_headers,timeout=40)
                tend = time.perf_counter()
                #print(req.status_code)
                #print(req.headers)
                #print(req.text)
                if req.status_code==404:
                    print(str(countrecord)+" Record: "+str(id)+f" not found Deleting ({tini - tend:0.4f}) seconds")
                    Recordsnodeleted.write(str(id)+f"({tini - tend:0.4f}) seconds \n")
                    countnodel=+1
                    print("==================================")
                elif req.status_code==204:
                    print(str(countrecord)+" Record: "+str(id)+f" has been deleted (time in {tini - tend: 0.4f}) seconds")
                    deletedRecords.write(str(id)+f" ({tini - tend: 0.4f}) seconds\n")
                    countdel=+1
                    print("==================================")
                elif req.status_code==503:
                    print(req.text)
                    Recordsnodeleted.write(str(id)+f"({tini - tend:0.4f}) seconds \n")
                    time.sleep(60) # Sleep for 3 seconds
                elif req.status_code==504:
                    print(req.text)
                    Recordsnodeleted.write(str(id)+f"({tini - tend:0.4f}) seconds \n")
                    time.sleep(60) # Sleep for 3 seconds
            deletedRecords.close()
        
        except ValueError:
            print("General Error on DEL")
        #(pathPattern,okapi_url,okapi_tenant,okapi_token,idRecord,recordtoUpdate)
    def make_put(pathPattern,okapi_url, okapi_tenant,okapi_token,idrec,i,client):
        try:
            rec={}
            countrecord=0
            pathPattern="/orders/composite-orders/{id}"
            pathPattern=pathPattern.replace("{id}", idrec)
            okapi_url=okapi_url
            j_content=i
            okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
            id=""
            path = pathPattern
            #print("Record no: "+str(countrecord))
            url = okapi_url + path
            tini = time.perf_counter()
            print(j_content)
            req = requests.put(url, json=j_content, headers=okapi_headers,timeout=10)
            print(req.status_code)
            print(req.text)
            tend = time.perf_counter()
            client="folijet"
            errorMessages(str(idrec),req.status_code,req.text,tini,tend,client+"POST_logFileName.txt")
        except ValueError:
            print("General Error on POST:"+req.text+"\nError Number:  "+req.status_code)

    def make_post(pathPattern,okapi_url, okapi_tenant, okapi_token,json_file, schema,client):
        try:
            rec={}
            countrecord=0
            pathPattern=pathPattern
            okapi_url=okapi_url
            json_file=json_file
            okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
            id=""
            path = pathPattern
            url = okapi_url + path

            with open(json_file) as data:
                for line in data:
                    line= data.readline()
                    line=line.replace("\n","")
                    #print(line)
                    j_content =json.loads(line)
                    countrecord=countrecord+1
                    #print("Record no: "+str(countrecord))
                    url = okapi_url + path
                    tini = time.perf_counter()
                    req = requests.post(url, json=j_content, headers=okapi_headers,timeout=10)
                    print(req.status_code)
                    print(req.text)
                    tend = time.perf_counter()
                    errorMessages(str(countrecord),req.status_code,req.text,tini,tend,client+"POST_logFileName.txt")
        except ValueError:
            print("General Error on POST:"+req.text+"\nError Number:  "+req.status_code)
            
    def make_post_login(pathPattern,okapi_url, okapi_tenant, okapi_user,okapy_password, schema,client):
        try:
            u=okapi_user
            p=okapy_password
            rec={}
            countrecord=0
            pathPattern=pathPattern
            okapi_url=okapi_url
            userpass=f"username={u}&password={p}"
            okapi_headers = {"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
            path = pathPattern
            url = okapi_url + path
            tini = time.perf_counter()
            req = requests.post(url, data=userpass, headers=okapi_headers,timeout=10)
            print(req.status_code)
            print(req.text)
            okapi_token=req.text
            tend = time.perf_counter()
            errorMessages(str(countrecord),req.status_code,req.text,tini,tend,client+"POST_logFileName.txt")
        except ValueError:
            print("General Error on POST:"+req.text+"\nError Number:  "+req.status_code)
            
    def filebyline(filetoformat,schema,client):
        try:
            f = open(filetoformat)
            archivo=open(client+"_"+str(filetoformat)+"byline.json", 'w', encoding='utf8')
            # returns JSON object as
            # a dictionary
            data = json.load(f)
            # Iterating through the json
            # list
            for i in data[schema]:
                print(i)
                a_line=str(i)
                archivo.write(a_line+"\n")
            print("file by line, ready")
            # Closing file
            f.close()
        except: 
            print("OOPS!! Error creating the File by line")
            
def errorMessages(recNum,Errvalue,contentRequest, tini,tend,logFileName):
    
    fileErrors= open(logFileName,"w")
    if Errvalue==400:
        print("Record # "+recNum+f" Exist time ({tini - tend}) seconds")
        countnodel=+1
        #print("==================================")
        fileErrors.write("Record # "+recNum+f"time ({tini - tend}) seconds"+"\n"+contentRequest+" Error value: "+str(Errvalue))
    elif Errvalue==404:
        print("Record # "+recNum+f" time ({tini - tend}) seconds"+"\nERROR "+contentRequest+" Error value: "+str(Errvalue))                     
        countnodel=+1
        print("==================================")
        fileErrors.write("Record # "+recNum+f" time ({tini - tend}) seconds"+"\n"+contentRequest+" Error value: "+str(Errvalue))
    elif Errvalue==422:
            print("Record # "+recNum+f" time ({tini - tend}) seconds"+"\nERROR "+contentRequest+" Error value: "+str(Errvalue))                     
            countnodel=+1
            fileErrors.write("Record # "+recNum+f" time ({tini - tend}) seconds"+"\n"+contentRequest+" Error value: "+str(Errvalue))
            print("==================================")
    elif Errvalue==201:
        print("Record # "+recNum+f" time ({tini - tend}) seconds")                         
        countnodel=+1
        #print("==================================")
        fileErrors.write("Record # "+recNum+f" time ({tini - tend}) seconds"+"\n"+contentRequest)
    elif Errvalue==204:
        print("Record # "+recNum+f" time ({tini - tend}) seconds")                          
        countdel=+1
        #print("==================================")
        fileErrors.write("Record # "+recNum+f" time ({tini - tend}) seconds"+"\n"+contentRequest)
    elif Errvalue==503:
        print("Record # "+recNum+f"time ({tini - tend}) seconds"+"\n ERROR"+contentRequest)                          
        time.sleep(60) # Sleep for 3 seconds
        fileErrors.write("Record # "+recNum+f" time ({tini - tend}) seconds"+"\nERROR "+contentRequest+" Error value: "+str(Errvalue))
        print("==================================")
    elif Errvalue==504:
        print("Record # "+recNum+f" time ({tini - tend}) seconds"+"\n ERROR"+contentRequest)  
        fileErrors.write("Record # "+recNum+f"time ({tini - tend}) seconds"+"\nERROR "+contentRequest+" Error value: "+str(Errvalue))
        time.sleep(60) # Sleep for 3 seconds
        print("==================================")
    else:
        print("Record # "+recNum+f" time ({tini - tend}) seconds"+"\n ERROR"+contentRequest+" Error value"+str(Errvalue))  
        fileErrors.write("Record # "+recNum+f" time ({tini - tend}) seconds"+"\nnERROR "+contentRequest+" Error value: "+str(Errvalue))
        print("==================================")

    
                            
def Clients():
    try:
        # Opening JSON file
        dic=[]
        f = open("okapi_customers.json",)
        data = json.load(f)
        for i in data['okapi']:
            a_line=str(i)
            dic.append(i['name'])#+"- Version:"+['x-okapi-version']+"-Release: "+['x-okapi-release'])
        f.close()
        return dic
    except: 
        print("OOPS!! General error occurred in Clients")
        
def schemas():
        # Opening JSON file
        dic=[]
        f = open("setting_data.json",)
        data = json.load(f)
        for i in data['settings']:
            a_line=str(i)
            dic.append(i['name'])#+"- Version:"+['x-okapi-version']+"-Release: "+['x-okapi-release'])
        f.close()
        return dic

def get_one_schema(code_search):
    valor=[]
    try:
        #valor="0"
        f = open("setting_data.json",)
        data = json.load(f)
        for i in data['settings']:
            a_line=str(i)
            if i['name'] == code_search:
            #if (a_line.find(code_search) !=-1):
                valor.append(i['pathPattern'])
                valor.append(i['name'])
                break
        f.close()
        return valor
    except ValueError:
        print("schema does not found")
        return 0

def get_all_schemas(self,code_search):
        f = open("setting_data.json",)
        data = json.load(f)
        for i in data['settings']:
            valor=i['path']
            break
        f.close()
        return valor

def SearchClient(code_search):
        # Opening JSON file
        dic =dic= {}
        f = open("okapi_customers.json",)
        data = json.load(f)
        for i in data['okapi']:
            a_line=str(i)
            if i['name'] == code_search:
            #if (a_line.find(code_search) !=-1):
                 dic=i
                 del dic['name']
                 del dic['user']
                 del dic['password']
                 del dic['x_okapi_version']
                 del dic['x_okapi_status']
                 del dic['x_okapi_release']
                 break
        f.close()
        return dic
    
def main(opt):
    try:
        okapi=""
        tenant=""
        token=""
        filename=""
        client = {}
        print(Clients())
        print("Enter Customer name:")
        cuts_name = str(input())
        client=SearchClient(cuts_name)
        if len(client)>0:
            ale=str(cuts_name)
            okapi=str(client.get('x_okapi_url'))
            tenant=str(client.get('x_okapi_tenant'))
            token=str(client.get('x_okapi_token'))
            print(schemas())
            print("Enter schema name:")
            sn = input()
            print("searching the path in setting file...")
            schema_name=str(sn)
            paths=get_one_schema(schema_name)
            if len(paths)>0:
                print("the path has been found "+schema_name)
                pathschema=paths[0]
                nameschema=paths[1]
                if opt==1:
                    tic = time.perf_counter()
                    filename=str(ale)+"_"+str(sn)+".json"
                    a=backup()
                    backup.make_get(pathschema,okapi,tenant,token,filename)
                    toc = time.perf_counter()
                    print(f"Getting time in {toc - tic:0.4f} seconds")
                    backup.filebyline(filename,nameschema,ale)
                elif opt==2:
                    tic = time.perf_counter()
                    filename = str(cuts_name+"_"+schema_name+".json")
                    print("Name file to upload: "+filename)
                    bbb = input()
                    a=backup()
                    backup.make_post(pathschema,okapi,tenant,token,filename,nameschema,ale)
                    toc = time.perf_counter()
                    print(f"Getting time in {toc - tic:0.4f} seconds hours")
                elif opt==4:
                    tic = time.perf_counter()
                    filename=ale+"_"+str(sn)+".json"
                    print("is it the JSON file name:"+filename+" ?")
                    a=backup()
                    backup.make_del(pathschema,okapi,tenant,token,filename,nameschema,ale)
                    toc = time.perf_counter()
                    toctic=(((toc - tic)/60)/60)
                    print(f"Deleting time in {toc - tic:0.4f} seconds {toctic} hours")
                elif opt==5:
                    print("User:")
                    user_validation = input()
                    print("Password:")
                    password_validation = input()
                    a=backup()
                    #make_post_login(pathPattern,okapi_url, okapi_tenant, okapi_user,okapy_password, schema,client):
                    backup.make_post_login(pathschema,okapi,tenant,user_validation,password_validation,nameschema,ale)
                elif opt==6:
                    tic = time.perf_counter()
                    filename=str(ale)+"_"+str(sn)+".json"
                    workflowStatusToupdate="Open"
                    a=backup()
                    backup.make_get_and_put(pathschema,okapi,tenant,token,filename,schema_name,workflowStatusToupdate,client)
                    toc = time.perf_counter()
                    print(f"Getting time in {toc - tic:0.4f} seconds")
                    #backup.filebyline(filename,nameschema,ale)
                    
            else:
                print("the path has not been found "+schema_name)
                sys.exit()
        else:
            print("Customer does not exist in the okapi file, try again the okapi customer should be include in okapi file")
    except ValueError:
        print("Main Error"+str(ValueError))
        
#===================MAIN==================================
if __name__ == "__main__":
    """This is the Starting point for the script"""
    option=""
    print("MENU UTIL")
    print("1. GET"+"\n"+"2. POST"+"\n"+"3.PUT"+"\n"+"4.DEL"+"\n"+"5.GET TOKEN"+"\n"+"6.UPDATE ORDERS FROM PENDING TO OPEN")
    option = int(input())
    main(option)
