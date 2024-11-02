# setup.py
from setuptools import setup, find_packages

def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='finance_calculator_ForCU_Ruslan',
    version='0.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'finance_calculator_ForCU_Ruslan=finance_calculator_ForCU_Ruslan:main',
        ],
    },
    description='A simple finance calculator for net profit and ROI.',
    author='Ruslan',
    author_email='r.khuseyinov@edu.centraluniversity.ru',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
)
