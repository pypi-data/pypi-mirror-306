# bidding_library/bidding_logic/bidding.py

from django.contrib import messages

def make_bid_logic(request, auction, bid_amount):
    """
    Logic to place a bid on an auction. Assumes request is from an authenticated user.
    """
    if auction.highest_bid == 0:  # No bids placed yet
        if bid_amount > auction.starting_price:
            # Create the first bid
            auction.highest_bid = bid_amount
            auction.highest_bidder = request.user
            auction.save()
            messages.success(request, f'Your bid of ${bid_amount} was successful! You are the highest bidder.')
            return True
        else:
            messages.error(request, f'Your bid must be higher than the starting price of ${auction.starting_price}.')
            return False
    else:
        if bid_amount > auction.highest_bid:
            # Create a new bid
            auction.highest_bid = bid_amount
            auction.highest_bidder = request.user
            auction.save()
            messages.success(request, f'Your bid of ${bid_amount} was successful! You are the highest bidder.')
            return True
        else:
            messages.error(request, f'Your bid must be higher than the current highest bid of ${auction.highest_bid}.')
            return False
