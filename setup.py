from setuptools import setup

setup(name='ges',
      version='0.1',
      description='geometrical efficiency calculator',
      url='https://github.com/andry3vi/GeometryEfficiencySimulation',
      author='Oiggart',
      author_email='andrea.a.raggio@jyu.fi',
      license='GPL-3.0',
      packages=['ges'],
      install_requires=[
          'tqdm',
          'argparse',
      ],
      zip_safe=False,
      entry_points={
        'console_scripts': [
            'ges = ges:main'
        ]},
        )