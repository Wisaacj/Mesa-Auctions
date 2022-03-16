from sklearn.metrics import roc_curve
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def load_data(file_path):
    csv_path = os.path.join(file_path, "results_legacy_bidincrease.csv")
    return pd.read_csv(csv_path)

bid_data = load_data("")

print(bid_data.info())
#print(bid_data["Highest Bidder"][bid_data["Highest Bidder"]== "SniperBidder"].value_counts())

sniperWins = bid_data["Highest Bidder"][bid_data["Highest Bidder"]== "SniperBidder"].value_counts()
earlyWins = bid_data["Highest Bidder"][bid_data["Highest Bidder"]== "EarlyBidder"].value_counts()

print("Sniper win ratio: ", sniperWins/1010000)
print("Early win ratio: ", earlyWins/1010000)

print("\n\n")

print("Total mean", np.mean(bid_data["Highest Bid"]))
print("Sniper mean", np.mean(bid_data["Highest Bid"][bid_data["Highest Bidder"]== "SniperBidder"]))
print("Early mean", np.mean(bid_data["Highest Bid"][bid_data["Highest Bidder"]== "EarlyBidder"]))

print("\n\n")

print("Snipers above 950: ", bid_data[(bid_data["Highest Bidder"]=="SniperBidder") & (bid_data["Highest Bid"]>950)])

sniper_above_avg = bid_data["Highest Bidder"][(bid_data["Highest Bidder"]=="SniperBidder") & (bid_data["Highest Bid"]>950)].value_counts()

print("Overpaid snipers: ",sniper_above_avg/sniperWins)