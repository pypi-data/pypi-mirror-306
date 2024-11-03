from setuptools import setup

setup(
    name='binaryrepr',
    version='0.19',
    author='David Lamouller',
    author_email='dlamouller@protonmail.com',
    py_modules=['binaryrepr'],
    install_requires=[
        'Click',
        'PrettyTable',
    ],
    description="binaryrep utility to display position of the bits for a number.",
    long_description='binaryrep is a utility to display position of the bits of a number. Entries can be decimal, hexadecimal, binary or octal.',
    long_description_content_type='text/plain',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Utilities'
    ],
    keywords='binary representation', 
    url='https://github.com/dlamouller/binaryreprtui',
    entry_points='''
        [console_scripts]
        binaryrepr=binaryrepr:binaryrepr
    ''',
)
