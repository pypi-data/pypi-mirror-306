from setuptools import setup, find_packages

setup(
    name='plotassist',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'pandas'
    ],
    author='Calvin Sprouse',
    author_email='calvinsprouse@proton.me',
    description='A package for handling MATLAB data and working with Matplotlib plots',
    long_description=open('README.md', mode='r', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CalvinSprouse/plotassist',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
