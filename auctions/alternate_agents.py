from collections import defaultdict
from mesa import Agent
from auctions.bidder import Bidder
import numpy as np

"""These Agents do not employ the average bid increase strategy"""

class AAuctioneer(Agent):
    
    def __init__(self, unique_id, model):
        # Initialise the parent class with required parameters
        super().__init__(unique_id, model)
        self.bidHistory: list = [] # List of tuples, e.g., (Agent, valuation): (Bidder, int)
        self.bids: list = [] # List to hold bids sent by agents _during_ a step

    def __str__(self):
        return "Auctioneer"

    def step(self):
        self.bidHistory += self.bids
        self.bidHistory = self.sortBids()
        # print(f'Second Highest Bid: {self.getSecondHighestBid()}')
        self.bids = [] # Resetting for next step

    def sortBids(self) -> list:
        # Sorted by second item in each tuple (in descending order)
        return sorted(self.bidHistory, key=lambda x: x[1], reverse=True)

    def getHighestBid(self) -> int:
        if len(self.bidHistory) < 1:
            return 0

        return self.bidHistory[0][1]

    def getHighestBidder(self) -> Bidder:
        if len(self.bidHistory) < 1:
            return None

        return self.bidHistory[0][0]

    def getSecondHighestBid(self) -> int:
        if len(self.bidHistory) < 2:
            return self.getHighestBid()

        return self.bidHistory[1][1]

    def getSecondHighestBidder(self) -> Bidder:
        if len(self.bidHistory) < 2:
            return self.getHighestBidder()

        return self.bidHistory[1][0]

class ASniperBidder(Bidder):
    
    def __init__(self, unique_id, model, auctioneer, maxBid, valuation, watchProba, bidProba, bidTimeframe, auctionLength):
        # Initialise the parent class with required parameters
        super().__init__(unique_id, model, auctioneer, maxBid, valuation, watchProba, bidProba)
        self.bidTimeframe: int = bidTimeframe # Snipers only bid when currentTime is within the final bidTimeframe steps of the auctions
        self.auctionLength: int = auctionLength
        self.currentTime: int = 1 # To be incremented at each step

    def __str__(self):
        return "SniperBidder"

    def step(self):
        if (self.auctionLength - self.currentTime < self.bidTimeframe):
            # Final bidTimeframe steps of the auction (snipers activated)
            if (self.valuation < self.auctioneer.getSecondHighestBid()):
                scalar = np.random.uniform(1.0, 2.0)
                # Update private valuation (by multiplying by scalar drawn from uniform distribution) note this distribution has a larger range than the one used for EarlyBidder
                self.valuation = min(self.auctioneer.getSecondHighestBid() * scalar, self.maxBid) # Update private valuation
                # Generate probability (from uniform distribution)
                proba = np.random.uniform()
                if (proba < self.bidProba):
                    # Submit bid if probability < bidProba
                    self.auctioneer.bids.append((self, self.valuation))
                    # print(f'Submitting bid: {self.valuation} (sniper bidder)')

        self.currentTime += 1