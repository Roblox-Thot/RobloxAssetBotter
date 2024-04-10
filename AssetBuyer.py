from requests import session

class Buyer:
    def __init__(self, cookie:str, asset:str|int, proxies:dict = None):
        """
        Initializes the AssetBuyer with the provided cookie and asset ID.

        Args:
            cookie (str): The user's authentication cookie.
            asset (str|int): The ID of the asset to be bought.
            proxies (dict): Proxy dict to use when buying.
        """

        self.asset = asset
        self.session = session()
        self.session.cookies.set(".ROBLOSECURITY", cookie, domain=".roblox.com")
        # self.session.headers
        if proxies: self.session.proxies.update(proxies)

        # Debugging
        # req = self.session.get("https://users.roblox.com/v1/users/authenticated").text
        # print(req)
    
    def get_csrf(self) -> str:
        """
        Returns the CSRF token required for authentication.

        Returns:
            str: The CSRF token.
        """

        return self.session.post('https://auth.roblox.com/v1/login').headers['x-csrf-token']
