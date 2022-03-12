from collections import defaultdict
from mesa import Agent
from auctions.bidder import Bidder
import numpy as np

class Auctioneer(Agent):
    
    def __init__(self, unique_id, model):
        # Initialise the parent class with required parameters
        super().__init__(unique_id, model)
        self.bidHistory: list = [] # List of tuples, e.g., (Agent, valuation): (Bidder, int)
        self.bids: list = [] # List to hold bids sent by agents _during_ a step

    def step(self):
        self.bidHistory += self.bids
        self.sortBids()
        print(f'Second Highest Bid: {self.getSecondHighestBid()}')
        self.bids = [] # Resetting for next step

    def sortBids(self) -> list:
        # Sorted by second item in each tuple (in descending order)
        return sorted(self.bidHistory, key=lambda x: x[1])

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

"""
Properties of bidder classes:
- maxBid: L (from research paper)
- valuation: v (from research paper)
- watchProba: w (from research paper)
- bidProba: b (from research paper)
"""

class EarlyBidder(Bidder):
    
    def __init__(self, unique_id, model, auctioneer, maxBid, valuation, watchProba, bidProba):
        # Initialise the parent class with required parameters
        super().__init__(unique_id, model, auctioneer, maxBid, valuation, watchProba, bidProba)

    def step(self):
        secondHighestBid = self.auctioneer.getSecondHighestBid()
        prob_watch = np.random.uniform()
        # Check current price with probability = self.watchProba
        if (prob_watch < self.watchProba):
            # If outbid at current timestep
            if (self.valuation < secondHighestBid or secondHighestBid == 0):
                scalar = np.random.uniform(1.2, 2.0)
                # Update private valuation (by multiplying by scalar drawn from uniform distribution)
                self.valuation = min(scalar * self.valuation, self.maxBid)
                if (self.valuation > secondHighestBid):
                    # Generate probability (from uniform distribution)
                    proba = np.random.uniform()
                    if (proba < self.bidProba):
                        # Submit with probability = self.bidProba
                        self.auctioneer.bids.append((self, self.valuation))
                        print(f'Submitting bid: {self.valuation} (early bidder)')

class SniperBidder(Bidder):
    
    def __init__(self, unique_id, model, auctioneer, maxBid, valuation, watchProba, bidProba, bidTimeframe, auctionLength):
        # Initialise the parent class with required parameters
        super().__init__(unique_id, model, auctioneer, maxBid, valuation, watchProba, bidProba)
        self.bidTimeframe: int = bidTimeframe # Snipers only bid when currentTime is within the final bidTimeframe steps of the auctions
        self.auctionLength: int = auctionLength
        self.currentTime: int = 1 # To be incremented at each step

    def step(self):
        prob_watch = np.random.uniform()
        # Check current price with probability = self.watchProba
        if (prob_watch < self.watchProba):
            if (self.auctionLength - self.currentTime < self.bidTimeframe):
                # Final bidTimeframe steps of the auction (snipers activated)
                self.valuation = min(self.auctioneer.getSecondHighestBid() * 2, self.maxBid) # Update private valuation
                # Generate probability (from uniform distribution)
                proba = np.random.uniform()
                if (proba < self.bidProba):
                    # Submit bid if probability < bidProba
                    self.auctioneer.bids.append((self, self.valuation))
                    print(f'Submitting bid: {self.valuation} (sniper bidder)')

        self.currentTime += 1