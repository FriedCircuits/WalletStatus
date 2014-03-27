WalletStatus
============

Emails balance changes for your coin. Data is parsed from a site running Abe Block Explorer. Useful for wallets you are mining to like from a P2Pool.

Includes error handling of failed attempts to fetch data from site. If there is a partial success then email will still be sent and failed count be at the bottom of the email. Command prompt output will give you more detials during and at the end of each run. 

Orginally I was going also pool stats from a P2Pool status page, but you can ignore the code for now.

Orginally I created this while mining Vertcoin but should work for any coin that has a site runing ABE Block Exploere from https://github.com/bitcoin-abe/bitcoin-abe


Things to configure 

Wallets you want to track and make sure each array has the same amount of elements with zero as the starting value.

Email SMTP settings: Doesn't have to be GMAIL, just any SMTP server will do

Address of block exporer and URL to balance using API



Requires BeatifulSoup4 and SMTPLIB

Code is based on my previous work for checking stock status which can be found here:
https://github.com/FriedCircuits/Stock_Checker



License: All source code and designs are released under 

Creative Commons - By - ShareAlike 

CC BY-SA

![CC BY-SA](http://i.creativecommons.org/l/by-sa/3.0/88x31.png)





