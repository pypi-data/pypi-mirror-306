from setuptools import setup, find_packages

setup(
    name='BlutoRS',
    version='2.4.18',
    author='Darryl Lane',
    maintainer='ProjectResurrect',
    maintainer_email='contact@boukhrisssaber.tn',
    url='https://github.com/ProjectResurrect/Bluto',
    packages=find_packages(),  # Automatically finds all packages and subpackages
    include_package_data=True,
    license='LICENSE.txt',
    description=(
        "DNS Recon | Brute Forcer | DNS Zone Transfer | DNS Wild Card Checks | "
        "DNS Wild Card Brute Forcer | Email Enumeration | Staff Enumeration | "
        "Compromised Account Checking"
    ),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "docopt",
        "dnspython",
        "termcolor",
        "beautifulsoup4",
        "requests[security]",
        "pythonwhois",
        "lxml",
        "oletools",
        "pdfminer.six"  # Updated to pdfminer.six as pdfminer is outdated
    ],
    python_requires='>=3.6',  # Requires Python 3.6 or higher
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Use the appropriate license if different
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'bluto=Bluto.bluto:main',  # Allows users to run 'bluto' from the CLI
        ],
    },
)