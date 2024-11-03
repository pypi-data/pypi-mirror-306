import pkg_resources

# 替换'module_name'为你想查看的模块名
module_name = 'setuptools'

# 获取模块的版本
version = pkg_resources.get_distribution(module_name).version

print(f"The version of {module_name} is {version}")