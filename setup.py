from setuptools import setup, find_packages

setup(name='ExilTool',
      version='1.0',
      author='Jean Giard',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      package_data={'exiltool': ['templates/*']},
      install_requires=['injector', 'pymongo', 'pyckson', 'flask', 'flask-session']
      )
