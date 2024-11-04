from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    readme = file.read()
 
setup(
    name='ofilepy',
    version='1.1.2',
    license='MIT License',
    author='Lincoln Oliver',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='lincolnolive@gmail.com',
    keywords='files manipulation with python',
    description='A library to make easier work with files in local system',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    url='https://github.com/lincolnolivr/pylib_ofilepy.git'
)