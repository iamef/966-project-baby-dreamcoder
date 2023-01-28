
# note if we calculate wake solely based on bayesian weights
# then I'll have to modify my wake algorithm
# it would then need to be some sort of a priority queue

# order 0

# format
# dict[func_output][[
number_game_primitive_weights = {
    int: {  # output is int
        tuple(): 1,
        (int,): 1,
        (int, int): 1,
        (bool, int, int): 1/3,
        (int, int, callable): 1/5  # doesn't exist in primitives number game
    },
    bool: {
        (int, int): 1,
        (bool, bool): 0.5
    },
    callable: {
        (bool, callable, callable): 1
    }
}


# p(function | next problem) = p(function | previous problems)
# generate input output pairs based on that



# you can generate all the possible programs

# at the end of the day you can order from most probable to least probable
# replace max depth with how probable a program, but has guarantee that
# all programs above probability

# we don't need to actually sort the list
# iteratively


# start with simple prior
# to see what programs actually be useful
# that will help fit better parameters for the prior



# prob(next func | pred)
# seems like it's too complicated
# for the context of the project

# p(program | input, training output) => posterior
# p(training output | program, input) => ... likelihood

# p(program)


# P(data / hypothesis) = 0 or 1


# formula to calculate weight based on program size
# weight_based_on_program_size = initial_weight / (depth * num_arguments)
# ^ I feel like penalizes cond and ind even more than it needs to...


