import logicData
import sys
import matplotlib.pyplot as plt

inFile = sys.argv[1]
imin = int(sys.argv[2])
imax = int(sys.argv[3])
outFile = "output/trickle_test_output/"

data = logicData.LogicData(inFile, "ms", 8)
data.set_decimal_points(2)
capture_data = data.get_raw_data()


def trickle_validate(data, min_vals, max_vals):
    fail_count = 0
    for i in range(len(data)):
        if min_vals[i] <= data[i][0] < max_vals[i]:
            pass
        else:
            print(i, "test fail on", data[i][0], "not in range [", min_vals[i], ",", max_vals[i], "]")
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


# tests t with respect to actual generated intervals
def test_t_and_i(i_toggles, t_toggles):
    for i in range(len(i_toggles)-1):
        if i_toggles[i] <= t_toggles[i] < i_toggles[i+1]:
            pass
        else:
            print(i, "fail.", t_toggles[i], "not in range", i_toggles[i], ",", i_toggles[i+1])

# test
def determine_min_max(imin, imax, transmit_delta_times):
    limit = 0.002 * data.time_multiplier
    trickle_out_data_without_tiny_toggles = [] # logicData.calculate_tx_intervals(transmit_delta_times, [0, limit])
    for i in range(len(transmit_delta_times)):
        if transmit_delta_times[i] < limit:
            trickle_out_data_without_tiny_toggles[-1] += transmit_delta_times[i]
        else:
            trickle_out_data_without_tiny_toggles.append(transmit_delta_times[i])

    trickle_min_vals = [imin/2]
    trickle_max_vals = [imin-1]
    next_min = imin/2
    next_max = imin-1
    last_i = 0

    for i in range(len(trickle_out_data_without_tiny_toggles)):
        if next_max*2 < imax:
            next_max *= 2
            trickle_max_vals.append(next_max + last_i/2)
        else:
            next_max = imax
            trickle_max_vals.append(imax-1 + last_i/2)

        last_i = next_max

        if next_min*2 < imax/2:
            next_min *= 2
            trickle_min_vals.append(next_min)
        else:
            trickle_min_vals.append(imax/2)

    for i in range(len(trickle_out_data_without_tiny_toggles)):
        trickle_out_data_without_tiny_toggles[i] = \
            [trickle_out_data_without_tiny_toggles[i]] + [trickle_min_vals[i]] + [trickle_max_vals[i]]

    print("--------- test t with expected i values ---------")
    trickle_validate(trickle_out_data_without_tiny_toggles, trickle_min_vals, trickle_max_vals)

    return trickle_out_data_without_tiny_toggles

transmit_times = []
i_toggles = []
last_sample = 0
for i in capture_data:
    current_transmit_timeout = (i[1] >> 8) ^ (last_sample >> 8)
    current_interval = ((i[1] >> 7) & 1) ^ ((last_sample >> 7) & 1)
    if current_transmit_timeout:
        transmit_times.append(i[0])
    if current_interval:
        i_toggles.append(i[0])
    last_sample = i[1]


#test_t_and_i(i_toggles, transmit_times)

trickle_out_data = \
    determine_min_max(imin, imax, logicData.get_delta_times(transmit_times))

logicData.save(trickle_out_data, outFile + 'trickle.csv')

plt.xlabel("transmit")
plt.ylabel("time (ms) since last transmit")
plt.suptitle("Durations between each transmit and restrictions from the trickle algorithm")
plt.plot(trickle_out_data)
plt.grid(True)
plt.show()