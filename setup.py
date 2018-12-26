from setuptools import setup, find_packages

setup(name='pyclimax',
      version='0.0.1',
      description='Python API for talking to Climax HA controllers',
      url='https://github.com/pavoni/pyvera',
      author='Niklas Hjern',
      author_email='',
      license='MIT',
      install_requires=['requests>=2.0'],
      packages=find_packages(),
      zip_safe=True)
