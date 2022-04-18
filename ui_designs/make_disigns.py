from os import getcwd, listdir, system
from os.path import join

designs_dir_name = 'designs'
py_designs_dir_name = 'py_designs'

cwd = getcwd()
designs_dir_path = join(cwd, designs_dir_name)
py_designs_dir_path = join(cwd, py_designs_dir_name)

for name in listdir(designs_dir_path):
    print(name)
    name_without_ext = name.split('.')[0]
    design_path = join(designs_dir_path, name)
    py_design_path = join(py_designs_dir_path, name_without_ext)
    system(f'pyuic5 {design_path} -o {py_design_path}.py')
