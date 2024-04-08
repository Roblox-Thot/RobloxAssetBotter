from requests import session

class Buyer:
    def __init__(self, cookie:str, asset:str|int):
        self.asset = asset
        self.session = session()
        self.session.cookies.set(".ROBLOSECURITY", cookie, domain=".roblox.com")
        self.session.headers

        # Debuging
        # req = self.session.get("https://users.roblox.com/v1/users/authenticated").text
        # print(req)
    
    def get_csrf(self) -> str:
        return self.session.post('https://auth.roblox.com/v1/login').headers['x-csrf-token']

