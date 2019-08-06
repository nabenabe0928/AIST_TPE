from argparse import ArgumentParser as ArgPar
from main import start_opt
from optimize import sample_target, create_hyperparameter, save_evaluation, print_iterations
from objective_functions.train import func
from objective_functions.benchmark import *
import numpy as np

def objective_func(model, num, n_cuda, n_jobs, lock):
    hp_dict = {}
    sample = sample_target(model, num, n_jobs, lock)

    """
    var_name = "batch_size"
    hp_dict[var_name] = sample(create_hyperparameter("int", name = var_name, lower = 32, upper = 256, default_value = 128))
    var_name = "lr"
    hp_dict[var_name] = sample(create_hyperparameter("float", name = var_name, lower = 5.0e-3, upper = 5.0e-1, default_value = 5.0e-2))
    var_name = "momentum"
    hp_dict[var_name] = sample(create_hyperparameter("float", name = var_name, lower = 0.9, upper = 1.0, default_value = 0.9))
    var_name = "weight_decay"
    hp_dict[var_name] = sample(create_hyperparameter("float", name = var_name, lower = 5.0e-6, upper = 5.0e-2, default_value = 5.0e-4))
    var_name = "ch1"
    hp_dict[var_name] = sample(create_hyperparameter("int", name = var_name, lower = 16, upper = 128, default_value = 32))
    var_name = "ch2"
    hp_dict[var_name] = sample(create_hyperparameter("int", name = var_name, lower = 16, upper = 128, default_value = 32))
    var_name = "ch3"
    hp_dict[var_name] = sample(create_hyperparameter("int", name = var_name, lower = 16, upper = 128, default_value = 64))
    var_name = "ch4"
    hp_dict[var_name] = sample(create_hyperparameter("int", name = var_name, lower = 16, upper = 128, default_value = 64))
    var_name = "drop_rate"
    hp_dict[var_name] = sample(create_hyperparameter("float", name = var_name, lower = 0., upper = 1., default_value = 0.5))
    """

    hp_dict["loss"] = 0
    xs = []
    for n in range(2):
        var_name = "x{}".format(n)
        hp_dict[var_name] = sample(create_hyperparameter("float", name = var_name, lower = -32., upper = 32., default_value = 0.5))
        xs.append(hp_dict[var_name])
        #hp_dict["loss"] += hp_dict[var_name] ** 2

    xs = np.array(xs)
    t1 = 20
    t2 = - 20 * np.exp(- 0.2 * np.sqrt(1.0 / len(xs) * np.sum(xs ** 2)))
    t3 = np.e
    t4 = - np.exp(1.0 / len(xs) * np.sum(np.cos(2 * np.pi * xs)))
    loss = t1 + t2 + t3 + t4
    hp_dict["loss"] = loss
    #loss, acc = func(hp_dict, model, num, n_cuda, n_jobs)
    #print_iterations(n_jobs, loss, acc)
    print_iterations(n_jobs, hp_dict["loss"])

    #hp_dict["loss"] = hp_dict["x"] ** 2
    #hp_dict["acc"] = acc

    save_evaluation(hp_dict, model, num, n_jobs, lock)


if __name__ == "__main__":
    argp = ArgPar()
    argp.add_argument("-model", default = "CNN")
    argp.add_argument("-num", type = int, default = None)
    argp.add_argument("-parallel", type = int, default = None)
    argp.add_argument("-jobs", type = int, default = None)
    argp.add_argument("-re", type = int, default = None, choices = [0, 1])
    args = argp.parse_args()

    num = args.num
    n_parallels = args.parallel
    n_jobs = args.jobs
    rerun = bool(args.re)
    model = args.model

    start_opt(obj = objective_func, model = model, num = num, n_parallels = n_parallels, n_jobs = n_jobs, rerun = rerun)
