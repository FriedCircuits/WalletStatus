WalletStatus
============

Emails balance changes for your coin. Data is parsed from a site running Abe Block Explorer. Useful for wallets you are mining to like from a P2Pool.

Right now there is a bug when the page has a timeout (HTTP 504) and can affect the balance incorrectly. Need to add a check for HTTP status and or the data is valid.

Orginally I was going also pool stats from a P2Pool status page, but you can ignore the code for that.

Other than that it works great, 

Things to configure 

Wallets you want to track and make sure each array has the same amount of elements that zero as the starting value.

Email SMTP settings.

Address of block exporer



Requires BeatifulSoup4 and SMTPLIB

Code is based on my previous work for checking stock status which can be found here:
https://github.com/FriedCircuits/Stock_Checker



License: All source code and designs are released under 

Creative Commons - By - ShareAlike 

CC BY-SA

![CC BY-SA](http://i.creativecommons.org/l/by-sa/3.0/88x31.png)





