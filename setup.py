from setuptools import setup

setup(name='koalas',
      version='0.1',
      description='A simple wrapper for simple pandas operations',
      url='http://github.com/flbulgarelli/koalas',
      author='Franco Bularelli',
      author_email='franco@mumuki.org',
      license='MIT',
      packages=['koalas'],
      install_requires=[
          'pandas',
      ],
      zip_safe=False)