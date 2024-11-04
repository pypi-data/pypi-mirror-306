from setuptools import find_packages, setup

setup(
    name='python-sqlbuddy',
    packages=find_packages(include=['sqlbuddy']),
    version='0.1.2',
    description='A SQL library for generating SQL queries using GPT-4o',
    author='Pradeep Kumar Yadav',
    install_requires=['langchain', 'langchain_community', 'langchain_experimental', 'langchain_openai'],
    author_email='pydev.pk@gmail.com'
)