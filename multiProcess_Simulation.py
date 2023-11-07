import multiprocessing
import os

import numpy as np
from queue import Queue
import random
import math


class Customer:

    def __init__(self, id, arrival_time, waiting_time, service_time, cl):
        self.arrival_time = arrival_time
        self.waiting_time = waiting_time
        self.service_time = service_time
        self.id = id
        self.cl = cl

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


def make_customer(pre_cus_time, id, cl,lamb,const_theta=False,theta=2.0,mu=1.0):
    if const_theta:
        waiting_time = theta
    else:
        waiting_time = generate_exp_rv(1.0 / theta)

    service_time = generate_exp_rv(mu)
    arrival_time = pre_cus_time + generate_exp_rv(lamb)
    customer = Customer(id, arrival_time, waiting_time, service_time, cl)
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
        if (p.service_time / p.cl) < (min.service_time / min.cl):
            min = p
    return min


def square(lamba):
    lamb = lamba
    theta = 2.0
    mu = 1.0
    const_theta = False
    num_of_customers = 1_000_000_0

    arrival_time = 0
    pre_cus_time = 0
    len_c1, len_c2 = 0, 0

    cl = 1 if random.random() < 0.5 else 2
    cus = make_customer(pre_cus_time, id=0, cl=cl,lamb=lamb)

    queue = []

    num_blocked_users = 0
    num_deadlined_users = 0

    num_deadlined_users1 = 0
    num_deadlined_users2 = 0

    events = []

    time = 0
    cnt = 0
    cnt1 = 0
    cnt2 = 0

    cnt1 = cnt1 + 1 if cl == 1 else cnt1
    cnt2 = cnt2 + 1 if cl == 2 else cnt2

    events.append(Event(cnt, type_idx=0, occ_time=cus.arrival_time))
    pre_cus = cus
    cnt += 1

    cl = 1 if random.random() < 0.5 else 2
    nxt_cus = make_customer(cus.arrival_time, 1, cl=cl,lamb=lamb)
    done = False

    # main loop
    while len(events) > 0 or cnt < num_of_customers or len(queue) > 0:

        pre_task_service1 = 0
        pre_task_service2 = 0

        if len(queue) > 0:
            pre_task_service1 = (mu * 1 / (1 * len_c1 + 2 * len_c2))
            pre_task_service2 = (mu * 2 / (1 * len_c1 + 2 * len_c2))

        first_job = find_first_job(queue)

        tmp_per_task_service = 0
        if first_job:
            tmp_per_task_service = pre_task_service1 if first_job.cl == 1 else pre_task_service2

        if first_job and (
                ((first_job.service_time / tmp_per_task_service) + time) < nxt_cus.arrival_time or
                cnt >= num_of_customers):
            if events[0].occ_time >= ((first_job.service_time / tmp_per_task_service) + time):

                ############ CALCULATE SERVICE ###########
                # a job should be execute before next event
                # remove customer from server
                queue.remove(first_job)
                if first_job.cl == 1:
                    len_c1 -= 1
                else:
                    len_c2 -= 1

                # remove deadline event
                for event in events:
                    if event.customer_id == first_job.id and event.type_idx == 1:
                        events.remove(event)
                        break

                # calculate current time
                time += (first_job.service_time / tmp_per_task_service)

                # calculate the time should subtract for each customer
                for customer in queue:
                    customer.service_time -= (customer.cl * first_job.service_time / first_job.cl)

                continue
                ###########################################

        if nxt_cus:
            ################ ADDING CUSTOMER ################
            if cnt < num_of_customers:
                if len(events) == 0:
                    events.append(Event(cnt, type_idx=0, occ_time=nxt_cus.arrival_time))
                    cnt += 1
                    pre_cus = nxt_cus
                    cl = 1 if random.random() < 0.5 else 2
                    cnt1 = cnt1 + 1 if cl == 1 else cnt1
                    cnt2 = cnt2 + 1 if cl == 2 else cnt2
                    nxt_cus = make_customer(pre_cus.arrival_time, cnt, cl=cl,lamb=lamb)
                elif nxt_cus.arrival_time < events[0].occ_time:
                    events.insert(0, Event(cnt, type_idx=0, occ_time=nxt_cus.arrival_time))
                    cnt += 1
                    pre_cus = nxt_cus
                    cl = 1 if random.random() < 0.5 else 2
                    cnt1 = cnt1 + 1 if cl == 1 else cnt1
                    cnt2 = cnt2 + 1 if cl == 2 else cnt2
                    nxt_cus = make_customer(pre_cus.arrival_time, cnt, cl=cl,lamb=lamb)
            #################################################

        # get first event of list of events (sorted)
        event = events.pop(0)

        # update time
        pre_time = time
        time = event.occ_time

        # calculate each per_task_services
        pre_task_service1 = 0
        pre_task_service2 = 0

        if len(queue) > 0:
            pre_task_service1 = (mu * 1 / (1 * len_c1 + 2 * len_c2))
            pre_task_service2 = (mu * 2 / (1 * len_c1 + 2 * len_c2))

        # calculate service time of each service
        for customer in queue:
            customer.service_time -= ((time - pre_time) * pre_task_service1 * customer.cl)

        # arrival customer event
        if event.type_idx == 0:
            if len(queue) >= 12:
                cnt += 1
                num_blocked_users += 1
                pre_cus = nxt_cus
                cl = 1 if random.random() < 0.5 else 2
                cnt1 = cnt1 + 1 if cl == 1 else cnt1
                cnt2 = cnt2 + 1 if cl == 2 else cnt2
                nxt_cus = make_customer(pre_cus.arrival_time, cnt, cl=cl,lamb=lamb)
                insert_arr(events, Event(pre_cus.id, 0, pre_cus.arrival_time))
            else:
                customer = pre_cus
                queue.append(customer)

                if customer.cl == 1:
                    len_c1 += 1
                else:
                    len_c2 += 1

                # adding deadline by the way
                insert_arr(events, Event(customer.id, 1, time + customer.waiting_time))

        # dead line event
        if event.type_idx == 1:
            customer = next((x for x in queue if x.id == event.customer_id), None)
            queue.remove(customer)

            if customer.cl == 1:
                len_c1 -= 1
            else:
                len_c2 -= 1

            num_deadlined_users += 1
            if customer.cl == 1:
                num_deadlined_users1 += 1
            elif customer.cl == 2:
                num_deadlined_users2 += 1

    pb_experiment = num_blocked_users / num_of_customers
    pd_experiment = num_deadlined_users / num_of_customers
    pd1_experiment = num_deadlined_users1 / num_of_customers
    pd2_experiment = num_deadlined_users2 / num_of_customers

    print("lambda : ", lamba, '\t\t :', pb_experiment, "\t", pd_experiment, "\t", pd1_experiment, "\t", pd2_experiment)

    return [str(pb_experiment), str(pd_experiment), str(pd1_experiment), str(pd2_experiment)]


if __name__ == "__main__":
    # input list
    const_theta = False
    theta = 2.0
    mu = 1.0

    mylist = np.arange(0.1, 20.1, 0.1)

    # creating a pool object
    p = multiprocessing.Pool(processes=5)

    # map list to target function
    result = p.map(square, mylist)

    print(result)
    print("=======================")
    for item in result:
        print('\t'.join(item))

    result = np.array(result)
    with open('15_20.npy', 'wb') as f:
        np.save(f, result)
