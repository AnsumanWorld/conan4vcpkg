import os,platform,sys,time,yaml
from colorama import init,Fore
import vcpkg_mgr
import conan_mgr
from conans import tools
init(autoreset=True)

class Vcpkgbin:
    _user_type="help"
    _valid_arg_status = False
    _vcpkg_path =os.path.normpath(os.getcwd())
    _port=[]
    _triplet=""
    _repository=""

    def __init__(self):
        self._user_type="help"
        self.validate_arg()
        if self._valid_arg_status == True:
            self._vcpkg = vcpkg_mgr.vcpkg_mgr(self._vcpkg_path)
            self._conan = conan_mgr.conan_mgr()

    def print_message(self,input_str,type="",term='\n'):
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        ENDC = '\033[0m'

        if type.lower() == 'warning':
            print(YELLOW + input_str,end=term)
        elif type.lower() == 'error':
            print(RED + input_str,end=term)
        elif type.lower() == 'success':
            print(GREEN + input_str,end=term)
        else:
            print(input_str,end=term)

    def help(self,info_type):
        if "help" in info_type:
            print("commands:")
            print("vcpkgbin download     downloading particular package")
            print("vcpkgbin search       search particular package in local or remote")
            print("vcpkgbin list  remote  <remote repository name>")
            print("vcpkgbin help topics  display list of help topics")
        elif "download" in info_type:
            print("vcpkgbin download <remote repository name> <port name> <triplet>")
            print("         - for downloading particular package")
        elif "list" in info_type:
            print("vcpkgbin list local")
            print("         - search for repository installed in local")
            print("vcpkgbin list local <triplet>")
            print("         - search for port installed in local")
            print("vcpkgbin list local <triplet> <port>")
            print("         - search ports of particular triplet installed in local")
            print("vcpkgbin list remote <remote repository name>")
            print("         - search for all packages of the particular repository installed in remote")
            print("vcpkgbin list remote <remote repository name> <triplet>")
            print("         - search for all the ports of the particular triplet of the particular repository in remote")
            print("vcpkgbin list remote <remote repository name> <port name>")
            print("         - search for port information of the particular port name of particular repository in remote")
            print("vcpkgbin list remote <remote repository name> <port name> <triplet>")
            print("         - search for port information of the particular portname and triplet of particular repository in remote")

    def validate_arg(self):
        argc = len(sys.argv)
        if argc >= 2:
            self._user_type = sys.argv[1]
            if "download" in self._user_type:
                if argc == 5:
                    self._repository=sys.argv[2]
                    self._port=sys.argv[3].split(" ")
                    self._triplet=sys.argv[4]
                    self._valid_arg_status = True
            elif "list" in self._user_type:
                if "local" == sys.argv[2]:
                    if argc == 3:
                        self._valid_arg_status = True
                    elif argc == 4:
                        self._triplet=sys.argv[3]
                        self._valid_arg_status = True
                    elif argc == 5:   
                        self._triplet=sys.argv[3]
                        self._port=sys.argv[4].split(" ")
                        self._valid_arg_status = True
                elif "remote" == sys.argv[2]:
                    if argc == 4:
                        self._repository=sys.argv[3]
                        self._valid_arg_status = True
                    elif argc == 5:
                        self._repository=sys.argv[3]
                        self._triplet=sys.argv[4]
                        self._valid_arg_status = True
                    elif argc == 6:
                        self._repository=sys.argv[3]
                        self._triplet=sys.argv[4]
                        self._port=sys.argv[5].split(" ")
                        self._valid_arg_status = True
            elif "help" in self._user_type:
                if argc== 3:
                    self.help(sys.argv[2])
                    self._valid_arg_status = True
            else:
                self._user_type = "help"
        else:
            self._valid_arg_status = False

        if self._valid_arg_status == False:
             self.help(self._user_type)

    def run(self):
        if self._valid_arg_status == True:
            if sys.argv[2] != "local":
                print("configuring conan please wait")
                self._conan.init_conan_setting()
                print("configuring conan completed")
            if self._user_type == "download":
                self.download()
            elif self._user_type == "list":
                self.list()

    def download_conan_pkg_info(self):
        download_recipe_template_file = self._vcpkg_path + os.sep + "conan_script" + os.sep + "conan_download_recipe_template.txt"
        download_recipe_gen_dir= self._vcpkg_path + os.sep + "Temp"
        package_info_file=download_recipe_gen_dir+ os.sep+ "packagelist.yml"
        if os.path.isfile(package_info_file )==True:
            os.system('del /Q %s' % package_info_file)
        self._conan.make_download_recipe(download_recipe_template_file,download_recipe_gen_dir,self._repository,".")
        self._conan.download(download_recipe_gen_dir,download_recipe_gen_dir,"info","info")
        status,remote_installed_data=self._conan.getdata_from_yml(package_info_file)
        return remote_installed_data

    def download_conan_pkg(self,repo,port,triplet):
        download_recipe_template_file = self._vcpkg_path + os.sep + "conan_script" + os.sep + "conan_download_recipe_template.txt"
        download_recipe_gen_dir= self._vcpkg_path + os.sep + "Temp"
        retcode=self._conan.make_download_recipe(download_recipe_template_file,temp_folder,repo,".")
        if retcode == 0:
            retcode=self._conan.download(temp_folder,temp_folder,port,triplet)
        return retcode

    def download(self):
        retcode = 0
        download_recipe_template_file = self._vcpkg_path + os.sep + "conan_script" + os.sep + "conan_download_recipe_template.txt" 
        installed_pkg_count=0
        conan_pkg_info=self.download_conan_pkg_info()
        if len(conan_pkg_info) != 0:
            for d_port in self._port:
                installed_pkg_list=self._vcpkg.get_installed_pkg_list()
                req_vcpkg_port_list=[]
                if self._repository in conan_pkg_info.keys() and self._triplet in conan_pkg_info[self._repository].keys() and d_port in conan_pkg_info[self._repository][self._triplet].keys() and 'Dependant' in conan_pkg_info[self._repository][self._triplet][d_port].keys():
                    req_vcpkg_port_list.append(d_port)
                    req_vcpkg_port_list.extend(conan_pkg_info[self._repository][self._triplet][d_port]['Dependant'])
                    self._conan.updatesetting("vcpkg_port",req_vcpkg_port_list,"vcpkg_triplet",[self._triplet])
                    for package in installed_pkg_list:
                        installed_port,installed_triplet=package.split(":")
                        if installed_port in req_vcpkg_port_list and installed_triplet == self._triplet:
                            req_vcpkg_port_list.remove(installed_port)

                    if len(req_vcpkg_port_list) == 0:
                        continue
                    index = 1
                    total_package=len(req_vcpkg_port_list) 
                    print("===============================================================")
                    for port in req_vcpkg_port_list:
                        self.print_message("downloading %s/%s: %s:%s please wait" % (index,total_package,port,self._triplet),"success",'\r')
                        retcode = self.download_conan_pkg(self._repository,port,self._triplet)
                        if retcode == 0:
                            self.print_message("downloading %s/%s: %s:%s is completed               " % (index,total_package,port,self._triplet),"success")
                            print("--configuring %s/%s: %s:%s Please wait..." % (index,total_package,port,self._triplet),end='\r')
                            status = self._vcpkg.load_conan_pkg(temp_folder,port,self._triplet) 
                            if status == True:
                                installed_pkg_count+=1
                                print("--configuring %s/%s: %s:%s is completed       " % (index,total_package,port,self._triplet))
                                self._vcpkg.update_installed_vcpkg(self._repository,[port],self._triplet,conan_pkg_info)
                            else:
                                print("--configuring %s/%s: %s:%s is failed          " % (index,total_package,port,self._triplet))
                        else:
                            self.print_message("fail to download %s/%s: %s:%s           " % (index,total_package,port,self._triplet),"error")
                        index+=1
                    print("===============================================================")
                else:
                    self.print_message("%s:%s not available in server" % (d_port,self._triplet),"error")
        else:
            self.print_message("no package available in server","error")

        if installed_pkg_count == 0:
            self.print_message("no package installed","error")


    def show_pkg(self,repo,triplet,port_list,pkg_data):
        if len(pkg_data) != 0:
            if triplet != "" and len(port_list) != 0 and repo in pkg_data.keys() and triplet in pkg_data[repo].keys():
                self.print_message(repo,"success")
                self.print_message("  " + triplet,"success")
                for port in port_list:
                    if port in pkg_data[repo][triplet].keys():
                        self.print_message("    " + port,"success")
                        for tag in pkg_data[repo][triplet][port]:
                            value = "      "+str(tag) +": "+ str(pkg_data[repo][triplet][port][tag])
                            self.print_message(value,"success")
            elif triplet!="" and len(port_list) == 0 and repo in pkg_data.keys() and triplet in pkg_data[repo].keys():
                    self.print_message(repo,"success")
                    self.print_message("  " + triplet,"success")
                    for tag in pkg_data[repo][triplet]:
                        value = "    "+str(tag)
                        self.print_message(value,"success")
            elif repo!="" and triplet=="" and len(port_list) == 0 and repo in pkg_data.keys():
                    self.print_message(repo,"success")
                    for tag in pkg_data[repo]:
                        value = "  "+str(tag)
                        self.print_message(value,"success")
            else:
                self.print_message("no entry found","error")
        else:
            self.print_message("no package found","error")

    def list(self):
        installed_port=[]
        if sys.argv[2] == "local":
            installed_port,installed_port_data =self._vcpkg.get_installed_pkg_data()
            self.show_pkg("local",self._triplet,self._port,installed_port_data)
        elif sys.argv[2] == "remote":
            print("collecting information from remote,please wait")
            conan_pkg_info=self.download_conan_pkg_info()
            self.show_pkg(self._repository,self._triplet,self._port,conan_pkg_info)

if __name__ == "__main__":
    os.system('echo "%s" > vcpkgbin.log' % sys.argv[0:])
    vcpkgbin_mgr=Vcpkgbin()
    temp_folder = vcpkgbin_mgr._vcpkg_path + os.sep+"Temp"
    os.makedirs(temp_folder, exist_ok=True)
    vcpkgbin_mgr.run()    
    os.system('rmdir /Q /S %s' % temp_folder)