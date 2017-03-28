from setuptools import setup, find_packages

setup(name='jukebox',
      # url='https://gitlab.com/danielhones/jukebox',
      license='MIT',
      version='0.0.0',
      packages=['jukebox'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['flask', 'Flask-SQLAlchemy'],
)
