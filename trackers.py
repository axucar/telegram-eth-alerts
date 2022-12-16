import sys
import eth_abi
from collections import deque
import asyncio
import asyncio.locks
import json
import websockets
import brownie
import telegram.constants
import config as cfg
import time

##For details on subscribing to JSON-RPC notifications : https://geth.ethereum.org/docs/rpc/pubsub
## event types: newHeads, logs (filter for emitted Events), pendingTransactions
async def track_eth_transfers(usd_threshold=0):
    async for websocket in websockets.connect(uri=brownie.web3.provider.endpoint_uri):        
        try:
            await websocket.send(json.dumps(
                    {
                        "id": 1,
                        "method": "eth_subscribe",
                        "params": ["newHeads"],
                    }))
            subscribe_result = await websocket.recv()
            print("Tracking ETH transfers: " + subscribe_result)

            while True:            
                try:                                                      
                    message = json.loads(await websocket.recv())                                  
                    block_number = int(message.get("params").get("result").get("number"),16)                                        
                    block_tx_data = brownie.web3.eth.get_block(block_number,full_transactions=True).get("transactions")
                    
                          
                    for tx_data in block_tx_data:
                        if not tx_data.get("to"): continue #contract creation, skip                        
                        
                        ##filter on transfer value   
                        cfg.weth.update_price()                                                
                        eth_transfer_value = tx_data.get("value")/(10**18)
                        usd_transfer_value = eth_transfer_value*cfg.weth.price
                        if usd_transfer_value <= usd_threshold: continue
                        
                        ##get to, from addresses
                        tx_hash = tx_data.get("hash").hex()                       
                        to_address = brownie.convert.to_address(tx_data.get("to"))
                        from_address = brownie.convert.to_address(tx_data.get("from"))
                        
                        ##MATCH "to" and "from"
                        if (to_address in cfg.WALLETS_TRACKED):
                            wallet = cfg.WALLETS_TRACKED[to_address]
                            sent_or_received = "received (+)"
                        elif (from_address in cfg.WALLETS_TRACKED):
                            wallet = cfg.WALLETS_TRACKED[from_address]
                            sent_or_received = "sent (-)"
                        else: continue

                        output=f'{tx_hash}:{wallet} {sent_or_received} {eth_transfer_value} ETH (${usd_transfer_value:0,.2f})'
                        print(output)
                        
                        if not cfg.SILENCE:                        
                            telegram_output = f"ETH Transfer: `{wallet}` *{sent_or_received}* "\
                                                f"`{eth_transfer_value} ETH` "\
                                                f"(${usd_transfer_value:0,.2f}) "
                            telegram_output=telegram_output.replace(".","\.").replace("(","\(").replace(")","\)").replace("+","\+").replace("-","\-")
                            telegram_output+=f"[Etherscan](https://etherscan.io/tx/{tx_hash})"
                            await cfg.application.bot.send_message(cfg.USER_ID,telegram_output,disable_web_page_preview=True,parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)

                except websockets.WebSocketException:
                    break  # escape the while loop to reconnect websocket
                except Exception as e:                
                    print(f"Exception in ETH transfer tracking: {e}")     
        
        except websockets.WebSocketException:
            print("Reconnecting websocket...")
            continue
        except Exception as e:
            print(f"Exception in ETH transfer tracking: {e}")     


async def track_erc20_transfers(usd_threshold=0):
    
    async for websocket in websockets.connect(uri=brownie.web3.provider.endpoint_uri):
        try:
            await websocket.send(
                json.dumps(
                    {
                        "id": 1,
                        "method": "eth_subscribe",
                        "params": ["logs",{"topics": [brownie.web3.keccak(text="Transfer(address,address,uint256)").hex()]}],
                    }))

            subscribe_result = await websocket.recv()
            print("Tracking ERC20 transfers: " + subscribe_result)

            while True:
                try:
                    message = json.loads(await websocket.recv())   
                    erc20_address = brownie.convert.to_address(message.get("params").get("result").get("address"))
                    
                    if erc20_address in cfg.token_dict.keys():          
                        ##filter on transfer value               
                        token = cfg.token_dict[erc20_address]
                        token.update_price()
                        event_data = message.get("params").get("result").get("data")
                        transfer_value = eth_abi.decode_single("uint256",bytes.fromhex(event_data[2:])) #Data for Transfer events is only wad                        
                        usd_transfer_value = (transfer_value/(10**token.decimals))*token.price
                        if usd_transfer_value <= usd_threshold: continue

                        ##get to, from addresses
                        tx_hash = message.get("params").get("result").get("transactionHash")
                        _ , raw_from_address, raw_to_address = message.get("params").get("result").get("topics")
                        to_address = brownie.convert.to_address(eth_abi.decode_single("address",bytes.fromhex(raw_to_address[2:])))
                        from_address = brownie.convert.to_address(eth_abi.decode_single("address",bytes.fromhex(raw_from_address[2:])))
            
                        ##MATCH "to" or "from"
                        if (to_address in cfg.WALLETS_TRACKED):
                            wallet = cfg.WALLETS_TRACKED[to_address]
                            sent_or_received = "received (+)"
                        elif (from_address in cfg.WALLETS_TRACKED):
                            wallet = cfg.WALLETS_TRACKED[from_address]
                            sent_or_received = "sent (-)"
                        else: continue

                        output=f'{tx_hash}:{wallet} {sent_or_received} {transfer_value/10**token.decimals} {token.symbol} (${usd_transfer_value:0,.2f})'
                        print(output)
                        
                        if not cfg.SILENCE:                        
                            telegram_output = f"ERC20 Transfer: `{wallet}` *{sent_or_received}* "\
                                                f"`{transfer_value/10**token.decimals} {token.symbol}` "\
                                                f"(${usd_transfer_value:0,.2f}) "
                            telegram_output=telegram_output.replace(".","\.").replace("(","\(").replace(")","\)").replace("+","\+").replace("-","\-")
                            telegram_output+=f"[Etherscan](https://etherscan.io/tx/{tx_hash})"
                            await cfg.application.bot.send_message(cfg.USER_ID,telegram_output,disable_web_page_preview=True,parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)

                except websockets.WebSocketException:
                    break  # escape the loop to reconnect
                except Exception as e:
                    print(f"Exception in ERC20 transfer tracking: {e}")     

        except websockets.WebSocketException:
            print("reconnecting...")
            continue
        except Exception as e:
            print(f"Exception in ERC20 transfer tracking: {e}")     


