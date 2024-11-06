from setuptools import setup, find_packages

setup(
    name='netcook_v2',
    version='2.3',
    packages=find_packages(),
    install_requires=[
        'requests==2.31.0',
        'tabulate==0.9.0',
        'beautifulsoup4==4.12.3',
        'googletrans==4.0.0-rc1',
        'pyunpack==0.3',
        'rarfile==4.2',
        'PyDrive2==1.6.3'
    ],
    entry_points={
        'console_scripts': [
            'netcook_v2=netcook_v2.netcook:checked_cookies',
        ],
    },
    author='NetCook',
    author_email='hupbyu36@gmail.com',
    description='A package to check Netflix cookies status.',
    long_description='A package to check Netflix cookies status.',
    long_description_content_type='text/plain',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
