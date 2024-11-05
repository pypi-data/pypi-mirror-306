from .models import BrowserSettings, BrowserSettings, BrowserConfig


# Default configuration
DEFAULT_BROWSER_CONFIG = BrowserConfig(
    type="chrome",
    settings=BrowserSettings(
        os=["linux"],
        devices=["mobile"],
        screen={
            "max_width": 1920,
            "max_height": 1080,
            "min_width": 320,
            "min_height": 240
        },
        locales=["en-US"]
    ),
    block_ads=True,
    proxy=True
)
