from mesa.batchrunner import BatchRunner
from mesa.datacollection import DataCollector
from auctions.agents import Auctioneer, EarlyBidder, SniperBidder
from auctions.model import AuctionHouse
import pandas as pd

"""
When running batch-run, comment out all print statements in model.py and agents.py
as this will drastically reduce the computation time.
"""

params = {
    "snipers": 7,
    "earlyBidders": 7,
    "maxValueStandardDeviation": 250,
    "bidProba": 0.75,
    "watchProba": 0.75,
    "bidTimeframe": 20,
    "auctionLength": 100
}

br = BatchRunner(
    AuctionHouse,
    fixed_parameters=params,
    iterations=10000,
    max_steps=100,
    model_reporters={"Data Collector": lambda m: m.datacollector},
)

br.run_all()
br_df = br.get_model_vars_dataframe()

br_step_data = pd.DataFrame()
for i in range(len(br_df["Data Collector"])):
    if isinstance(br_df["Data Collector"][i], DataCollector):
        i_run_data = br_df["Data Collector"][i].get_model_vars_dataframe()
        br_step_data = br_step_data.append(i_run_data, ignore_index=True)
        
br_step_data.to_csv("data/same_sniper_early_bid increase.csv")