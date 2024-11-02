from setuptools import setup, find_packages
setup(
    name='notix',
    version='0.0.1',
    author='Pop1avok',
    author_email='pop1avplov@example.com',
    description='A simple library for showing notifications.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Pop1avok/notix/',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)