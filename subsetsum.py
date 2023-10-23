RED = '\033[91m'
RESET = '\033[0m'
GREEN = "\033[92m"

def generate_instances(num_instances, tam_max, range_max):
    Sets = []
    for _ in range(num_instances):
        nums = random.sample(range(range_max[0], range_max[1]), random.randint(10, tam_max))
        target_sum = random.randint(range_max[0], range_max[1])
        Sets.append({'nums': nums, 'target_sum' : target_sum})
    return Sets

def validate_input(input_tupla):
    if not isinstance(input_tupla, tuple) or len(input_tupla) != 2:
        print("Input não é uma tupla com 2 elementos.")
        return False

    if not all(isinstance(element, int) and element > 0 for element in input_tupla):
        print("Ambos os elementos precisam ser inteiros positivos.")
        return False

    if input_tupla[0] >= input_tupla[1]:
        print("O primeiro elemento precisa ser menor que o segundo.")
        return False

    return True

def delta(x, a, B):
    return B - sum(x[i] * a[i] for i in range(len(x)))

def adapted_algorithm(a, B, num_trials):
    n = len(a)
    x_best = [0] * n

    for trial in range(1, num_trials + 1):
        x = [0] * n

        # Seleção randômica
        for i in random.sample(range(n), n):
            if a[i] <= delta(x, a, B):
                x[i] = 1

        L = [i for i, val in enumerate(x) if val == 1]
        for i in random.sample(L, len(L)):
            if delta(x, a, B) == 0:
                break

            T_idx = [j for j in range(n) if x[j] == 0 and 0 < (a[i] - a[j]) <= delta(x, a, B)]

            if len(T_idx) > 0:
                k = max(T_idx, key=lambda j: a[j])
                x[k] = 1
                x[i] = 0

        # Pelo que entendi, aqui o xBest é atualizado
        if delta(x, a, B) < delta(x_best, a, B):
            x_best = x.copy()

        if delta(x_best, a, B) == 0:
            break

    return x_best


def extract_elements(a, solution):
    selected_elements = [a[i] for i in range(len(solution)) if solution[i] == 1]
    return selected_elements

print("This is the interface to setup the configurations of the instances of subset sum problem.")

# Quantidade de instâncias
num_instances = None
while True:
    num_instances = eval(input("How many instances you want?"))
    if isinstance(num_instances,int) and num_instances > 0:
        break;
    else:
        print("You must insert an integer value")

# Tamanho máximo de instância
tam_max = None
while True:
    tam_max = int(input("What will be the maximum length of any instance? It needs to be greater than 10."))
    if isinstance(tam_max,int) and tam_max > 10:
        break
    else:
        print("You must insert an integer value.")

range_max = None
while True:
    range_max = eval(input("Which should be the range? Enter a tuple. \n Ex: (1,1000)"))
    if validate_input(range_max):
        break
    else:
        print("Enter a tuple. Ex: (1, 1000)")

save = None
while True:
    save = input("Do you want to save the file? Y/N")
    if save.lower() == 'y' or save.lower() == 'n':
        save = True if 'y' == save.lower() else False
        break;
    else:
        print("Insert Y for saving and N for not saving.")


Sets = generate_instances(num_instances, tam_max, range_max)


f = None
if save:
    f = open("table" , "a")

num_trials_range = [1, 5, 10, 15, 20, 25, 50, 75, 100]

results_num_fails = []
results_full_time = []

for num_trials in num_trials_range:
    num_fails = 0
    num_succ = 0
    num_sets = len(Sets)
    full_time = 0
    start_algorithm = time.time()

    for subset in Sets:
        new_set = subset['nums']
        target = subset['target_sum']
        start_time = time.time()
        resulted_match = adapted_algorithm(new_set, target, num_trials)
        result = extract_elements(new_set, resulted_match)
        end_time = time.time()
        total_time = end_time - start_time
        print("Set selected:", new_set)
        print("Target:", target)
        print(f"Time of execution: {total_time:.4f}")
        if result:
            sum_result = sum(result)
            print("Subset with the target sum:", result)
            if sum_result != target:
                num_fails += 1
                print(f"{RED} O resultado foi diferente do esperado! {RESET}")
            else:
                num_succ += 1
        else:
            print("No such subset exists.")
        print("==============================================================")
        if f != None:
            f.write(str(new_set) + ',' + str(target) + ',' + str(result) + ',' + str(total_time) + 's,' + str(num_trials) + (",SUCCESS\n" if sum(result) == target else ",FAIL\n"))

    end_algorithm = time.time()
    full_time = end_algorithm - start_algorithm
    results_num_fails.append((num_trials, num_fails))
    results_full_time.append((num_trials, full_time))
    print(f"{GREEN} O algoritmo terminou sua execução! {RESET}")
    print("Número de conjuntos: ", num_sets)
    print("Número de sucessos: ", num_succ)
    print("Número de falhas: ", num_fails)
    print("Número de Trials: ", num_trials)

num_trials_values, num_fails_values = zip(*results_num_fails)
num_trials_values_time, full_time_values = zip(*results_full_time)


plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(num_trials_values, num_fails_values, marker='o', linestyle='-')
plt.title('Comparação entre número de "Trials" e número de falhas')
plt.xlabel('num_trials')
plt.ylabel('num_fails')
plt.grid(True)

plt.xticks(num_trials_values)
plt.yticks(num_fails_values)

plt.subplot(1, 2, 2)
plt.plot(num_trials_values_time, full_time_values, marker='o', linestyle='-')
plt.title('Comparação entre "Trials" e Tempo de execução')
plt.xlabel('num_trials')
plt.ylabel('full_time (s)')
plt.grid(True)

plt.xticks(num_trials_values_time)
plt.yticks(full_time_values)

plt.tight_layout()
plt.show()