from dataclasses import dataclass, field
from pygnmi.client import gNMIclient
from enum import auto, Enum
import json
import logging
import datetime



@dataclass
class Cards:
    context: str 
    slot: int
    admin_state: str
    card_type: str

@dataclass
class Fp:
    context: str 
    slot: int
    fp: int

@dataclass
class Mda:
    context: str 
    slot: int
    mda_slot: int
    mda_type: str

def append_to_discovered(discovered_array,snippet):
    
    snippet_as_dictionary = snippet.__dict__ 
    cleaned_snippet={k: v for k, v in snippet_as_dictionary.items() if v != None}
    discovered_array.append(cleaned_snippet)

if __name__ == '__main__':
    host=("10.85.112.162","57400")
    Discovery=[]

    logging.basicConfig(filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')

    start_time=datetime.datetime.now()
    with gNMIclient(target=host,username="admin",password="admin",insecure=True) as gc:
        
        try:
            data=gc.get(path=[f"/configure/card"],datatype="config")
            main_array=data["notification"][0]["update"]
            
           
            for card_item in main_array:
                
                main=card_item["val"]

                json_snippet=Cards(
                    context="cards",
                    slot=main["slot-number"],
                    admin_state=main["admin-state"],
                    card_type=main["card-type"])
                append_to_discovered(Discovery,json_snippet)

                if "mda" in main:
                    mdas=main["mda"]
                    for item in mdas:
                        json_snippet=Mda(
                        context="mda",
                        mda_slot=item["mda-slot"],
                        mda_type=item["mda-type"],
                        slot=main["slot-number"])
                        append_to_discovered(Discovery,json_snippet)
                
                if "fp" in main:
                    fps=main["fp"]
                    for item in fps:
                        json_snippet=Fp(
                        context="fp",
                        slot=1,
                        fp=item["fp-number"]) 
                        append_to_discovered(Discovery,json_snippet)

        except Exception as e:
                logging.error(f"An error occurred: {e}")

    end_time=datetime.datetime.now()
    print(f"time elapsed: {end_time - start_time}")
    print(Discovery)

                
