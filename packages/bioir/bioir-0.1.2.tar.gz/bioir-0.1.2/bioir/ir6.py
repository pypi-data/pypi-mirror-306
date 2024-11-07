print("""import numpy as np
adj_matrix = np.array([[0,1,1,0],
                       [0,0,1,1],
                       [1,0,0,1],
                       [0,0,1,0]])
n = len(adj_matrix)
transition_matrix = np.zeros((n,n))

for i in range(n):
    row_sum = np.sum(adj_matrix[i])

    if row_sum == 0:
        transition_matrix[i] = 1 / n
    else:
        transition_matrix[i] = adj_matrix[i] / row_sum


damping_factor = 0.85
num_iterations = 100
tolerance = 1e-6

page_rank = np.ones(n) / n

for i in range(num_iterations):
    new_page_rank = (1-damping_factor) / n + damping_factor * transition_matrix.T @ page_rank

    if np.linalg.norm(new_page_rank - page_rank,ord=1) < tolerance:
        print('converged')
        break

    page_rank = new_page_rank """)