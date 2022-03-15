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
        self.averageBidIncrease = 0

    def step(self):
        self.bidIncrease() # calculate new bid increase
        self.bidHistory += self.bids
        print(type(self.bids))
        self.bidHistory = self.sortBids()
        print(f'Second Highest Bid: {self.getSecondHighestBid()}')
        self.bids = [] # Resetting for next step

    def bidIncrease(self):
        #  if first bid(s) to be added
        if len(self.bids) !=0:
            if len(self.bidHistory) == 0:
                if (len(self.bids) < 1): # if first and unique, average bid increase is the new bid
                    self.averageBidIncrease = self.bids
                else: # if first and non- unique add first one then calculate average increment
                    self.averageBidIncrease = self.bids[0][1]
                    for i in range (1, len(self.bids)):
                         self.averageBidIncrease *= i
                         self.averageBidIncrease = abs(self.averageBidIncrease - self.bids[i][1])
                         self.averageBidIncrease /= i+1 
            else: # case for elements already added
                if (len(self.bids) < 1): # case that only one new bid id added
                    self.averageBidIncrease *= len(self.bidHistory)
                    self.averageBidIncrease = abs(self.averageBidIncrease - self.bids[0][1])
                    self.averageBidIncrease /=  len(self.bidHistory)+1
                else: # case that muktiple new bids are added 
                    for i in range (len(self.bids)):
                         self.averageBidIncrease *= (i + len(self.bidHistory)) 
                         self.averageBidIncrease = abs(self.averageBidIncrease - self.bids[i][1])
                         self.averageBidIncrease /= (i + len(self.bidHistory)+1)


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

    def getBidIncreaseAverage(self) -> int:
        return self.averageBidIncrease

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
                scalar = np.random.uniform(1.0, 1.2)
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
        self.bidAverage: float = 0

    def newBid(self):
        self.auctioneer.getSecondHighestBid()

    def step(self):
        prob_watch = np.random.uniform()
        # Check current price with probability = self.watchProba
        if (prob_watch < self.watchProba):
            if (self.auctionLength - self.currentTime < self.bidTimeframe):
                # Final bidTimeframe steps of the auction (snipers activated)
                if (self.valuation < self.auctioneer.getSecondHighestBid()):
                    self.valuation = min(self.auctioneer.getSecondHighestBid() + self.auctioneer.getBidIncreaseAverage() + 5, self.maxBid) # Update private valuation based on previous bid increases
                    # Generate probability (from uniform distribution)
                    proba = np.random.uniform()
                    if (proba < self.bidProba):
                        # Submit bid if probability < bidProba
                        self.auctioneer.bids.append((self, self.valuation))
                        print(f'Submitting bid: {self.valuation} (sniper bidder)')

        self.currentTime += 1