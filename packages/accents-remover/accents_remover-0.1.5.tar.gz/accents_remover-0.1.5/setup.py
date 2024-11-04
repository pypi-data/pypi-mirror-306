from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    readme = file.read()
 
setup(
    name='accents_remover',
    version='0.1.5',
    license='MIT License',
    author='Lincoln Oliver',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='lincolnolive@gmail.com',
    keywords='remove accents',
    description='A function to remove string accents withouth changing other characters',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    url='https://github.com/lincolnolivr/pylib_accents_remover.git'
)