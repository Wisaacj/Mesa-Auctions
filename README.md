# ABM: Second-Price Auctions

## Repository Architecture

> root - Contains run.py and batch-run.py for running the webserver visualisation / generating datasets respectively

> analysis - Contains data analysis notebooks used for the hypothesis analysis section of the report

> auctions - Contains the whole agent-based model of second price auctions

> images - Contains images used in the report

## Model Design

1. maxBid drawn from a normal distribution with mean = 1000, standard deviation = (user inputted)
2. valuation drawn from a normal distribution with mean = 500, standard deviation = (user inputted)
3. EarlyBidder bids are updated by a scalar factor drawn from uniform distribution [1.0, 1.2]
     + min(self.valuation * scalar, self.valuation)
4. Naive SniperBidder bids are updated by a scalar factor drawn from uniform distribution [1.0, 2.0]
     + min(self.valuation * scalar, self.maxBid)
5. Intelligent SniperBidder bids are updated by the average bid increase (observed over the whole auciton)
     + min(self.auctioneer.getSecondHighestBid() + self.auctioneer.getBidIncreaseAverage() + 5, self.maxBid)
