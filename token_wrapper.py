import brownie

class Token:
    def __init__(self, address: str, oracle_address: str) -> None:
        self.address = brownie.convert.to_address(address) ##checksum to allow address comparisons
        try:
            self.contract = brownie.Contract(address)
        except:        
            self.contract = brownie.Contract.from_explorer(address)
        
        self.symbol = self.contract.symbol()    
        if type(self.symbol) == brownie.convert.datatypes.HexString:
            self.symbol = self.symbol.decode()
        
        self.name = self.contract.name()    
        if type(self.name) == brownie.convert.datatypes.HexString:
            self.name = self.name.decode()
            
        self.decimals = self.contract.decimals()
        
        try:
            self._oracle_contract = brownie.Contract(oracle_address)
        except:            
            self._oracle_contract = brownie.Contract.from_explorer(oracle_address)            

        self.update_price()
        print(f"* {self.symbol} ({self.name}): ${self.price}")
    
    def update_price(self) -> None:
        try:
            self.price: float = self._oracle_contract.latestRoundData()[1] / (10**self._oracle_contract.decimals())
        except:
            pass
