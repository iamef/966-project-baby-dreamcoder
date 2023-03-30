from program_generator import *
import numpy as np
import matplotlib.pyplot as plt

# use
# import primitives_number_game as prim
# or
# import primitives_ng_more_ints as prim
# in program_generator
# to see the difference between having the 2 different primitive systems



def get_normalized(progs):
    norm_constant = sum([w for f, w in progs])
    progs_normalized = list(map(lambda x: (x[0], x[1] / norm_constant), progs))

    return progs_normalized

def get_accepts_probabilities(progs):
    num_accepts = np.zeros(100)
    num_probs = np.zeros(100)

    progs_normalized = get_normalized(progs)

    for i in range(0, 100):
        prob_normed: float
        for prog, prob_normed in progs_normalized:
            try:
                if interpret(prog, (i,)):
                    num_accepts[i] += 1
                    num_probs[i] += prob_normed
                else:
                    pass  # print("wow")
            except:
                pass

    return num_accepts, num_probs

def num_passes(program):
    try:
        interpret(program, ("anuthing",))
        return 100
    except:
       count = 0
       for i in range(0, 100):
           try:
               if interpret(program, (i,)):
                   count += 1
               else:
                   pass  # print("wow")
           except:
               pass

    return count


def get_size_weighted_normalized(progs, power=1):
    progs_size_weighted = list(map(lambda x: (x[0], x[1] / num_passes(x[0]) ** power), progs))
    norm_constant = sum([w for f, w in progs_size_weighted])
    progs_size_weighted = list(map(lambda x: (x[0], x[1] / norm_constant), progs_size_weighted))

    progs_size_weighted.sort(key=lambda f_and_prob: (-f_and_prob[1], str(f_and_prob[0])))
    return progs_size_weighted


def get_weighted_accepts_probabilities(progs, power=1):
    num_accepts = np.zeros(100)
    num_weighted_probs = np.zeros(100)

    progs_size_weighted = get_size_weighted_normalized(progs, power)

    for i in range(0, 100):
        prob_normed: float
        for prog, prob_normed in progs_size_weighted:
            try:
                if interpret(prog, (i,)):
                    num_accepts[i] += 1
                    num_weighted_probs[i] += prob_normed
                else:
                    pass  # print("wow")
            except:
                pass

    return num_accepts, num_weighted_probs


def make_plots(num_accepts, num_probs, ng_nums: str, depth: int, pr: float):
    # plt.figure(figsize=(16, 4))
    # plt.title("Number Game 60: Depth 2")

    # plt.subplot(2, 4, 1)
    plt.plot(num_accepts, "go", num_accepts, "k", ms=3.0)
    plt.axis([0, 100, 0, max(num_accepts)])
    plt.title(f"Number Game {ng_nums}: Depth {depth}, Prob {pr} Program Acceptance Counts")
    plt.xlabel("Number")
    plt.ylabel("Number of Acceptance")
    plt.savefig(f"ngmipi{ng_nums}_d{depth}_p{pr}_AccCounts.png")
    plt.show()

    # plt.subplot(1, 2, 2)
    plt.plot(num_probs, "ro", num_probs, "k", ms=3.0)
    plt.axis([0, 100, 0, 1])
    plt.title(f"Number Game {ng_nums}: Depth {depth}, Prob {pr} Program Probability Sums")
    plt.xlabel("Number")
    plt.ylabel("Probability Sums")
    plt.savefig(f"ngmipi{ng_nums}_d{depth}_p{pr}_ProbSums.png")
    plt.show()


number_game_1 = Problem(
    input_type=(int,),
    output_type=bool,
    input_ouput_pairs=[
        ((60,), True)
    ]
)









################################################################
# GRAPHS FOR NUMBER GAME WITH JUST NUMBER 60
################################################################

# Depth 1 program generation and graphs
# print("D1")

# progs1_d1 = generate_programs(number_game_1, 1, 1e-6)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d1)
# make_plots(num_accepts, num_probs, "60", 1, 1e-6)

# progs1_d1 = generate_programs(number_game_1, 1, 1e-5)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d1)
# make_plots(num_accepts, num_probs, "60", 1, 1e-5)
#
# progs1_d1 = generate_programs(number_game_1, 1, 1e-4)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d1)
# make_plots(num_accepts, num_probs, "60", 1, 1e-4)
#
# progs1_d1 = generate_programs(number_game_1, 1, 1e-3)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d1)
# make_plots(num_accepts, num_probs, "60", 1, 1e-3)


# Depth 2 program generation and graphs
# print("D2")
#
# progs1_d2 = generate_programs(number_game_1, 2, 1e-6)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d2)
# make_plots(num_accepts, num_probs, "60", 2, 1e-6)
#
# progs1_d2 = generate_programs(number_game_1, 2, 1e-5)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d2)
# make_plots(num_accepts, num_probs, "60", 2, 1e-5)
#
# progs1_d2 = generate_programs(number_game_1, 2, 1e-4)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d2)
# make_plots(num_accepts, num_probs, "60", 2, 1e-4)
#
# progs1_d2 = generate_programs(number_game_1, 2, 1e-3)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d2)
# make_plots(num_accepts, num_probs, "60", 2, 1e-3)


# Depth 3 program generation and graphs
# print("D3")
#
# progs1_d3 = generate_programs(number_game_1, 3, 1e-3)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d3)
# make_plots(num_accepts, num_probs, "60", 3, 1e-3)
# #
# progs1_d3 = generate_programs(number_game_1, 3, 1e-4)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d3)
# make_plots(num_accepts, num_probs, "60", 3, 1e-4)
#
# print("1e-5")
# progs1_d3 = generate_programs(number_game_1, 3, 1e-5)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d3)
# make_plots(num_accepts, num_probs, "60", 3, 1e-5)
#
# print("1e-6")
# progs1_d3 = generate_programs(number_game_1, 3, 1e-6)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d3)
# make_plots(num_accepts, num_probs, "60", 3, 1e-6)
#
# note that for depth 3, generate_program smaller than a 1e-4 threshold takes a significant amount of time.


# Depth 4 program generation and graphs
# print("D4")
#
# progs1_d4 = generate_programs(number_game_1, 4, 1e-3)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d4)
# make_plots(num_accepts, num_probs, "60", 4, 1e-3)
#
# progs1_d4 = generate_programs(number_game_1, 4, 1e-4)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d4)
# make_plots(num_accepts, num_probs, "60", 4, 1e-4)
#
# progs1_d4 = generate_programs(number_game_1, 4, 1e-5)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d4)
# make_plots(num_accepts, num_probs, "60", 4, 1e-5)
#
# progs1_d4 = generate_programs(number_game_1, 4, 1e-6)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d4)
# make_plots(num_accepts, num_probs, "60", 4, 1e-6)
#
# note that for depth 4, generate_program smaller than a 1e-4 threshold takes a significant amount of time.




# Use the size principle to get full Bayesian posterior
# print("D2")
# progs1_d2 = generate_programs(number_game_1, 2)
# print(1, get_size_weighted_normalized(progs1_d2, 1)[:5])
# num_accepts, num_probs = get_weighted_accepts_probabilities(progs1_d2, 1)
# num_accepts, num_probs = get_weighted_accepts_probabilities(progs1_d2, 2)  # modified size principle
# make_plots(num_accepts, num_probs, "60", 2, 1e-6)





################################################################
# TOP PROGRAMS FOR ADDING MORE NUMBERS TO NUMBER GAME
################################################################

# Using depth 2, 1e-6 settings.

# 60, 65
number_game_2 = Problem(
    input_type=(int,),
    output_type=bool,
    input_ouput_pairs=[
        ((60,), True),
        ((65,), True)
    ]
)
progs2_d2 = generate_programs(number_game_2, 2, 1e-6)

# print top 5; technically prints Program object address
# I used debugger to get the actual programs TODO can make it better later
print(2, get_size_weighted_normalized(progs2_d2, 2)[:5])


# 60, 65, 69
number_game_3 = Problem(
    input_type=(int,),
    output_type=bool,
    input_ouput_pairs=[
        ((60,), True),
        ((65,), True),
        ((69,), True)
    ]
)

progs3_d2 = generate_programs(number_game_3, 2, 1e-6)
print(3, get_size_weighted_normalized(progs3_d2, 3)[:5])  # print top 5


# 60-69
number_game_60_69 = Problem(
    input_type=(int,),
    output_type=bool,
    input_ouput_pairs=[
        ((60,), True),
        ((61,), True),
        ((62,), True),
        ((63,), True),
        ((64,), True),
        ((65,), True),
        ((66,), True),
        ((67,), True),
        ((68,), True),
        ((69,), True)
    ]
)

progsf_d2 = generate_programs(number_game_60_69, 2, 1e-6)
print("full", get_size_weighted_normalized(progsf_d2, 3)[:5])


# try to get interesting conjunctions with depth 3

# this took forever to run; I had it in the background probably for several hours and forgot about it
# progsf_d3_10 = generate_programs(number_game_60_69, 3, 10e-10)
# # random comment: technically count can get us the maximum a priori; using only size prinicple
# progsf_d3_10_count = list(map(lambda x: (x[0], x[1], num_passes(x[0])), progsf_d3_10))
# progsf_d3_10_count.sort(key=lambda x: x[2])  # sort by count, to investigate in debugger
# print("full", get_size_weighted_normalized(progsf_d3_10, 10)[:5])

#
# print("phew... that was a lot")
