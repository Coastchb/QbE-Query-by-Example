try:
    from setuptools import setup #enables develop
except ImportError:
    from distutils.core import setup

setup(name='common_tool',
      version='1.0',
      description='Some common tools for audio processing',
      author='Coast Cao',
      author_email='Coastchb@sina.com',
      license='RUC',
      url='./',
      packages=['common/'],
    )
