import os,string
from conans import tools


def update_conan_setting(port_list,triplet):
    conan_setting_filename= os.environ['Homedrive'] + os.environ['Homepath'] + os.sep + ".conan" + os.sep + "settings.yml"
    conan_setting__org_filename= os.environ['Homedrive'] + os.environ['Homepath'] + os.sep + ".conan" + os.sep + "settings_org.yml"    
    if os.path.isfile(conan_setting__org_filename) == False:
        conan_setting_content = tools.load(conan_setting_filename)
        tools.save(conan_setting__org_filename,conan_setting_content)
    if os.path.isfile(conan_setting__org_filename) == True:
        conan_setting_content = tools.load(conan_setting__org_filename)
        conan_setting_content += "\nvcpkg_triplet: [%s]" % triplet
        conan_setting_content += "\nvcpkg_port: [%s]\n" % port_list
        tools.save(conan_setting_filename,conan_setting_content)
    else:
         print("fail to update setting")

def parse_packagename(bintray_package):
    packagename,str_list,channel = bintray_package.split("/")
    packageversion,user = str_list.split("@")
    return packagename,packageversion,user,channel

def gen_producer_conanfile(repo_name,repo_version,user_name,channel_name,vcpkg_path,portlist,gen_path):
    conan_producer_recipe_template = vcpkg_path + os.sep + "conan_script" + os.sep + "producer_conanfile_template.py"
    conan_producer_recipe = gen_path + os.sep + "conanfile.py"
    if os.path.isfile(conan_producer_recipe_template) == True:
        producer_conanfile_template_content=tools.load(conan_producer_recipe_template)
        producer_conanfile_template_content = producer_conanfile_template_content % (user_name,channel_name,repo_name,repo_version,vcpkg_path,portlist)
        tools.save(conan_producer_recipe,producer_conanfile_template_content)
    else:
        raise Exception("conan recipe template not found")

def gen_consumer_conanfile(bintray_package,vcpkg_path,gen_path):
    conan_consumer_recipe_template = vcpkg_path + os.sep + "conan_script" + os.sep + "consumer_conanfile_template.txt"
    conan_consumer_recipe = gen_path + os.sep + "conanfile.txt"
    if os.path.isfile(conan_consumer_recipe_template) == True:
        consumer_conanfile_template_content=tools.load(conan_consumer_recipe_template)
        consumer_conanfile_template_content = consumer_conanfile_template_content % (bintray_package)
        tools.save(conan_consumer_recipe,consumer_conanfile_template_content)
    else:
        raise Exception("conan recipe template not found")