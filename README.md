WalletStatus
============

Emails balance changes for your coin. Data is parsed from a site running Abe Block Explorer. Useful for wallets you are mining to like from a P2Pool.

Right now there is a bug when the page has a timeout (HTTP 504) and can affect the balance incorrectly. Need to add a check for HTTP status and or the data is valid.

Other than that it works great, just configure your wallets you want to track and make sure each array has the same amount of elements that zero as the starting value.

Finally fill in your SMTP settings.

Requires BeatifulSoup4 and SMTPLIB



