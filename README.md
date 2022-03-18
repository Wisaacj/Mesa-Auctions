# ABM: Second-Price Auctions

Auctions have existed for millennia, dating back to the Ancient Greeks. They facilitate a vast swathe of transactions each year, with over 17.6 billion dollars of art and antiques sold via auction in 2020, not to mention the mammoth volume of auction-based transactions in the general financial system. Total assets under management for the hedge-fund industry eclipses $4.5 trillion (with a ‘t’) dollars and many of these institutions use auctions for the sale of their assets. The sheer volume of transactions by auctions and the power they wield warrants an investigation into optimising such systems.

We aim to investigate various bidding strategies in a second-price auction system. The goal of such a system is for both buyers and sellers to pay/receive a ‘fair’ price for the goods on sale - mitigating against the infamous “winner’s curse”. We introduce two types of bidders: early and so-called ‘sniper’ bidders, which we model using a Python Agent-Based Modelling framework “Mesa”. The characteristic distinction between the two is that whilst early bidders are permitted to bid throughout the auction, with acute scale factors used to update their bids, sniper bidders wait until the end to swoop in and place a large bid in the hope they ‘steal’ the item at the last moment.

## Repository Architecture

> root - Contains run.py and batch-run.py for running the webserver visualisation / generating datasets respectively

> analysis - Data analysis notebooks used in the hypothesis analysis section of the report

> auctions - Agent-based model of second price auctions

> data - All datasets used for data analysis

> images - Images used in the report

## Model Design

1. maxBid drawn from a normal distribution with mean = 1000, standard deviation = (user inputted)
2. valuation drawn from a normal distribution with mean = 500, standard deviation = (user inputted)
3. EarlyBidder bids are updated by a scalar factor drawn from uniform distribution [1.0, 1.2]
     + min(self.valuation * scalar, self.valuation)
4. Naive SniperBidder bids are updated by a scalar factor drawn from uniform distribution [1.0, 2.0]
     + min(self.valuation * scalar, self.maxBid)
5. Intelligent SniperBidder bids are updated by the average bid increase (observed over the whole auciton)
     + min(self.auctioneer.getSecondHighestBid() + self.auctioneer.getBidIncreaseAverage() + 5, self.maxBid)
