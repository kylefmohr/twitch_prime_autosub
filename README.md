This script will automatically subscribe to the Twitch streamer of your choice using your Twitch Prime subscription. It is intended to be used in combination with a cron job or a Windows Task Scheduler task to run it monthly.

For cron, you can use the following command to run it on the first day of every month at 12:00 AM:

```
0 0 1 * * python3 /path/to/twitch_prime_autosub.py
```
(replace `/path/to/twitch_prime_autosub.py` with the actual path to the script).

Make sure to install the package requirements:

```
pip install -r requirements.txt
```

You'll also need your Twitch cookies so that you don't need to enter your username and password. You can get them by logging into Twitch on your computer, installing an extension like [this one](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) for Chrome or [this one](https://addons.mozilla.org/en-US/firefox/addon/get-cookies-txt-locally/) for Firefox, then on the Twitch page, open the extension and click "Export". Then simply move the `www.twitch.tv_cookies.txt` file to the same directory as the script.

Don't forget to replace the `STREAMER_NAME` variable in the script with the name of the streamer you want to subscribe to.
