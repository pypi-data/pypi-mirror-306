from setuptools import setup, find_packages

setup(
    name='harshpy',
    author='Harsh Sankhala',
    description='A Basic Demo pip package',
    entry_points={
        'console_scripts': [
            'harshpy=harshpy.shell:main',
        ],
    },
    install_requires=[
        'readchar', 'rich'
    ]
)
