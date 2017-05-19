

def trickle_validate(data, min_vals, max_vals):
    fail_count = 0
    for i in range(len(data)):
        if min_vals[i] <= data[i] < max_vals[i]:
            pass
        else:
            print(i, "test fail on", data[i], "not in range [", min_vals[i], ",", max_vals[i], "]")
            fail_count += 1
    print("fail count: ", fail_count)


def validate_intervals(data, imin, imax):
    interval = imin
    fail_count = 0
    for time in data:
        if interval/2 <= time < interval:
            pass
        elif imin/2 <= time < imin:
            interval = imin
        else:
            print("     test fail on", time, "for interval", interval)
            fail_count += 1
        if interval*2 < imax:
            interval *= 2
        else:
            interval = imax

# tests t with respect to actual i
def test_t_and_i(i_toggles, t_toggles):
    for i in range(len(i_toggles)-1):
        if i_toggles[i] <= t_toggles[i] < i_toggles[i+1]:
            pass
        else:
            print(i, "fail.", t_toggles[i], "not in range", i_toggles[i], ",", i_toggles[i+1])


def determine_min_max(imin, imax, transmit_delta_times):
    trickle_out_data = [[i] for i in transmit_delta_times]
    trickle_min_vals = [imin/2]
    trickle_max_vals = [imin-1]
    next_min = imin/2
    next_max = imin-1
    last_i = 0

    for i in range(len(trickle_out_data)):
        if next_max*2 < imax:
            next_max *= 2
            trickle_max_vals.append(next_max + last_i/2)# last_i/2)
        else:
            next_max = imax
            trickle_max_vals.append(imax-1 + last_i/2)# last_i/2)

        last_i = next_max

        if next_min*2 < imax/2:
            next_min *= 2
            trickle_min_vals.append(next_min)
        else:
            trickle_min_vals.append(imax/2)

    for i in range(len(trickle_out_data)):
        trickle_out_data[i] = trickle_out_data[i] + [trickle_min_vals[i]] + [trickle_max_vals[i]]

    print("--------- test t with expected i values ---------")
    trickle_validate(transmit_delta_times, trickle_min_vals, trickle_max_vals)

    return trickle_out_data