**BLUTO**
-----
**This project is a fork of [Bluto](https://github.com/darryllane/Bluto) by Darryl Lane. The original project appears unmaintained, so this fork by [ProjectResurrect](https://github.com/ProjectResurrect) aims to continue improving and maintaining it.**
-----
**DNS Recon | Brute Forcer | DNS Zone Transfer | DNS Wild Card Checks | DNS Wild Card Brute Forcer | Email Enumeration | Staff Enumeration | Compromised Account Enumeration | MetaData Harvesting**
 
>Maintainer: ProjectResurrect  |  Email:'contact@boukhrisssaber.tn'

>https://github.com/ProjectResurrect/Bluto


## About ProjectResurrect

**ProjectResurrect**  revives and updates powerful, forgotten open-source security tools, helping teams defend against modern threats with proven, trusted resources.


## Versioning

This fork continues from version `v2.4.17` of the original repository. The latest version is `v2.4.18` (details in the changelog).


## Usage

Bluto now takes command line arguments at launch, the new options are as follows;

	-e		This uses a very large subdomain list for bruting.
	-api	You can supply your email hunter api key here to gather a considerably larger amount of email addresses.
	-d		Used to specify the target domain on the commandline.
	-t		Used to set a timeout value in seconds. Default is 10

**Examples:** (feel free to use this EmailHunter API Key until it is removed)

	bluto -api 2b0ab19df982a783877a6b59b982fdba4b6c3669
	bluto -e
	bluto -api 2b0ab19df982a783877a6b59b982fdba4b6c3669 -e
	bluto -d example.com -api 2b0ab19df982a783877a6b59b982fdba4b6c3669 -e

## Installation Instructions

**Install Pip (if not already installed):**

Note: To test if pip is already installed execute.

`pip -V`

On Mac or Kali, run the following command to download and install `pip`.

`curl https://bootstrap.pypa.io/get-pip.py -o - | python`

**Install Bluto**

Once `pip` is installed, run the following command to install Bluto:

`sudo pip install bluto`

You should now be able to execute `bluto` from any working directory.
 
`bluto`

## Upgrade Instructions

To upgrade Bluto to the latest version, simply run:

`sudo pip install bluto --upgrade`


Changelog
====
* Version __2.4.8__ (__01/11/2024__):
  * Added Python 3 compatibility
  * fixed regular expressions
  * improved README

Legacy Versions
====
* Version __2.4.7__ (__20/07/2018__):
  * Last release by the original author
  * GeoIP lookup refactor
  
* Version __2.3.10__ (__13/01/2017__):
  * BugFixes
  
* Version __2.3.6__ (__14/08/2016__):
  * BugFixes
  * Timeout value can be parsed as argument (-t 5)
  
* Version __2.3.2__ (__02/08/2016__):
  * MetaData Scraping From Document Hunt On Target Domain
  * Target Domain Parsed As Argument
  
* Version __2.0.1__ (__22/07/2016__):
  * Compromised Account Data Prensented In Terminal And HTML Report

* Version __2.0.0__ (__19/07/2016__):
  * Pushed Live 2.0
 
* Version __1.9.9__ (__09/07/2016__):
  * Email Hunter API Support Added.
  * Haveibeenpwned API Support Added.
  * HTML Evidence Report Added.
  * Modulated Code Base.
  * Local Error Logging.