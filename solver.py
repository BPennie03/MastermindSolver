import itertools


NUM_COLORS = 8
CODE_LENGTH = 4


def generate_codes():
    return [list(code) for code in itertools.product(range(1, NUM_COLORS + 1), repeat=CODE_LENGTH)]


def score_guess(guess, solution):
    correct_position = 0
    correct_color = 0
    secret_code_copy = list(solution)
    guess_copy = list(guess)

    for i in range(len(guess)):
        if guess[i] == solution[i]:
            correct_position += 1
            secret_code_copy[i] = None
            guess_copy[i] = None

    for color in guess_copy:
        if color is not None and color in secret_code_copy:
            correct_color += 1
            secret_code_copy[secret_code_copy.index(color)] = None

    feedback = 'R' * correct_position + 'W' * correct_color
    return feedback


def filter_possible_solutions(possible_solutions, guess, response):
    filtered_codes = []
    for code in possible_solutions:
        if score_guess(guess, code) == response:
            filtered_codes.append(code)
    return filtered_codes


def minimax(possible_solutions, all_codes):
    best_guess = None
    min_max_score = float('inf')

    for guess in all_codes:
        score_distribution = {}

        for code in possible_solutions:
            feedback = score_guess(guess, code)
            if feedback in score_distribution:
                score_distribution[feedback] += 1
            else:
                score_distribution[feedback] = 1

        # Find the worst-case scenario for this guess
        worst_case_score = max(score_distribution.values())

        # Choose the guess with the smallest worst-case score
        if worst_case_score < min_max_score:
            min_max_score = worst_case_score
            best_guess = guess

    return best_guess


def mastermind_solver():
    possible_solutions = generate_codes()
    all_codes = generate_codes()
    guess = [1, 1, 2, 2]  # Initial guess

    attempts = 0
    while True:
        print(f"Attempt {attempts + 1}: Guessing {guess}")

        response = input("Enter response (format: RRWW): ")

        if response == 'RRRR':
            print(f"Code found in {attempts + 1} attempts.")
            break

        # Filter possible solutions
        possible_solutions = filter_possible_solutions(
            possible_solutions, guess, response)
        print(f"\nPossible solutions remaining: {len(possible_solutions)}\n")

        if len(possible_solutions) == 1:
            print(f"The code is {possible_solutions[0]}.")
            break

        # Determine next guess using minimax
        guess = minimax(possible_solutions, all_codes)
        attempts += 1

        if not guess:
            print("No valid guess found. Algorithm may be stuck.")
            break


# Run the Mastermind solver
if __name__ == "__main__":
    mastermind_solver()
