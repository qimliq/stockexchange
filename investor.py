class Investor:
    asset_list = []
    capital = 0
    id = None
    money_in_stock = 0

    def __init__(self, id, cap):
        self.id = id
        self.capital = cap

    def add_asset(self,asset):
        for iasset in self.asset_list:
            if iasset.name == asset.name:
                return
        self.asset_list.append(asset)