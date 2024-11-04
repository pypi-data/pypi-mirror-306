from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='simplified_regex',
    version='1.0',
    packages=find_packages(),
    license='MIT',
    description='A tool that simplifies RegEx extremly!',
    author='D&I',
    author_email='di.projects.help@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/d-i-projects/simplified_regex',
    download_url='https://github.com/D-I-Projects/simplified_regex/archive/refs/tags/v1.0.tar.gz',
    keywords=['simplified_regex', 'regex', 'simple'],
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points='''
        [console_scripts]
        diec-cli=diec.cli:cli
    ''',
)
