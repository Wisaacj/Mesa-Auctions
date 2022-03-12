from auctions.agents import Auctioneer, EarlyBidder, SniperBidder
from auctions.bidder import Bidder
from mesa import Model, Agent
from mesa.datacollection import DataCollector
from mesa.time import BaseScheduler
from auctions.schedulers import RandomActivationByType
import numpy as np

def getHighestBid(model) -> int:
    return model.auctioneer.getHighestBid()

def getHighestBidder(model) -> Bidder:
    return model.auctioneer.getHighestBidder()

def getSecondHighestBid(model) -> int:
    return model.auctioneer.getSecondHighestBid()

def getSecondHighestBidder(model) -> Bidder:
    return model.auctioneer.getSecondHighestBidder()

class AuctionHouse(Model):

    def __init__(self, snipers, earlyBidders, maxValueStandardDeviation, bidProba, watchProba, bidTimeframe, auctionLength):
        self.snipers: int = snipers
        self.earlyBidders: int = earlyBidders
        self.maxValueStandardDeviation: int = maxValueStandardDeviation
        self.bidProba: float = bidProba
        self.watchProba: float = watchProba
        self.bidTimeframe: int = bidTimeframe
        self.auctionLength: int = auctionLength
        self.schedule: BaseScheduler = RandomActivationByType(self)

        self.datacollector = DataCollector(
            model_reporters = {
                "Highest Bid": getHighestBid,
                "Highest Bidder": getHighestBidder,
                "Second Highest Bid": getSecondHighestBid,
                "Second Highest Bidder": getSecondHighestBidder
            }
        )

        """ 
        AGENTS:
        -> Agents have a maxBid value generated from a normal distribution with properties:
        ---> Mean = 100, standard dev. = maxValueStandardDeviation

        -> Agents have a valuation value generated from a normal distribution with properties:
        ---> Mean = 100 - maxValueStandardDeviation, standard dev. = maxValueStandardDeviation
        """

        # Creating auctioneer agent
        self.auctioneer: Agent = Auctioneer(0, self)
        self.schedule.add(self.auctioneer)
        print("Agent 0")

        # Creating early bidder agents
        for i in range(self.earlyBidders):
            # Generating normally-distributed maxBid with mean = 1000
            maxBid = np.random.normal(1000, self.maxValueStandardDeviation)
            # Generating normally-distributed private valuation with mean = 500
            valuation = np.random.normal(500, self.maxValueStandardDeviation)

            print(f'Agent: {i+1}')
            a = EarlyBidder(i+1, self, self.auctioneer, maxBid, valuation, self.watchProba, self.bidProba)
            self.schedule.add(a)

        # Creating sniper bidder agents
        for i in range(self.snipers):
            # Generating normally-distributed maxBid with mean = 1000
            maxBid = np.random.normal(1000, self.maxValueStandardDeviation)
            # Generating normally-distributed private valuation with mean = 500
            valuation = np.random.normal(500, self.maxValueStandardDeviation)

            print(f'Agent {i+1+self.earlyBidders}')
            a = SniperBidder(i+1+self.earlyBidders, self, self.auctioneer, maxBid, valuation, self.watchProba, self.bidProba, self.bidTimeframe, self.auctionLength)
            self.schedule.add(a)

        self.running: bool = True
        self.datacollector.collect(self)
        
    def step(self):
        # Tell all bidding agents to run their step function
        self.schedule.step_type(EarlyBidder)
        self.schedule.step_type(SniperBidder)
        # Tell auctioneer to run its step function
        self.schedule.step_type(Auctioneer)
        # Collect data
        self.datacollector.collect(self)

    def run_model(self):
        for i in range(self.auctionLength):
            self.step()