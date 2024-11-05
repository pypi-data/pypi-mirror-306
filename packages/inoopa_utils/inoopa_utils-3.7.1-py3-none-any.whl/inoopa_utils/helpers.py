import requests
from tldextract import extract
from functools import lru_cache


def extract_domain(url: str) -> str:
    """
    Extract the domain from a url. We dedicate a function here to make sure we do it the same way everywhere.

    ex: https://www.inoopa.com/contact -> inoopa.com
    """
    # if http is not present, we can't parse the domain
    if "https://" in url and "http://" not in url:
        url = "http://" + url
    return extract(url).registered_domain


@lru_cache
def get_latest_user_agent(operating_system: str = "macintosh", browser: str = "safari") -> str:
    print("in")
    """General function to fetch the latest user agent for a given operating system and browser."""
    # Daily updated list of user agents
    url = "https://jnrbsn.github.io/user-agents/user-agents.json"
    r = requests.get(url)
    r.raise_for_status()
    user_agents = r.json()

    for user_agent in user_agents:
        user_agent = user_agent.lower()
        if operating_system.lower() in user_agent and browser.lower() in user_agent:
            return user_agent
    raise ValueError(f"No user-agent found for OS: {operating_system} and browser: {browser}")
