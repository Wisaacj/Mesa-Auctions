from collections import defaultdict
from mesa import Agent
from auctions.bidder import Bidder
import numpy as np

class Auctioneer(Agent):
    
    def __init__(self, unique_id, model):
        # Initialise the parent class with required parameters
        super().__init__(unique_id, model)
        self.highestBid: int = 0
        self.highestBidder: Bidder = None
        self.secondHighestBid: int = 0
        self.secondHighestBidder: Bidder = None
        self.bids: defaultdict = {} # Bidder-bid pair
        self.currentTime: int = 1

    def step(self):
        if (not len(self.bids) == 0):
            # Finding highest Bidder-bid pair
            highBidder = max(self.bids, key=self.bids.get)
            highBid = self.bids[highBidder]

            # Checking if there's a new highest bidder
            if (highBid > self.highestBid):
                self.highestBidder = highBidder
                self.highestBid = highBid
                self.highestBidder.isHighestBidder = True # Letting the highest bidder know they are the highest bidder
            elif (highBid > self.secondHighestBid): # Checking if there's a new second highest bidder
                self.secondHighestBidder = highBidder
                self.secondHighestBid = highBid
            
            # Removing highest Bidder-bid pair from dictionary
            self.bids.pop(highBidder)

            if (not len(self.bids) == 0):
                # Finding second highest Bidder-bid pair
                secondHighBidder = max(self.bids, key=self.bids.get)
                secondHighBid = self.bids[secondHighBidder]

                if (secondHighBid > self.secondHighestBid):
                    self.secondHighestBidder = secondHighBidder
                    self.secondHighBid = secondHighBid
            
            # Resetting bids dictionary for next step
            self.bids = {}

        self.currentTime += 1

    def sortBids(bidList) -> list:
        pass

    def getSecondHighestBid(self) -> int:
        return self.secondHighestBid

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
                        self.auctioneer.bids[self] = self.valuation
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
                    self.auctioneer.bids[self] = self.valuation
        self.currentTime += 1