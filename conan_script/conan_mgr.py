import os,platform,sys,yaml
from conans import tools

class conan_mgr:
    _workingpath= os.path.normpath(os.getcwd()) + os.sep + "conan_script" + os.sep + "config"

    def init_conan_setting(self):
        conan_setting_filename= self._workingpath + os.sep+ "settings.yml"
        if os.path.isfile(conan_setting_filename) == True:
            system('7z.exe a %s.zip %s\*' % (self._workingpath,self._workingpath))
            system('conan config install %s.zip' % self._workingpath)
            system('del /Q %s.zip' % self._workingpath)
        else:
             print("fail to update setting")

    def updatesetting(self,port_tag,port_value,triplet_tag,triplet_value):
        conan_setting_filename= self._workingpath + os.sep+ "settings.yml"
        conan_setting_content=""
        port_tag_value=['info']
        triplet_tag_value=['info']
        update = False
        if os.path.isfile(conan_setting_filename) == True:
            status,data = self.getdata_from_yml(conan_setting_filename)
            if 'vcpkg_port' in port_tag and port_tag in data.keys():
                port_tag_value = data[port_tag]
                if set(port_value).issubset(set(port_tag_value)) == False:
                    update = True
                    port_tag_value.extend(port_value)
            if 'vcpkg_triplet' in triplet_tag and triplet_tag in data.keys():
                triplet_tag_value = data[triplet_tag]
                if set(triplet_value).issubset(set(triplet_tag_value)) == False:
                    update = True
                    triplet_tag_value.extend(triplet_value)

            if update == True:
                conan_setting_content += "vcpkg_port: %s\r\n" % port_tag_value
                conan_setting_content += "vcpkg_triplet: %s\r\n" % triplet_tag_value
                tools.save(conan_setting_filename,conan_setting_content)
                system('7z.exe a %s.zip %s\*' % (self._workingpath,self._workingpath))
                system('conan config install %s.zip' % self._workingpath)
                system('del /Q %s.zip' % self._workingpath)
        else:
             print("fail to update setting")

    def parse_repositoryname(self,repository):
        valid_repository = False
        packagename=""
        packageversion=""
        user=""
        channel=""
        findindex = repository.find("/")
        if findindex != -1:
            packagename,str_list,channel = repository.split("/")
            findindex = str_list.find("@")
            if findindex != -1:
                valid_repository = True
                packageversion,user = str_list.split("@")
        return valid_repository,packagename,packageversion,user,channel

    def create(self,upload_recipe_gen_dir,repository,port,triplet):
        status,repo_name,repo_version,user_name,channel_name = self.parse_repositoryname(repository)
        if status == True and repo_name!="" and repo_version != "" and user_name !="" and channel_name != "":
            ret_code=system('conan create -c %s %s/%s -s vcpkg_port=%s -s vcpkg_triplet=%s -k' % (upload_recipe_gen_dir,user_name,channel_name,port,triplet))
        else:
            print("invalid repository")
            ret_code = 1
        return ret_code

    def download(self,download_recipe_gen_dir,download_path,port,triplet):
        ret_code=system('conan install %s --install-folder %s -s vcpkg_port=%s -s vcpkg_triplet=%s --build=never -u' % (download_recipe_gen_dir,download_path,port,triplet))
        os.system('del /Q %s\*.txt' % download_path)        
        return ret_code

    def make_download_recipe(self,download_recipe_template,download_recipe_gen_dir,repository_name,download_folder):
        retcode = 0
        download_recipe_gen_file = download_recipe_gen_dir + os.sep + "conanfile.txt"
        if os.path.isfile(download_recipe_template) == True:
            download_recipe_template_content=tools.load(download_recipe_template)
            download_recipe_content = download_recipe_template_content % (repository_name,download_folder)
            tools.save(download_recipe_gen_file,download_recipe_content)
            if os.path.isfile(download_recipe_gen_file) == False:
                retcode = 1
                system('echo "%s is not created"' % download_recipe_gen_file)
        else:
            retcode = 1
            system('echo %s "is not found"' % download_recipe_template)
        return retcode

    def getdata_from_yml(self,filename):
        data = {}
        status=False
        if os.path.isfile(filename )==True:
            status = True
            content=tools.load(filename)
            data=yaml.load(content)
        return status,data

    def get_current_repository(self,temp_folder):
        package_search_file =temp_folder + os.sep+"conan_search.txt"
        os.system('conan search > %s' % (package_search_file))
        lines = tuple(open(package_search_file, 'r'))
        installed_list=[]
        for line in lines:
            status,repo_name,repo_version,user_name,channel_name = self.parse_repositoryname(line)
            if status == True and repo_name!="" and repo_version != "" and user_name !="" and channel_name != "":
                installed_list.append(line[0:-1])
        return installed_list

    def get_installed_pkg_data(self,temp_folder,repository):
        package_search_file =temp_folder + os.sep+"conan_search.txt"
        os.system('conan search %s > %s' % (repository,package_search_file))
        lines = tuple(open(package_search_file, 'r'))
        cur_package_id=""
        cur_port=""
        cur_triplet=""
        installed_list=[]
        for line in lines:
            find_package_index = line.find("Package_ID: ")
            if find_package_index != -1:
                find_package_index += len("Package_ID: ")
                cur_package_id = line[find_package_index:-1]
            find_port_index = line.find("vcpkg_port: ")
            if find_port_index != -1:
                find_port_index += len("vcpkg_port: ")
                cur_port = line[find_port_index:-1]
            find_triplet_index = line.find("vcpkg_triplet: ")
            if find_triplet_index != -1:
                find_triplet_index += len("vcpkg_triplet: ")
                cur_triplet = line[find_triplet_index:-1]
                installed_list.append(cur_package_id+":"+cur_port+":"+cur_triplet)
        return installed_list

def system(command):
    if os.path.isfile("vcpkgbin.log" )==False:
        command += " > vcpkgbin.log"
    else:
        command += " >> vcpkgbin.log"
    ret_code=os.system(command)
    return ret_code