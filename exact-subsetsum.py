import random
Sets = []

for size in range(51):
    nums = random.sample(range(1, 1000), size)
    target_sum = random.randint(1, 5000)
    Sets.append({'nums': nums, 'target_sum': target_sum})

for _ in range(1000):
    nums = random.sample(range(1, 1000), random.randint(1, 50))
    target_sum = random.randint(5000, 10000)
    Sets.append({'nums': nums, 'target_sum': target_sum})

for set_data in Sets[:10]:
    print(set_data)

print("READY")

def find_subset_with_sum(nums, target_sum):
    n = len(nums)
    # Tabela (Programação dinâmica, array de duas dimensões para guardar valores intermediários)
    dynamic_table = [[False] * (target_sum + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dynamic_table[i][0] = True

    for i in range(1, n + 1):
        for j in range(1, target_sum + 1):
            if j < nums[i - 1]:
                dynamic_table[i][j] = dynamic_table[i - 1][j]
            else:
                dynamic_table[i][j] = dynamic_table[i - 1][j] or dynamic_table[i - 1][j - nums[i - 1]]

    if not dynamic_table[n][target_sum]:
        return None

    subset = []
    i, j = n, target_sum
    while i > 0 and j > 0:
        if dynamic_table[i][j] and not dynamic_table[i - 1][j]:
            subset.append(nums[i - 1])
            j -= nums[i - 1]
        i -= 1

    return subset

for subset in Sets:
    new_set = subset['nums']
    target = subset['target_sum']
    start_time = time.time()
    result = find_subset_with_sum(new_set, target)
    end_time = time.time()
    total_time = end_time - start_time
    print("Set selected:", new_set)
    print("Target:", target)
    print(f"Time of execution: {total_time:.4f}")
    if result:
        sum_result = sum(result)
        print("Subset with the target sum:", result)
        assert sum_result == target, "Sum result must be equal to target sum"

    else:
        print("No such subset exists.")
    print("================================")