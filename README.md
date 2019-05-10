# vcpkgbin
extracting vcpkg binary through conan

## Requirement
Python -: 3.6
7z.exe
set pip and python path and 7z.exe in environment variable

## run
run vcpkgbin.bat <operation> <conanPackageName> <vcpkg portname> <vcpkg triplet>
'download package'
example 1: vcpkgbin.bat download vcpkg/0.0.81-6@had/vcpkg bzip2 x64-windows-v141  (for download bzip2:x64-windows-v141 package)

'listing package present in remote'
example 2: vcpkgbin.bat list remote vcpkg/0.0.81-6@had/vcpkg  (for listing list of triplet installed in remote vcpkg/0.0.81-6@had/vcpkg)
example 3: vcpkgbin.bat list remote vcpkg/0.0.81-6@had/vcpkg x64-windows-v141 (for listing list of ports of x64-windows-v141 installed in remote vcpkg/0.0.81-6@had/vcpkg)
example 4: vcpkgbin.bat list remote vcpkg/0.0.81-6@had/vcpkg x64-windows-v141 bzip2 (for listing information of bzip2 of x64-windows-v141 installed in remote vcpkg/0.0.81-6@had/vcpkg)

'listing package present in local'
example 2: vcpkgbin.bat list local                        (for listing list of triplet installed in current directory)
example 3: vcpkgbin.bat list local x64-windows-v141       (for listing list of ports of x64-windows-v141 installed in current directory )
example 4: vcpkgbin.bat list local x64-windows-v141 bzip2 (for listing information of bzip2 of x64-windows-v141 installed in current directory)

'listing package present in local'
example 2: vcpkgbin.bat list local                        (for listing list of triplet installed in current directory)
example 3: vcpkgbin.bat list local x64-windows-v141       (for listing list of ports of x64-windows-v141 installed in current directory )
example 4: vcpkgbin.bat list local x64-windows-v141 bzip2 (for listing information of bzip2 of x64-windows-v141 installed in current directory)

## notes
after running this script, all the requested package will be installed/<platform>-windows-<toolset>
