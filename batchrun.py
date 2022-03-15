from mesa.batchrunner import batch_run, BatchRunner
from mesa.datacollection import DataCollector
from auctions.agents import Auctioneer, EarlyBidder, SniperBidder
from auctions.model import AuctionHouse
import pandas as pd

params = {
    "snipers": 3,
    "earlyBidders": 7,
    "maxValueStandardDeviation": 250,
    "bidProba": 0.75,
    "watchProba": 0.75,
    "bidTimeframe": 20,
    "auctionLength": 100
}

"""
results = batch_run(
    AuctionHouse,
    parameters=params,
    iterations=1,
    number_processes=1,
    data_collection_period=2,
    display_progress=True
)

results_df = pd.DataFrame(results)
results_df.to_csv("results.csv")
"""

br = BatchRunner(
    AuctionHouse,
    fixed_parameters=params,
    iterations=100,
    max_steps=100,
    model_reporters={"Data Collector": lambda m: m.datacollector},
)

br.run_all()
br_df = br.get_model_vars_dataframe()

br_step_data = pd.DataFrame()
for i in range(len(br_df["Data Collector"])):
    if isinstance(br_df["Data Collector"][i], DataCollector):
        i_run_data = br_df["Data Collector"][i].get_model_vars_dataframe()
        br_step_data = br_step_data.append({"Highest Bid": "NEW EPOCH", "Highest Bidder": "NEW EPOCH", "Second Highest Bid": "NEW EPOCH", "Second Highest Bidder": "NEW EPOCH"}, ignore_index=True)
        br_step_data = br_step_data.append(i_run_data, ignore_index=True)
        
br_step_data.to_csv("results_legacy.csv")

