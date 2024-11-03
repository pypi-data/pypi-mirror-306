from setuptools import setup, find_packages

setup(
    name='weather_query',
    version='0.1.3',
    packages=find_packages(),
    description='My sample package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='minsung8',
    author_email='alstjddl8@naver.com',
    url='https://github.com/minsung8/weather_project',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
