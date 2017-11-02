from setuptools import setup

setup(name='movieclassifier',
      version='0.0.1',
      description='A simple classifier for movie genre on Grakn',
      url='http://github.com/pluraliseseverythings/movieclassifier',
      author='Domenico Corapi',
      author_email='domenico@grakn.ai',
      packages=['movieclassifier'],
      install_requires=[
          'grakn',
          'tensorflow',
          'numpy',
          'sklearn',
          'pandas',
          'scipy'
      ])
