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

print("D1")

# progs1_d1 = generate_programs(number_game_1, 1)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d1)
# make_plots(num_accepts, num_probs, "60", 1, 1e-6)
#
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


print("D2")

progs1_d2 = generate_programs(number_game_1, 2)
num_accepts, num_probs = get_accepts_probabilities(progs1_d2)
make_plots(num_accepts, num_probs, "60", 2, 1e-6)
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


print("D3")

# progs1_d3 = generate_programs(number_game_1, 3, 1e-3)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d3)
# make_plots(num_accepts, num_probs, "60", 3, 1e-3)
# #
# progs1_d3 = generate_programs(number_game_1, 3, 1e-4)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d3)
# make_plots(num_accepts, num_probs, "60", 3, 1e-4)


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
#
# print("1e-5")
# progs1_d3 = generate_programs(number_game_1, 3, 1e-5)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d3)
# make_plots(num_accepts, num_probs, "60", 3, 1e-5)  # todo need to run this again
#
# progs1_d4 = generate_programs(number_game_1, 4, 1e-5)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d4)
# make_plots(num_accepts, num_probs, "60", 4, 1e-5)


# print("1e-6")
# progs1_d3 = generate_programs(number_game_1, 3, 1e-6)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d3)
# make_plots(num_accepts, num_probs, "60", 3, 1e-6)
#
# progs1_d4 = generate_programs(number_game_1, 4, 1e-6)
# num_accepts, num_probs = get_accepts_probabilities(progs1_d4)
# make_plots(num_accepts, num_probs, "60", 4, 1e-6)






print("D2")

# progs1_d2 = generate_programs(number_game_1, 2)
# num_accepts, num_probs = get_weighted_accepts_probabilities(progs1_d2)
# make_plots(num_accepts, num_probs, "60", 2, 1e-6)