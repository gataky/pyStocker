data = []

previous = data[0]
peak     = previous
dip      = previous
trending = True

for point in data:

    delta = point - previous

    if delta > 0:
        print "trending up"
        peak = point # new high

        if trending: # moving upward
            print "\talready moving up"
            continue
        else:
            if (peak - dip) >= reversal:
                print "\t\treverse trending up"
                trending = not trending
            else:
                print "\t\tholding trending up"
                continue



    #~ elif delta < 0:
        #~ dip  = point # new low

