from setuptools import setup, find_packages

# Read the long description from the README file
with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='iMail',  # Package name
    version='1.1.0',  # Version number
    description='A simple and effective email notification script.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Zhiwei Li',
    author_email='lizhw.cs@outlook.com',
    url='https://github.com/mtics/iMail',
    install_requires=[
        'Pillow',  # Required dependency
    ],
    license='MIT License',  # Corrected license
    packages=find_packages(),  # Automatically find packages
    platforms=["all"],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Email',
    ],
)
