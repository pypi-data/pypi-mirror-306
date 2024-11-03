import click , os , yaml , json , jinja2
from nimc import Nimc
from nimc.extension import render_cpp_template


@click.group()
def cli():
    pass 

@cli.command()
@click.argument('name')
@click.argument('path', default=os.getcwd())
def init(name,path) : 
    projectpath = os.path.join(path,name)
    os.makedirs(projectpath , exist_ok=False )
    os.makedirs(os.path.join(projectpath , 'nim'))
    nimcode = 'proc add*( a : cint , b:cint ): cint {.cdecl,exportc,dynlib.} = \n    return a + b'
    print(nimcode, file=open(os.path.join(projectpath , 'nim',f'{name}.nim'),'w'))
    print(f'name : {name}' , file=open(os.path.join(projectpath , 'info.yml') , 'w'))

@cli.command()
@click.argument('path', default=os.getcwd())
def build(path) : 
    yaml_text = open(os.path.join(path,'info.yml'),'r').read()
    data = yaml.safe_load(yaml_text)
    x = Nimc(prj=path)
    name = data.get('name')
    x.setMainFile(f'{name}.nim')
    x.compile()
    rendred = render_cpp_template(name = name,nimfile = x.data.Mainfile ) 
    os.path.join(x.data.buildsrc , f'{name}.cpp')
    cpp_file = os.path.join(x.data.buildsrc , f'{name}.cpp')
    if not os.path.exists(cpp_file) : 
        print(rendred, file = open(cpp_file,"w"))
    if not os.path.exists(os.path.join(x.data.buildInclude,'nimbase.h')) : 
        current = os.path.join(os.environ.get('HOME') ,'.choosenim','current')
        current = open(current).read()
        nimbase = os.path.join(current,'lib','nimbase.h')
        content = open(nimbase).read()
        print(content , file=open(os.path.join(x.data.buildInclude,'nimbase.h'),'w'))
        

        

    

    


def main() : 
    cli()


if __name__ == '__main__' : 
    main()

