from configparser import ConfigParser
from pip._vendor.distlib.compat import raw_input
import json
import hashlib

if __name__ == "__main__":

    def read_configfile():
        cfg = ConfigParser()
        cfg.read('config.ini')
        users = []  # lists of users.index: 0-username 1-password 2-usertype 3-privilagelevel
        for section in cfg.sections():
            users.append(cfg.items(section))
        return users

    user_list = read_configfile()

    def write_to_configfile():
        username = raw_input('username: ')
        password = raw_input('password: ')
        usertype = raw_input('user type(patient/clerk/nurse/doctor/surgeon): ')

        hashpassword = hashlib.md5(password.encode()).hexdigest()

        if(usertype=="patient"):
            privlevel = "userlevel1"
        elif(usertype=="clerk"):
            privlevel = "userlevel2"
        elif (usertype == "nurse"):
            privlevel = "userlevel3"
        elif (usertype == "doctor"):
            privlevel = "userlevel4"
        elif (usertype == "surgeon"):
            privlevel = "userlevel5"
        else:
            print("invalid user type")
            return 0

        cfg_rd = ConfigParser()
        cfg_rd.read('config.ini')
        index = len(cfg_rd.sections()) + 1
        section_name = 'section' + str(index)

        cfg_wrt = ConfigParser()
        cfg_wrt[section_name] = {'username': username, 'password': hashpassword, 'usertype': usertype, 'privilagelevel': privlevel}
        with open('config.ini', 'a') as configfile:
            cfg_wrt.write(configfile)

    def get_user_privilege_level(username, password):
        hashpassword = hashlib.md5(password.encode()).hexdigest()
        for user in user_list:
            list_username = user[0][1]
            list_password = user[1][1]
            if(username==list_username and hashpassword==list_password):
                privlevel = user[3][1]
                privilagelevel = privlevel
                return privilagelevel

    def read_datafile(username, password):
        privilagelevel = get_user_privilege_level(username, password)
        if(privilagelevel==None):
            print("invalid username/password")
        else:
            if(privilagelevel=="userlevel1"):
                print("patient privilage level does not have access to read data")
                return 0
            elif(privilagelevel=="userlevel2"):
                read_access = ["datalevel1", "datalevel2"]
            elif(privilagelevel=="userlevel3"):
                read_access = ["datalevel1", "datalevel2", "datalevel3", "datalevel4"]
            elif (privilagelevel == "userlevel4"):
                read_access = ["datalevel1", "datalevel2", "datalevel3", "datalevel4"]
            elif (privilagelevel == "userlevel5"):
                read_access = ["datalevel1", "datalevel2", "datalevel3", "datalevel4"]

            with open('datafile.json') as f:
                data = json.load(f)
                datatypes = ["personal details", "sickness details", "drug prescriptions", "lab test prescriptions"]
                for dtype in datatypes:
                    sensitivity_level = data[dtype]["sensitivitylevel"]
                    if (sensitivity_level in read_access):
                        print(dtype)
                        print(data[dtype]["data"])
                        # patient id as key and object of detalis/list of details as values
                        # personal details,sickness details - objects
                        # drug prescriptions,lab test prescriptions - lists

    def write_to_datafile(username, password):
        privilagelevel = get_user_privilege_level(username, password)
        if (privilagelevel == None):
            print("invalid username/password")
        else:
            if (privilagelevel == "userlevel1"):
                print("patient privilage level does not have access to write data")
                return 0
            elif (privilagelevel == "userlevel2"):
                write_access = ["datalevel1"]
            elif (privilagelevel == "userlevel3"):
                print("nurse privilage level does not have access to write data.you can only view data")
                return 0
            elif (privilagelevel == "userlevel4"):
                write_access = ["datalevel1", "datalevel2", "datalevel3"]
            elif (privilagelevel == "userlevel5"):
                write_access = ["datalevel1", "datalevel2", "datalevel3", "datalevel4"]

            with open('datafile.json') as f:
                data = json.load(f)
                datatypes1 = ["personal details", "sickness details"]  # data of these 2 have stored as objects
                for dtype in datatypes1:
                    sensitivity_level = data[dtype]["sensitivitylevel"]
                    if (sensitivity_level in write_access):
                        print(dtype)
                        print(read_datafile(username, password)[dtype])
                        option = input("to edit enter 1:")
                        if(option=="1"):
                            patient_id = 0
                            while(patient_id!=""):
                                patient_id = raw_input("patient id(type 0 to end): ")
                                if(patient_id=="0"):
                                    break
                                if(patient_id!=""):
                                    try:
                                        data[dtype]["data"][patient_id]
                                    except:
                                        data[dtype]["data"][patient_id] = {}
                                    if(dtype=="personal details"):
                                        print("enter details with values. ex:- name/Alan. Type 0 to end")
                                    else:
                                        print("enter details with values. ex:- disease/tb1. Type 0 to end")
                                    detail = 0
                                    while(detail!=""):
                                        try:
                                            key, value = raw_input("detail (format: type/value): ").split("/")
                                            data[dtype]["data"][patient_id][key] = value
                                        except:
                                            break
                datatypes2 = ["drug prescriptions", "lab test prescriptions"]  # data of these 2 have stored as lists
                for dtype in datatypes2:
                    sensitivity_level = data[dtype]["sensitivitylevel"]
                    if (sensitivity_level in write_access):
                        print(dtype)
                        print(read_datafile(username, password)[dtype])
                        option = input("to edit enter 1:")
                        if (option == "1"):
                            patient_id = 0
                            while (patient_id != ""):
                                patient_id = raw_input("patient id(type 0 to end): ")
                                if(patient_id=="0"):
                                    break
                                if (patient_id != ""):
                                    try:
                                        data[dtype]["data"][patient_id]
                                    except:
                                        data[dtype]["data"][patient_id] = []
                                    print("enter prescription values.Type 0 to end")
                                    value = 1
                                    while (value != 0):
                                        value = raw_input("value: ")
                                        if(value!=""):
                                            data[dtype]["data"][patient_id].append(value)
            with open('datafile.json', 'w') as fr:
                json.dump(data, fr, indent=2)

    print(" 1-register user  2-read medical data    3-write medical data")
    option = raw_input("select an option and enter 1/2/3 to process: ")
    if(option=="1"):
        write_to_configfile()
    elif(option=="2"):
        username = raw_input("enter username: ")
        password = raw_input("enter password: ")
        read_datafile(username, password)
    elif(option=="3"):
        username = raw_input("enter username: ")
        password = raw_input("enter password: ")
        write_to_datafile(username, password)





























