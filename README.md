
# ComputerPerformanceEvaluation
Instructed by Prof. Ali Movaghar from the Department of Computer Engineering, Sharif University of Technology.
Course material: 



## M/M/1/K Queue Performance Analysis

[![GitHub release (latest)](https://img.shields.io/github/v/release/ImanRht/MM1K_Queue_Simulation)](https://github.com/ImanRht/MM1K_Queue_Simulation/releases)
![GitHub repo size](https://img.shields.io/github/repo-size/ImanRht/MM1K_Queue_Simulation)
[![GitHub stars](https://img.shields.io/github/stars/ImanRht/MM1K_Queue_Simulation?style=social)](https://github.com/ImanRht/MM1K_Queue_Simulation/stargazers) 
[![GitHub forks](https://img.shields.io/github/forks/ImanRht/MM1K_Queue_Simulation?style=social)](https://github.com/ImanRht/MM1K_Queue_Simulation/network/members) 
[![GitHub issues](https://img.shields.io/github/issues/ImanRht/MM1K_Queue_Simulation?style=social)](https://github.com/ImanRht/MM1K_Queue_Simulation/issues) 
[![GitHub license](https://img.shields.io/github/license/ImanRht/MM1K_Queue_Simulation?style=social)](https://github.com/ImanRht/MM1K_Queue_Simulation/blob/master/LICENSE) 

This repository contains a simulation of the M/M/1/K queue model, a classic queuing theory concept commonly used in the analysis of computer systems and network performance. These simulations are designed to analyze the performance of these queues under different scenarios.



**Parameters:**
- **Service Rate (μ):** The rate at which the service is provided.
- **Arrival Rate (λ):** The rate at which arrivals occur.
- **Queue Capacity (K):** Set to 14.



## FCFS Service Order

**Key Aspects Covered:**
- **Performance Metrics:** Calculation of the probability of having `n` customers in the system (`P_n`), average number of customers in the system (`N_c`), and probabilities of blocking (`P_b`) and dropping (`P_d`).
- **Simulation Results:** Results showing the impact of varying parameters on system performance.
- **Formulas Used:**
  - `P_n(λ, μ)` for the probability of `n` customers.
  - `N_c` for the average number of customers.
  - Calculation of `P_b` and `P_d` using the provided formulas.
- **Analysis:** Discussion on the impact of different parameters on system performance.

## Processor Sharing Service Order (Round Robin Scheduling)

**Key Aspects Covered:**
- **Round Robin Scheduling:** Examination of the algorithm's performance in managing queues.
- **Performance Metrics:** Analysis of average wait time and throughput under different configurations.
- **Theoretical Evaluation:**
  - Calculation of performance metrics with given parameters (μ and θ).
  - Breakdown of theoretical results and their implications.
  - Evaluation of the impact of different time slices and system configurations.
 
## Discriminatory Processor Sharing Service Order 

**Key Aspects Covered:**
- **Priority-Based Service:** Analysis of how tasks or requests are processed based on assigned priority levels, enabling differentiation in service rates.
- **Performance Metrics:** 
  - Calculation of metrics such as weighted average response time, throughput, and utilization for tasks with different priorities.
  - Probability distribution of customers in the system based on priority classes.
- **Theoretical Evaluation:** 
  - Derivation of performance equations for systems with multiple priority levels.
  - Impact of priority differentiation on overall system performance and fairness.



## Contents

- [FCFS_Simulation.py](FCFS_ServiceOrder/FCFS_Simulation.py): FCFS Service Order 


- [PS_Simulation.py](PS_Simulation.py): Processor Sharing Service Order 


- [DPS_Simulation.py](DPS_Simulation.py): Discriminatory Processor Sharing Service Order 

Evaluation Results for M/M/1/12 Queue with Exponential and Fixed Theta under different customer loads are available in the following files:


 - [FCFS_K12_thetaExp_10M](FCFS_ServiceOrder/FCFS_K12_thetaExp_10M.xlsx) , [FCFS_K12_thetaFixed_10M](FCFS_ServiceOrder/FCFS_K12_thetaFixed_10M.xlsx), [FCFS_K12_thetaExp_300M](FCFS_ServiceOrder/FCFS_K12_thetaExp_300M.xlsx) , [FCFS_K12_thetaFixed_300M](FCFS_ServiceOrder/FCFS_K12_thetaFixed_300M.xlsx)
 
  - [PS_K12_thetaExp_10M](PS_K12_thetaExp_10M.xlsx)  , [PS_K12_thetaFixed_10M](PS_K12_thetaFixed_10M.xlsx),  [PS_K12_thetaExp_100M](PS_K12_thetaExp_100M.xlsx)  , [PS_K12_thetaFixedFixed_100M](PS_K12_thetaFixedFixed_100M.xlsx)
  
   - [DPS_K12_thetaExp_1M](DPS_K12_thetaExp_1M.xlsx) , [DPS_K12_thetaFixed_1M](DPS_K12_thetaFixed_1M.xlsx),  [DPS_K12_thetaExp_10M](DPS_K12_thetaExp_10M.xlsx)
  

## References

- Mor. Harchol-Balter, “[Performance modeling and design of computer systems: queueing theory in action](https://books.google.de/books?hl=en&lr=&id=y1cgAwAAQBAJ&oi=fnd&pg=PR17&dq=M.+Harchol-Balter,+Performance+Modeling+and+Design+of+Computer+Systems,+Cambridge+University+Presss&ots=fyMxIXzywD&sig=r1Ez9ftmSQJsiU9qGxHaQ_K1ZI8&redir_esc=y#v=onepage&q=M.%20Harchol-Balter%2C%20Performance%20Modeling%20and%20Design%20of%20Computer%20Systems%2C%20Cambridge%20University%20Presss&f=false)", Cambridge University Press, 2013.
- Krishna. Kant, "[Introduction to computer system performance evaluation](http://repository.bitscollege.edu.et:8080/handle/123456789/311)" International Edition, 1992.


## Contribute
If you have an issue or found a bug, please raise a GitHub issue [here](https://github.com/ImanRht/MM1K_Queue_Simulation/issues). Pull requests are also welcome.


