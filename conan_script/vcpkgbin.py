import os,platform,sys,yaml
import conan_config

class Vcpkgconan:
    _ports_name=""
    _triplet=""
    _vcpkg_path=""
    _bintray_package=""
    _user_type=""
    _user_input = []

    def __init__(self, argv):
        if sys.argv[1] != '-s':
            validate_status=self.validate_arg(sys.argv)
            if validate_status==False:
                self.help()
                raise Exception("invalid argument provided")

        self._vcpkg_path = os.path.normpath(os.getcwd())
        self._user_type=sys.argv[1]
        if self._user_type != '-s':
            self._bintray_package = sys.argv[2]
            self._ports_name = sys.argv[3]
            self._triplet = sys.argv[4]
        else:
            self._user_input = sys.argv

    def run(self):
        if self._user_type == "-c":
            self.launch_conan_consumer_recipe()
        elif self._user_type == "-s":
            self.search(str(self._vcpkg_path +os.sep+ "downloaded"+ os.sep + "RemotePkg" + os.sep + "download_packages_info.yml"), self._user_input)

    def downloadpkg(self,conan_consumer_recipe_dir,download_vcpkg_bin_path,portname,triplet):
        port_7z_file_path = download_vcpkg_bin_path +os.sep+"RemotePkg"+os.sep+ "%s_%s.7z" % (portname,triplet)
        vcpkg_bin_install= download_vcpkg_bin_path+os.sep+"installed"
        vcpkg_bin= vcpkg_bin_install+os.sep+self._triplet
        consumer_log = download_vcpkg_bin_path+ os.sep + "Consumerlog"
        print("%s:%s is installing,Please wait..." % (portname,triplet),end="\r")
        if os.path.isfile(port_7z_file_path )==False:
            os.makedirs(consumer_log, exist_ok=True)
            os.system('conan install %s --install-folder %s -s vcpkg_port=%s -s vcpkg_triplet=%s > %s\%s_%s_log.txt' % (conan_consumer_recipe_dir,download_vcpkg_bin_path,portname,triplet,consumer_log,portname,triplet))
            if os.path.isfile(port_7z_file_path )==True:
                self.system('del /Q %s\*.txt' % download_vcpkg_bin_path)
                self.system('7z.exe x %s -aoa -o%s > nul' % (port_7z_file_path,vcpkg_bin))
                self.system('del /Q %s\CONTROL' % vcpkg_bin)
                self.system('del /Q %s\BUILD_INFO' % vcpkg_bin)
                print("%s:%s is installed                " % (portname,self._triplet))
            else:
                print("%s:%s is not available in the repository" % (portname,triplet))
        else:
            print("%s:%s is already installed           " % (portname,triplet))

    def launch_conan_consumer_recipe(self):        
        download_vcpkg_bin_path= self._vcpkg_path +os.sep+ "downloaded"
        conan_consumer_recipe_dir = download_vcpkg_bin_path+ os.sep + "ConsumerRecipe"
        conan_config.gen_consumer_conanfile(self._bintray_package,self._vcpkg_path,conan_consumer_recipe_dir)
        port_list = self._ports_name.split(" ")
        setting_port_list = self._ports_name.replace(" ",",")
        conan_config.update_conan_setting(setting_port_list,self._triplet)       
        for portname in port_list:
            self.downloadpkg(conan_consumer_recipe_dir,download_vcpkg_bin_path,portname,self._triplet)
            port_info_file_path = download_vcpkg_bin_path +os.sep+"RemotePkg"+os.sep+ "%s_%s.yml" % (portname,self._triplet)
            if os.path.isfile(port_info_file_path )==True:
                stream = open(port_info_file_path, 'r')
                data = yaml.load(stream)
                dependant_port_list = data[portname]['Dependant']
            port_yaml_path = download_vcpkg_bin_path +os.sep+"RemotePkg"+os.sep+ "%s_%s.yml" % (portname,self._triplet)
            downloaded_packages_info_file_path = download_vcpkg_bin_path + os.sep + "RemotePkg" + os.sep + "download_packages_info.yml"
            self.prepare_yml_file(downloaded_packages_info_file_path, port_yaml_path)
            for port in dependant_port_list:
                if port not in setting_port_list:
                    setting_port_list += "," + port
                    conan_config.update_conan_setting(setting_port_list,self._triplet)
                    self.downloadpkg(conan_consumer_recipe_dir,download_vcpkg_bin_path,port,self._triplet)
                depend_port_yaml_path = download_vcpkg_bin_path +os.sep+"RemotePkg"+os.sep+ "%s_%s.yml" % (port,self._triplet)
                self.prepare_yml_file(downloaded_packages_info_file_path, depend_port_yaml_path)

    def help(self):
        print("python vcpkg.py <bintray pakage name> <vcpkg port name> <triplet>")

    def validate_arg(self,argv):
        validate_status=True
        if len(argv[1:]) != 4:
            validate_status=False
            self.help()
        return validate_status

    def system(self,command):
        ret_code=os.system(command)
        if ret_code != 0:
            raise Exception("Error in executing:\n\t %s" % command)

    def write_to_yml(self, file, key, value):
        data = { key:value }
        with open(file, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style = False)

    def read_yml_file(self, file):
        stream = open(file, 'r')
        data = yaml.load(stream)
        return data

    def prepare_yml_file(self, output_yml_file_path, port_yml_path):
            if os.path.exists(output_yml_file_path):
                self.overwrite_yml(output_yml_file_path, str(self._bintray_package + ' ' + self._triplet), port_yml_path)
            else:
                bintray_package_info = {self._bintray_package : {self._triplet : self.read_yml_file(port_yml_path)}}
                self.write_to_yml(output_yml_file_path, 'bintray', bintray_package_info)

    def overwrite_yml(self, file, path, additional_filename):
            additional_value = self.read_yml_file(additional_filename)
            data = self.read_yml_file(file)
            parts = path.split(' ')
            if len(parts) == 2:
                if parts[1] in data['bintray']['%s' % parts[0]].keys():
                    data['bintray']['%s' % parts[0]]['%s' % parts[1]].update(additional_value)
                else:
                    new_triplet_updated_value = {parts[1] : additional_value}
                    data['bintray']['%s' % parts[0]].update(new_triplet_updated_value)
                self.write_to_yml(file, 'bintray', data['bintray'])

    def search(self, file, argv):
        print('')
        if os.path.exists(file):
            data = self.read_yml_file(file)
            temp_file_path = self._vcpkg_path +os.sep+ "downloaded" + os.sep + "RemotePkg" + os.sep + "temp.yml"
            if len(argv) == 2:
                    print('Available bintray packages: ')
                    for key in data['bintray'].keys():
                        print(key)
            elif len(argv) == 3:
                print('Available ports in ' + argv[2] + ' are: ')
                try:
                    self.write_to_yml(temp_file_path, argv[2], data['bintray']['%s' % argv[2]])
                    f = open(temp_file_path,'r')
                    f.readline()
                    print(f.read())
                    f.close()
                    os.remove(temp_file_path)
                except KeyError:
                    print('Invalid bintray package!')
            elif len(argv) == 4:
                print('Availale packages in ' + argv[2] + ':' + argv[3] + ' are:')
                try:
                    self.write_to_yml(temp_file_path, argv[2], data['bintray']['%s' % argv[2]]['%s' % argv[3]])
                    f = open(temp_file_path,'r')
                    f.readline()
                    print(f.read())
                    f.close()
                    os.remove(temp_file_path)
                except KeyError:
                    print('Invalid  bintray package or triplet name!')
            elif len(argv) == 5:
                print(argv[4] + ':')
                try:
                    self.write_to_yml(temp_file_path, argv[2], data['bintray']['%s' % argv[2]]['%s' % argv[3]]['%s' % argv[4]])
                    f = open(temp_file_path,'r')
                    f.readline()
                    print(f.read())
                    f.close()
                    os.remove(temp_file_path)
                except KeyError:
                    print('Invalid bintray package or triplet or port name!')
        else:
            print('No packages available.')

if __name__ == "__main__":
    conan_mgr=Vcpkgconan(sys.argv)
    conan_mgr.run()

