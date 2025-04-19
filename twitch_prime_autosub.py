import asyncio
import os, time
import nodriver
from nodriver import cdp

# change this to the Twitch streamer you want to subscribe to
STREAMER_NAME = "gooffkings"

# if you have never subscribed to this streamer before, change this to "Subscribe", else leave it as is.
BUTTON_TEXT = "Resubscribe"

async def load_cookies(tab):
    """Load cookies from .txt files in the current directory."""
    cookies = []
    for file in os.listdir("."):
        if file.endswith("cookies.txt"):
            with open(file, "r") as f:
                cookies_from_file = f.read().splitlines()
                for cookie in cookies_from_file:
                    cookie = cookie.strip()
                    if cookie.startswith("#") or not cookie:
                        continue
                    parts = cookie.split('\t')
                    if len(parts) < 3:
                        continue  # not enough data
                    # Create cookie with minimal required fields similar to main.py
                    cookies.append(cdp.network.CookieParam(
                        name=parts[-2],
                        value=parts[-1],
                        expires=int(parts[-3])
                    ))
    
    if cookies:
        # Clear existing cookies first
        await tab.send(cdp.storage.clear_cookies())
        
        for cookie in cookies:
            await tab.send(cdp.network.set_cookie(
                name=cookie.name,
                value=cookie.value,
                url="https://www.twitch.tv"
            ))
        
        print(f"Loaded {len(cookies)} cookies.")
    else:
        print("No cookies found to load.")

async def main():
    try:
        # Start a browser
        driver = await nodriver.start(headless=True)
        
        # Navigate to the Twitch channel using the driver.get method, which returns a tab
        tab = await driver.get("https://www.twitch.tv/" + STREAMER_NAME)
        
        # Load cookies
        await load_cookies(tab)
        
        # Refresh to apply cookies
        await tab.reload()
        
        # Wait for the page to load
        await tab.sleep(3)  # Wait 3 seconds for page to load fully
        print("Page loaded successfully.")
        
        # Find and click the subscribe button
        subscribe_button = await tab.find(BUTTON_TEXT, best_match=True)
        if subscribe_button:
            print("Found subscribe/resubscribe button.")
            await subscribe_button.click()
            print("Button clicked.")
        else:
            button = await tab.find("Gift a sub", best_match=True)
            if button:
                print("Found 'Gift a sub' button instead, you're probably already subscribed.")
                return
            else:
                print("Couldn't find the subscribe button or 'Gift a sub' button.")
                if BUTTON_TEXT == "Resubscribe":
                    BUTTON_TEXT = "Subscribe"
                else:
                    BUTTON_TEXT = "Resubscribe"
                button = await tab.find(BUTTON_TEXT, best_match=True)
                if button:
                    print(f"Found {BUTTON_TEXT} button, clicking it.")
                    await button.click()
                else:
                    print("No subscribe button found at all.")
                    return
        print("Subscribe button clicked, waiting for subscription modal to appear.")
        
        # Wait for the subscription modal to appear
        await tab.sleep(2)  # Short wait for modal to appear
        
        # Find and click the Use Prime Sub checkbox
        prime_checkbox = await tab.find("Use Prime", best_match=True)
        if prime_checkbox:
            print("Found Prime checkbox.")
            await prime_checkbox.click()
            print("Prime checkbox clicked.")
        else:
            print("Prime checkbox not found.")
            return
        
        # Find and click the confirm button (Subscribe with Prime)
        confirm_button = await tab.find("Subscribe with Prime", best_match=True)
        if confirm_button:
            print("Found confirm button.")
            await confirm_button.click()
            print("Confirm button clicked.")
        else:
            print("Confirm button not found.")
            return
        
        # Wait for subscription to complete
        await tab.sleep(5)
        print("Subscription process completed.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Use nodriver.loop() to run the main function
    nodriver.loop().run_until_complete(main())
