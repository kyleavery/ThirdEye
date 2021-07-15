# ThirdEye
Weaponizing [CLRvoyance](https://github.com/Accenture/CLRvoyance) by adding the following features:
* Pass arguments to the target .NET assembly
* Obfuscate shellcode with [SGN](https://github.com/EgeBalci/sgn)

All the credit for this script goes to the Accenture team for their great tool. This repo also includes [DonutTest](https://github.com/TheWover/donut/tree/master/DonutTest) for testing output shellcode.

## Usage
* python3 thirdeye.py PATH_TO_ASSEMBLY

## Components
* [CLRvoyance](https://github.com/Accenture/CLRvoyance) - Generates PIC shellcode, created by Accenture
* wrapper - .NET assembly wrapper, hardcodes arguments
* thirdeye.py - Sets up wrapper and generates shellcode with CLRvoyanace

## Requirements
* Only works on Windows currently, should be easy enough to port
* MSBuild and Python 3.X must be present on the system
