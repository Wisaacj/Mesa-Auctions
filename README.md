# Second price online auction

## Design

1. maxBid drawn from a normal distribution with mean = 1000, standard deviation = (user inputted)
2. valuation drawn from a normal distribution with mean = 500, standard deviation = (user inputted)
3. EarlyBidder bids are updated by a scalar factor drawn from uniform distribution [1.0, 1.2] --- min(self.valuation * scalar, self.valuation)
4. SniperBidder bids are updated by a scalar factor drawn from uniform distribution [1.0, 2.0] --- min(self.valuation * scalar, self.maxBid)

## IDEAS

1. Have different bid and watch probabilties for the different types of agents
     - Maybe generate their bid/watch probabilities from a normal distribution??
