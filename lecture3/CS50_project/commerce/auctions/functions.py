def set_winner(listing):
  if listing.last_bid_id:
    return listing.last_bid_id.user_id
  return None
