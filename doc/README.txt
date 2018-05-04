		   __________________________________

		    U/PREQUELMEMES_BOT DOCUMENTATION

				 thecsw
		   __________________________________


Table of Contents
_________________

1 Getting started
.. 1.1 Prerequisites
.. 1.2 Other Dependencies
..... 1.2.1 Linux
..... 1.2.2 Mac OS (homebrew)
2 Installing
3 Deployment
4 Source code
5 Built With
6 Authors
7 License


*Hello there!*

Welcome to the source page of u/prequelmemes_bot! Nice to meet
you. First of all, let me talk you through what the bot does and details
later.


1 Getting started
=================

  These instructions will get you a copy of the project up and running
  on your local machine for development and testing purposes.  See
  deployment for notes on how to deploy the project on a live system.


1.1 Prerequisites
~~~~~~~~~~~~~~~~~

  ,----
  | sudo pip install praw
  | sudo pip install python-opencv
  | sudo pip install pytesseract
  | sudo pip install tesseract-ocr
  | sudo pip install Pillow
  | sudo pip install tqdm
  `----

  OR

  ,----
  | pip install --upgrade -r requirements.txt
  `----
  1. [praw] is Python Reddit API Wrapper. This will be the main and only
     package to connect to Reddit's API and extract desired data.
  2. [python-opencv] is used for image transformations and computer
     vision problems.
  3. [pytesseract] is a python wrapper for Google's Tesseract-OCR.
  4. [Pillow] is the Python Imaging Library by Fredrik Lundh and
     Contributors.
  5. [tqdm] is used for fancy progress bars.


  [praw] https://github.com/praw-dev/praw

  [python-opencv] https://pypi.python.org/pypi/opencv-python

  [pytesseract] https://pypi.python.org/pypi/pytesseract

  [Pillow] https://pillow.readthedocs.io/en/latest/

  [tqdm] https://pypi.python.org/pypi/tqdm


1.2 Other Dependencies
~~~~~~~~~~~~~~~~~~~~~~

  Tesseract engine should be installed on a local machine to run the
  text recognition properly. We will also install the tesseract OCR
  trained languages for better accuracy and we will install only the
  English packages. For more information about other languages, please
  refer to tesseract's official [repository on
  Github]([https://github.com/tesseract-ocr/tesseract]).


1.2.1 Linux
-----------

* 1.2.1.1 Debian, Ubuntu (aptitude)

  ,----
  | sudo apt-get install tesseract-ocr
  | sudo apt-get install tesseract-ocr-eng
  `----


* 1.2.1.2 Arch Linux (pacman)

  ,----
  | sudo pacman -S tesseract
  | sudo pacman -S tesseract-data-eng
  `----


1.2.2 Mac OS (homebrew)
-----------------------

  ,----
  | brew install tesseract
  `----


2 Installing
============

  The only thing that needs to be done before execution is the
  config. The only thing that needs to be done before execution is the
  config profile. In the config profile you should fill your Reddit API
  details.

  For that please follow the steps below

  ,----
  | git clone https://github.com/thecsw/MemePolice_bot
  | cd MemePolice_bot
  | mv example.config.py config.py
  | nano config.py
  `----

  After filling out the details, save and exit. You're done with
  installation.


3 Deployment
============

  Remove the word **'example'** from the title of all files with it.

  Just run this

  ,----
  | python __main__.py
  `----

  That is everything. All the prequelmemes will be identified. Once and
  for all, the archives will never be incomplete.


4 Source code
=============

  The code is heavily commented and all the important modules are being
  separated into different files. Looks pretty, dunno.


5 Built With
============

  1. [praw] is Python Reddit API Wrapper. This will be the main and only
     package to connect to Reddit's API and extract desired data.
  2. [python-opencv] is used for image transformations and computer
     vision problems.
  3. [pytesseract] is a python wrapper for Google's Tesseract-OCR.
  4. [tqdm] is used for fancy progress bars.
  5. [Pillow] is the Python Imaging Library by Fredrik Lundh and
     Contributors.


  [praw] https://github.com/praw-dev/praw

  [python-opencv] https://pypi.python.org/pypi/opencv-python

  [pytesseract] https://pypi.python.org/pypi/pytesseract

  [tqdm] https://pypi.python.org/pypi/tqdm

  [Pillow] https://pillow.readthedocs.io/en/latest/


6 Authors
=========

  - *Sagindyk Urazayev* - /Initial work/ - [thecsw]
  - *farhank3389* - /Fixes/ - [farhank3389]


  [thecsw] https://github.com/thecsw

  [farhank3389] https://github.com/farhank3389


7 License
=========

  This project is licensed under the The GNU General Public License (see
  the [LICENSE.md] file for details), it explains everything pretty
  well.


  [LICENSE.md]
  https://github.com/thecsw/prequelmemes_bot/blob/master/LICENSE
