from requests import session
from copy import copy
class Buyer:
    def __init__(self, asset:str|int, proxies:dict = None):
        """
        Initializes the AssetBuyer with the provided cookie and asset ID.

        Args:
            asset (str|int): The ID of the asset to be bought.
            proxies (dict): Proxy dict to use when buying.
        """

        self.session = session()
        if proxies: self.session.proxies.update(proxies)

        self.asset_id = asset
        self.product_info = self.session.get(f'https://apis.roblox.com/toolbox-service/v1/items/details?assetIds={self.asset_id}').json()['data'][0]
        # sourcery skip: raise-specific-error
        if not self.product_info['product']['isForSaleOrIsPublicDomain']: raise Exception("Not on sale")
        self.product_id = self.product_info['product']['productId']
        self.asset_type = self.product_info['asset']['typeId']
        self.asset_price = self.product_info['product']['price']
        print(self.product_id,self.asset_type)
    
    def get_csrf(self) -> str:
        """
        Returns the CSRF token required for authentication.

        Returns:
            str: The CSRF token.
        """

        return self.session.post('https://auth.roblox.com/v1/login').headers['x-csrf-token']
    
    def set_cookie(self, cookie:str) -> None:
        """
        Sets the authentication cookie for buying.

        Args:
            cookie (str): The user's authentication cookie.
        """
        self.session.cookies.set(".ROBLOSECURITY", cookie, domain=".roblox.com")
        # Debugging
        # req = self.session.get("https://users.roblox.com/v1/users/authenticated").text
        # print(req)

    def buy(self) -> None:
        self.session.post("https://apis.roblox.com/creator-marketplace-purchasing-service/v1/products/1781152104/purchase",
                            headers={},
                            params={'assetId':16802935104,'assetType':10,'expectedPrice':0,'searchId':None})

    def delete(self) -> None:
        self.session.post('https://www.roblox.com/asset/delete-from-inventory',
                            headers={},
                            params={"assetId":self.asset_id})

if '__main__' in __name__:        
    # test1 = Buyer(339406852)
    # test2 = copy(test1)
    # test2.set_cookie("hi")
    # test3 = copy(test1)
    # test3.set_cookie("bye")
    test1 = Buyer(339406852)