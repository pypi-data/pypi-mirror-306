
cpp_code = '''
// myextension.cpp
// Extension lib defines
#define LIB_NAME "{{extension}}"
#define MODULE_NAME "{{extension}}"

// include the Defold SDK
#include <dmsdk/sdk.h>

extern "C" {
	#include "{{extension}}.h"
}

{{nim_cpp_implemenation}}

static void LuaInit(lua_State* L)
{
	int top = lua_gettop(L);

	// Register lua names
	luaL_register(L, MODULE_NAME, Module_methods);

	lua_pop(L, 1);
	assert(top == lua_gettop(L));
}

static dmExtension::Result AppInitializeMyExtension(dmExtension::AppParams* params)
{
	dmLogInfo("AppInitializeMyExtension");
	return dmExtension::RESULT_OK;
}

static dmExtension::Result InitializeMyExtension(dmExtension::Params* params)
{
	// Init Lua
	LuaInit(params->m_L);
	NimMain();
	dmLogInfo("Registered %s Extension", MODULE_NAME);
	return dmExtension::RESULT_OK;
}

static dmExtension::Result AppFinalizeMyExtension(dmExtension::AppParams* params)
{
	dmLogInfo("AppFinalizeMyExtension");
	return dmExtension::RESULT_OK;
}

static dmExtension::Result FinalizeMyExtension(dmExtension::Params* params)
{
	dmLogInfo("FinalizeMyExtension");
	return dmExtension::RESULT_OK;
}

static dmExtension::Result OnUpdateMyExtension(dmExtension::Params* params)
{
	dmLogInfo("OnUpdateMyExtension");
	return dmExtension::RESULT_OK;
}

static void OnEventMyExtension(dmExtension::Params* params, const dmExtension::Event* event)
{
	switch(event->m_Event)
	{
		case dmExtension::EVENT_ID_ACTIVATEAPP:
			dmLogInfo("OnEventMyExtension - EVENT_ID_ACTIVATEAPP");
			break;
		case dmExtension::EVENT_ID_DEACTIVATEAPP:
			dmLogInfo("OnEventMyExtension - EVENT_ID_DEACTIVATEAPP");
			break;
		case dmExtension::EVENT_ID_ICONIFYAPP:
			dmLogInfo("OnEventMyExtension - EVENT_ID_ICONIFYAPP");
			break;
		case dmExtension::EVENT_ID_DEICONIFYAPP:
			dmLogInfo("OnEventMyExtension - EVENT_ID_DEICONIFYAPP");
			break;
		default:
			dmLogWarning("OnEventMyExtension - Unknown event id");
			break;
	}
}


DM_DECLARE_EXTENSION({{extension}}, LIB_NAME, AppInitializeMyExtension, AppFinalizeMyExtension, InitializeMyExtension, OnUpdateMyExtension, OnEventMyExtension, FinalizeMyExtension)
'''

import subprocess , shutil , tempfile , os , textwrap , re , json , io 
from bs4 import BeautifulSoup , formatter
import jinja2




class NimAstNode : 
	__NIM_AST_NODE__ = True 
	def __init__(self , *args, parent = None ) : 
		self.parent = parent 
		self.args  = args
		[i.setparent(self) for i in self.args if self._checkarg_isast(i) ] 
		self.text = [i  for i in self.args if not self._checkarg_isast(i) ] 
		self.childs = [i  for i in self.args if  self._checkarg_isast(i) ] 
		def newTree(self,*args) :return type(self)(*args)
		if self.isnewTree : setattr(self,'newTree', newTree)

	def toxml(self, indent = 0 ) : 
		_indent = indent + 1
		return f"\n{'    '* indent}<{type(self).__name__}>{''.join([i.toxml(indent = _indent) if  self._checkarg_isast(i) else json.dumps(i) for i in self.args ])}\n{'    '* indent}</{type(self).__name__}>"

	def dump(self) : 
		callnewtree = "" if not self.isnewTree else '.newTree'
		return f"{type(self).__name__}{callnewtree}({','.join([json.dumps(i) if  not self._checkarg_isast(i)  else i.dump() for i in self.args ])})"
	
	def setparent(self,parent) : 
		self.parent = parent

	def _checkarg_isast(self,arg) : 
		return hasattr(arg,'__NIM_AST_NODE__')
	
	def get(self,child) : 
		result = list()
		for i in self.childs : 
			if i.name == child : 
				result.append(i)
		return result
	
	def __repr__(self) -> str:
		return f'{self.name}({",".join(self.text)})'
	
	def has(self,child) : 
		return len([ch for ch in self.childs if ch.name == child]) != 0 


class nim  : 
	class ast : 
		pass 

	@classmethod
	def parse(cls,code , nim = None ) : 
		compiler_nim = nim if nim is not None else shutil.which('nim')
		astresult = None
		with tempfile.NamedTemporaryFile(mode='w+', suffix = '.nim' , delete=True) as temp_file:
			indented_code =  textwrap.indent(code, prefix="    ")
			temp_file.write(f'import macros \n\n\ndumpAstGen : \n{indented_code}\n')
			temp_file.flush()
			cmd = [
				compiler_nim , 'r' , '--hints:off' , temp_file.name
			]
			result = subprocess.run(cmd, capture_output=True, text=True)
			if result.returncode != 0 : 
				raise Exception(result.stderr)
			astresult = result.stdout
		return cls._convert2Tree(astresult.strip())
	
	@classmethod
	def unparse(cls,code , nim = None ) : 
		compiler_nim = nim if nim is not None else shutil.which('nim')
		astresult = None
		with tempfile.NamedTemporaryFile(mode='w+', suffix = '.nim' , delete=True) as temp_file:
			indented_code =  textwrap.indent(code.dump(), prefix="    ")
			temp_file.write(f'import macros\n\n\nmacro TreeGeneration(): untyped =\n  let tree = {indented_code}\n  echo tree.repr\n\nTreeGeneration()\n')
			temp_file.flush()
			cmd = [
				compiler_nim , 'r' , '--hints:off' , temp_file.name
			]
			result = subprocess.run(cmd, capture_output=True, text=True)
			if result.returncode != 0 : 
				raise Exception(result.stderr)
			astresult = result.stdout
		return astresult.strip()
	
	@classmethod
	def _convert2Tree(cls,tree_str) : 
		txt = "".join([i.lstrip() for i in tree_str.splitlines()])
		affected_newTree = re.findall(r'\b(\w+)\.newTree\(', txt)
		txt =  re.sub(r'(\b\w+\b)\.newTree\(', r'\1(', txt)
		lc = dict()
		name , done = None , False   
		## init 
		while not done   : 
			done = True 
			if name is not None : 
				astnodetype = type(name , (NimAstNode,) , dict(__qualname__ = name , isnewTree = name in affected_newTree  , name = name ))
				#setattr(cls.ast , name , astnodetype)
				lc[name] = astnodetype
			try : 
				exec(f"tree = {txt}" , dict() , lc )
			except NameError as err : 
				name = err.name 
				done = False
			except Exception as e:
				# Handle any other exceptions
				print(f"An unHandle error occurred: {e}" , e)
		return lc.get('tree')
	
class NimAstVistor : 
	def __init__(self,code) : 
		self.tree :str  = nim.parse(code)
		self.data = dict(procs = list())

	def visit(self) : 
		self.genric_visit()
		return self.data 


	def genric_visit(self) : 
		for i in self.tree.childs : 
			if i.name == 'nnkProcDef' : 
				node = self.visit_nnkProcDef(i)
				if node : 
					self.genric_visit(node)

	def visit_nnkProcDef(self,node) : 
		self.parse_nnkProcDef(node)



	def parse_nnkProcDef(self,node) : 
		func = dict(name = node.text , params = list())
		ispublic = any(i.text[0].strip() == "*" for i in node.get('nnkPostfix')[0].get('newIdentNode') )
		if not ispublic : 
			return None 
		name = [i.text[0] for i in node.get('nnkPostfix')[0].get('newIdentNode') if i.text[0].strip() != "*" ][0]
		func['name'] = name
		func['returntype'] = 'void' 
		for i in node.get('nnkFormalParams')[0].childs: 
			if i.name == 'newIdentNode' : 
				func['returntype'] = i.text[0]
			if i.name == 'nnkIdentDefs' : 
				if  i.has('nnkVarTy') or i.has('nnkPtrTy') : 
					annotation = {i.has('nnkVarTy') : 'nnkVarTy' , i.has('nnkPtrTy')  : 'nnkPtrTy'}.get(True)
					# pass by ref 
					argtype = i.get(annotation)[0].get('newIdentNode')[0].text[0].strip()
					argname = [j.text[0].strip() for j in i.get('newIdentNode') if j.text[0].strip() != "" ][0]
					arg = {
						'name' : argname , 'type' : argtype 
					}
					func['params'].append(arg)
					L.print(func , arg , i.toxml())
				else  : 
					# pass by value 
					arg = [j.text[0].strip() for j in i.get('newIdentNode') if j.text[0].strip() != "" ]
					arg = {
						'name' : arg[0] , 'type' : arg[1] 
					}
					func['params'].append(arg)

				
		self.data['procs'].append(func)

cpp_binding_proc = '''
static int nim_{{proc.name}}(lua_State* L)
{
	{%- for arg in proc.params %}
	int {{ arg.name }} = {{arg.lua}}(L, {{ loop.index  }});
	{%- endfor %}
	{{proc.type}} result = {{proc.name}}({{proc.callargs}}) ; 
	{{proc.push}}(L, result);
	return 1;
}
'''
cpp_luaL_reg  = '''
static const luaL_reg Module_methods[] =
{
	{%- for name in procs %}
	{"{{name}}", nim_{{name}}},
	{%- endfor %}
	{0, 0}
};
'''
class NimExportCpp : 
	LUA_CHECKS = {
		'cint' : 'luaL_checkinteger' , 
	}
	NIMCTYPES = {
		'cint' : 'int' 
	}
	LUA_PUSHS = {
		'cint' : 'lua_pushinteger'
	}
	def __init__(self, code) -> None:
		self.data =  NimAstVistor(code).visit()


	def createcppprocs(self) : 
		cpp_code = list()
		for i in self.data['procs'] : 
			proc = {
				'name' : i.get('name') , 
				'params' : [
					{
						'name' : arg.get('name') , 
						'ctype' : self.NIMCTYPES.get(arg.get('type')) , 
						'lua' : self.LUA_CHECKS.get(arg.get('type')) , 
						'callargs' : ",".join([a.get('name') for a in i.get('params')])
					}
					for arg in i.get('params')
				] , 
				'type' : self.NIMCTYPES.get(i.get('returntype'))  , 
				'push' : self.LUA_PUSHS.get(i.get('returntype'))
			}
			res = jinja2.Template(cpp_binding_proc).render(proc = proc )
			cpp_code.append(res)
		procs = [proc.get('name') for proc in self.data['procs'] ]
		res = jinja2.Template(cpp_luaL_reg).render(procs = procs )
		cpp_code.append(res)
		return "\n".join(cpp_code)
	

def render_cpp_template(name,nimfile) : 
	code = open(nimfile).read()
	nim_cpp_implemenation = NimExportCpp(code).createcppprocs()
	result = jinja2.Template(cpp_code).render({'extension' : name , 'nim_cpp_implemenation' : nim_cpp_implemenation}) 
	return result
	
