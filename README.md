# `vcpkgbin`
- Downloading vcpkg binary through conan from bintray

## `Requirement`
- Python >= 3.6
- 7z.exe
- set `pip` , `python`and `7z.exe` path in environment variable

## `run`
- syntax:

```bat
        vcpkgbin.bat <operation> <conanPackageName> <vcpkgportname> <vcpkg triplet>
```
### `operation`
1. `[download package]`
    - it will download library to local system
    - syntax:
    ```bat
        vcpkgbin.bat download <conanPackageName> <vcpkgportname> <vcpkg triplet>
    ```
    - example 1: **for downloading bzip2:x64-windows-v141 package**
    ```bat
        vcpkgbin.bat download vcpkg/0.0.81-6@had/vcpkg bzip2 x64-windows-v141  
    ```
2. `[listing package present in remote]`
    - it will show the package information which is present in remote system
    - syntax:
    ```bat
        vcpkgbin.bat list <conanPackageName>
        vcpkgbin.bat list <conanPackageName> <vcpkg triplet>
        vcpkgbin.bat list <conanPackageName> <vcpkg triplet> <vcpkgportname>
    ```
    - example 2: **for listing list of triplet installed in remote vcpkg/0.0.81-6@had/vcpkg**
    ```bat
        vcpkgbin.bat list remote vcpkg/0.0.81-6@had/vcpkg  
    ```
    - example 3: **for listing list of ports of x64-windows-v141 installed in remote vcpkg/0.0.81-6@had/vcpkg**
    ```bat
        vcpkgbin.bat list remote vcpkg/0.0.81-6@had/vcpkg x64-windows-v141
    ```
    - example 4: **for listing information of bzip2 of x64-windows-v141 installed in remote vcpkg/0.0.81-6@had/vcpkg**
    ```bat
        vcpkgbin.bat list remote vcpkg/0.0.81-6@had/vcpkg x64-windows-v141 bzip2
    ```
3. `[listing package present in local]`
    - it will show the package information which is already downloaded to local system
    - syntax:
    ```bat
        vcpkgbin.bat list local
        vcpkgbin.bat list local <vcpkg triplet>
        vcpkgbin.bat list local <vcpkg triplet> <vcpkgportname>
    ```
    - example 5: **for listing list of triplet installed in current directory**
    ```batch
        vcpkgbin.bat list local
    ```
    - example 6: **for listing list of ports of x64-windows-v141 installed in current directory**
    ```batch
        vcpkgbin.bat list local x64-windows-v141
    ```
    - example 7: **for listing information of bzip2 of x64-windows-v141 installed in current directory**
    ```batch
        vcpkgbin.bat list local x64-windows-v141 bzip2
    ```

## `notes`
- after running this script, all the requested package will be installed/<platform>-windows-<toolset>
