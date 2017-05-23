from setuptools import setup, find_packages

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='aiowebfinger',
    version='0.0.1',
    description='An asyncio webfinger client',
    long_description=long_description,
    author='William Pitcock',
    author_email='nenolod@dereferenced.org',
    url='https://github.com/kaniini/aiowebfinger',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ]
)
