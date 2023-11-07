import numpy as np
from queue import Queue
import random
import math


class Customer:

    def __init__(self, id, arrival_time, waiting_time, service_time):
        self.arrival_time = arrival_time
        self.waiting_time = waiting_time
        self.service_time = service_time
        self.id = id

    def __str__(self):
        return "id:" + str(self.id) + "\t arrival time:" + str(self.arrival_time) + "\t waiting time:" + str(
            self.waiting_time) + "\t service time:" + str(self.service_time)

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time


class Event:

    def __init__(self, customer_id, type_idx, occ_time):
        self.types = ['arrival', 'deadline', 'done']
        self.type_idx = type_idx
        self.occ_time = occ_time
        self.customer_id = customer_id

    def __str__(self):
        return "customer id:" + str(self.customer_id) + "\t occurence time:" + str(self.occ_time) + "\t type:" + str(
            self.types[self.type_idx])

    def __lt__(self, other):
        return self.occ_time < other.occ_time

    def __le__(self, other):
        return self.occ_time <= other.occ_time

    def __sub__(self, other):
        if isinstance(other, Event):
            return self.occ_time - other.occ_time
        else:
            return self.occ_time - other


def generate_exp_rv(rate):
    return -1.0 * np.log(1.0 - random.random()) / rate


def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0

    while low <= high:
        mid = (high + low) // 2

        # If x is greater, ignore left half
        if arr[mid] < x:
            low = mid + 1

        # If x is smaller, ignore right half
        elif arr[mid] > x:
            high = mid - 1

        # means x is present at mid
        else:
            return mid

    # If we reach here, then the element was not present
    return low


def insert_arr(arr, value):
    # idx = np.argmin(np.abs(value - np.array(arr)))
    idx = binary_search(arr, value)
    if idx >= len(arr):
        idx = len(arr)
        arr.insert(idx, value)
    else:
        if value <= arr[idx]:
            arr.insert(idx, value)
        else:
            while idx <= len(arr) - 1 and value > arr[idx]:
                idx += 1
            arr.insert(idx, value)
    return arr


def make_customer(pre_cus_time, id):
    if const_theta:
        waiting_time = theta
    else:
        waiting_time = generate_exp_rv(1.0 / theta)

    service_time = generate_exp_rv(mu)
    arrival_time = pre_cus_time + generate_exp_rv(lamb)
    customer = Customer(id, arrival_time, waiting_time, service_time)
    return customer


def phi_n(n, is_const_theta, mu, theta):
    if not is_const_theta:
        if n == 0:
            return 0
        else:
            return n / theta
    else:
        if n == 0:
            return 0
        else:
            return mu / (math.exp(mu * theta / n) - 1)


def p_n(n, p0, lamba, is_const_theta, mu, theta):
    if n == 0:
        return p0
    else:
        dom = 1
        for i in range(1, n + 1):
            dom *= (mu + phi_n(i, is_const_theta, mu, theta))
        return p0 * lamba ** n / dom


def caculate_p0(lamba, constant_theta, mu, theta):
    sum = 0
    for i in range(1, 13):
        makhraj = 1
        for j in range(1, i + 1):
            makhraj *= (mu + phi_n(j, constant_theta, mu, theta))
        sum += (lamba ** i / makhraj)
    p0 = 1.0 / (1 + sum)
    return p0


def find_first_job(queue):
    if len(queue) == 0:
        return None
    min = queue[0]
    for p in queue:
        if p.service_time < min.service_time:
            min = p
    return min


if __name__ == "__main__":

    f = open("parameters.conf", "r")
    # theta = float(f.readline())
    # mu = float(f.readline())

    theta = 2.0
    mu = 1.0


    const_theta = False
    num_of_customers = 1_000_000_0

    for lamba in [5.0,10.0,15.0]:
        lamb = lamba
        # ============================= Analytics =============================
        p0 = caculate_p0(lamba, const_theta, mu, theta)
        pb_analytics = p_n(12, p0, lamba, const_theta, mu, theta)
        pd_analytics = 1 - pb_analytics - (mu / lamba) * (1 - p0)

        # ============================= Experiment =============================
        arrival_time = 0
        pre_cus_time = 0
        cus = make_customer(pre_cus_time, id=0)

        queue = []

        num_blocked_users = 0
        num_deadlined_users = 0

        events = []

        time = 0
        cnt = 0

        events.append(Event(cnt, type_idx=0, occ_time=cus.arrival_time))
        pre_cus = cus
        cnt += 1

        nxt_cus = make_customer(cus.arrival_time, 1)
        done = False

        # main loop
        while len(events) > 0 or cnt < num_of_customers or len(queue) > 0:

            pre_task_service = 0
            if len(queue) > 0:
                pre_task_service = (mu / len(queue))
            first_job = find_first_job(queue)

            if first_job and ((
                                      (
                                              first_job.service_time / pre_task_service) + time) < nxt_cus.arrival_time or cnt >= num_of_customers):
                if events[0].occ_time >= ((first_job.service_time / pre_task_service) + time):

                    ############ CALCULATE SERVICE ###########
                    # a job should be execute before next event
                    # remove customer from server
                    queue.remove(first_job)

                    # remove deadline event
                    for event in events:
                        if event.customer_id == first_job.id and event.type_idx == 1:
                            events.remove(event)
                            break

                    # calculate current time
                    time += (first_job.service_time / pre_task_service)

                    # calculate the time should subtract for each customer
                    for customer in queue:
                        customer.service_time -= (first_job.service_time )

                    continue
                    ###########################################

            if nxt_cus:
                ################ ADDING CUSTOMER ################
                if cnt < num_of_customers:
                    if len(events) == 0:
                        if len(queue) != 0:
                            print("buuuuug")
                        events.append(Event(cnt, type_idx=0, occ_time=nxt_cus.arrival_time))
                        cnt += 1
                        pre_cus = nxt_cus
                        nxt_cus = make_customer(pre_cus.arrival_time, cnt)
                    elif nxt_cus.arrival_time < events[0].occ_time:
                        events.insert(0, Event(cnt, type_idx=0, occ_time=nxt_cus.arrival_time))
                        cnt += 1
                        pre_cus = nxt_cus
                        nxt_cus = make_customer(pre_cus.arrival_time, cnt)
                #################################################


            # get first event of list of events (sorted)
            event = events.pop(0)

            # update time
            pre_time = time
            time = event.occ_time

            # calculate service time of each service
            pre_task_service = 0
            if len(queue) > 0:
                pre_task_service = (mu / len(queue))
            for customer in queue:
                customer.service_time -= ((time - pre_time) * pre_task_service)
                if customer.service_time < 0: print("eroooor")

            # arrival customer event
            if event.type_idx == 0:
                if len(queue) >= 12:
                    cnt += 1
                    num_blocked_users += 1
                    pre_cus = nxt_cus
                    nxt_cus = make_customer(pre_cus.arrival_time, cnt)
                    insert_arr(events, Event(pre_cus.id, 0, pre_cus.arrival_time))
                else:
                    customer = pre_cus
                    queue.append(customer)
                    # adding deadline by the way
                    insert_arr(events, Event(customer.id, 1, time + customer.waiting_time))

            # dead line event
            if event.type_idx == 1:
                customer = next((x for x in queue if x.id == event.customer_id), None)

                if customer:
                    queue.remove(customer)

                num_deadlined_users += 1

        pb_experiment = num_blocked_users / num_of_customers
        pd_experiment = num_deadlined_users / num_of_customers

        print("lambda : ", lamba)
        print(pb_experiment, "\t", pb_analytics, "\t\t", pd_experiment, "\t", pd_analytics,"\n")
        with open('exp.txt', 'a') as f:
            f.writelines(str(pb_experiment) + "\t" + str(pb_analytics) + "\t\t" + str(pd_experiment) + "\t" + str(pd_analytics) + "\n")
