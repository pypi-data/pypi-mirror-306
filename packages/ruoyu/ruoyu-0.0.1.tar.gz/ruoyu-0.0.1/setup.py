from setuptools import setup, find_packages

setup(
    name='ruoyu',
    version='0.0.1',
    author='brody715',
    author_email='brody715@gmail.com',
    description='',
    url='https://github.com/brody715/ruoyu',
    packages=find_packages(),

    tests_require=[
        'pytest>=7.2.0',
    ],
    python_requires='>=3.8'
)