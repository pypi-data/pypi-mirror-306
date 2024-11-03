import os , shutil , subprocess , glob , json , sys 





class Nimc : 
    def __init__(self, prj) : 
        class DictClass : pass 
        self.data = DictClass()
        self.data.prj = os.path.abspath(prj) ; assert os.path.exists(self.data.prj)
        self.data.src = os.path.join(self.data.prj,'nim') ; assert os.path.exists(self.data.src)

    def setMainFile(self,file) : 
        self.data.Mainfile = os.path.join(self.data.src , file)
        self.data.name = os.path.basename(self.data.Mainfile).removesuffix('.nim')
        assert os.path.exists(self.data.Mainfile) 

    def copy_headers(self, src , dist ) : 
        headers = glob.glob(os.path.join(src , "*.h"))
        for file in headers : 
            shutil.copy(file , os.path.join(dist,os.path.basename(file)))

    def copy_srcfiles(self, src , dist ) : 
        srcfiles = glob.glob(os.path.join(src , "*.c"))
        self.data.srcfiles = set()
        for file in srcfiles : 
            self.data.srcfiles.add(os.path.basename(file))
            shutil.copy(file , os.path.join(dist,os.path.basename(file)))


    def createMakefile(self) : 
        jsonfile = glob.glob(os.path.join(self.data.nimcache , "*.json"))
        self.data.json = json.load(open(jsonfile[0]))
        compiling = self.data.json.get('compile')
        makebuild = list()
        for compilefile in compiling : 
            file = compilefile[0]
            cmd = compilefile[1]
            cmd = cmd.replace(self.data.src , './include').split()
            cmd = " ".join([os.path.join("./src" , i ) if i in self.data.srcfiles else i for i in cmd ])
            makebuild.append(cmd)
        linkedobjects = { i : os.path.basename(i) for i in self.data.json.get('link') }
        linkcmd = [linkedobjects.get(i,i) for i in self.data.json.get('linkcmd').split() ]
        linkcmd = " ".join([os.path.basename(i) if i.endswith('.so') else i for i in linkcmd])
        with open(os.path.join(self.data.build , 'Makefile'),'w') as buff : 
            nimversion = '\n'.join([f'# {line}' for line in subprocess.check_output(['nim','--version'] , text=True).strip().split("\n")])
            buff.write(nimversion)
            buff.write('\n.PHONY: test build all\nexport LD_LIBRARY_PATH := $(LD_LIBRARY_PATH):.\n')
            buff.write('\nbuild :\n')
            buff.write('\n'.join(['\t' + i for i in makebuild ]))
            buff.write( '\n\t' + linkcmd )
            buff.write( '\n\trm *.o\n' )
            buff.write( '\n\n')
            buff.write('test :\n')
            buff.write(f'\tgcc ./test/{os.path.basename(self.data.testcfile)} -I./include -L./ -l{self.data.name} -o ./test.out \n')
            buff.write('\texport LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:.\n')
            buff.write(f'\t./test.out \n')
            buff.write( '\n\n')
            buff.write('all : build\n\n')
            
    def createTest(self) : 
        self.data.test = os.path.join(self.data.build,'test')
        os.makedirs(self.data.test , exist_ok = True ) 
        self.data.testcfile = os.path.join(self.data.test,'main.c')
        if not os.path.exists(self.data.testcfile) : 
            c_code = '#include <stdio.h>\n'
            c_code += f'#include "{self.data.header}"'
            c_code += '\n\nint main(int argc, char *argv[]) {'
            c_code += '\n\tNimMain();\n'
            c_code += '\n\t' * 5 
            c_code += '''int r = add(1 , 2 ) ;'''
            c_code += '\n\t'
            c_code += '''printf("1 + 2 = %d ", r);'''
            c_code += '\n\treturn 0 ; \n}'
            print(c_code , file = open(self.data.testcfile  , 'w'))

    def compile(self) : 
        self.data.nimcache = os.path.join(self.data.prj , 'nimcache')
        self.data.build = os.path.join(self.data.prj , f'{self.data.name}')
        os.makedirs(self.data.build , exist_ok = True)
        if os.path.exists(self.data.nimcache)  : shutil.rmtree(self.data.nimcache)
        os.makedirs(self.data.nimcache  , exist_ok = True )
        self.data.header = f'{self.data.name}.h'
        self.data.cmd = ' '.join([
            'nim c ' , 
            '-d:release' , 
            f'--nimcache:{self.data.nimcache}' , 
            '--genScript' , 
            f'--header:{self.data.header}' , 
            '--gc:refc -d:useMalloc --noMain --app:lib', 
            f'{self.data.Mainfile}'
        ])
        self.data.cmd  = [ i.strip() for i in self.data.cmd.split(' ')  if i.strip() != '']
        nim = shutil.which('nim')
        result = subprocess.run(self.data.cmd , capture_output=True, text=True)
        if result.returncode != 0 : 
            exit('[Error] compiling lib.nim \n' + result.stderr)
        self.data.output = result.stdout
        self.data.buildInclude = os.path.join(self.data.build , 'include') ; os.makedirs(self.data.buildInclude , exist_ok = True)
        self.copy_headers(self.data.nimcache , self.data.buildInclude)
        self.data.buildsrc = os.path.join(self.data.build , 'src') ; os.makedirs(self.data.buildsrc, exist_ok = True)
        self.copy_srcfiles(self.data.nimcache , self.data.buildsrc)
        self.createTest()
        self.createMakefile()
        shutil.copy(os.path.join(self.data.prj , 'info.yml') , os.path.join(self.data.build , 'ext.manifest'))

        




































