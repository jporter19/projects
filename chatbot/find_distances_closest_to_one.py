# ------ Give list of Docs from Chroma DB -----------------------
#docs = closest_index(res["distances"][0],resp_cnt)
# dists = this is a list of distances returned from a query
# resp_cnt = there could be many distances in dist, this function will return the top "resp_cnt" only. 
# example: if there are 20 distances in dists and resp_cnt=3, then return_ids will only include the top 3

def closest_index(dists, val):
    # --------------- the absolute value of subtracting 1 from every number above and below 1, the closest will be the smallest
    difference = [abs(dist-1) for dist in dists]
    # the absolute val list (difference) and the input list (dists) have the same indexes
    # ----------------  sorted_list will be the dists sorted by difference
    sorted_list = sorted(dists, key=lambda x: difference[dists.index(x)])
    # ----------------  sorted_list could be very long, closet 3 takes the 1st 3 in the sorted list
    closest = sorted_list[:val]
    # ---------------- add the index from dists to return_ids when it matches a distance in the closest list
    return_ids = [dists.index(i) for i in closest if i in dists]
    return return_ids


