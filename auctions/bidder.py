from mesa import Agent

class Bidder(Agent):

    def __init__(self, unique_id, model, auctioneer, max_bid, internal_valuation, watch_proba, bid_proba):
        # Initialise the parent class with required parameters
        super().__init__(unique_id, model)
        self.auctioneer = auctioneer
        self.maxBid = max_bid
        self.valuation = internal_valuation
        self.watchProba = watch_proba
        self.bidProba = bid_proba
        self.isHighestBidder: bool = False