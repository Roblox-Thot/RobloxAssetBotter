from requests import session
from copy import copy
from time import sleep

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
        self.csrf = None
    
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
        self.csrf = self.get_csrf()
        # Debugging
        # req = self.session.get("https://users.roblox.com/v1/users/authenticated").text
        # print(req)
    
    def set_proxy(self, proxies:dict) -> None:
        if proxies: self.session.proxies.update(proxies)

    def buy(self) -> None:
        self.csrf = self.get_csrf()
        response = self.session.post(f'https://apis.roblox.com/creator-marketplace-purchasing-service/v1/products/{self.product_id}/purchase',
                            headers={'x-csrf-token':self.csrf},
                            json={'assetId':self.asset_id,'assetType':10,'expectedPrice':0})
        
        print('buy',response,response.text)
        if response.status_code == 500:
            sleep(2)
            self.buy()

    def delete(self) -> None:
        response = self.session.post('https://www.roblox.com/asset/delete-from-inventory',
                            headers={'x-csrf-token':self.csrf},
                            params={"assetId":self.asset_id})
        print('delete',response,response.text)
        if response.status_code == 429:
            sleep(10)
            self.delete()
        

if '__main__' in __name__:        
    # test1 = Buyer(339406852)
    # test2 = copy(test1)
    # test2.set_cookie("hi")
    # test3 = copy(test1)
    # test3.set_cookie("bye")
    test1 = Buyer(7216266159)
    while True:
        sleep(1)
        test1.buy()
        test1.delete()