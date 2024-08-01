import json
import random
import re

ideologies = json.load(open('testing/ideologies.json', encoding='utf-8'))
questions = json.load(open('testing/questions.json', encoding='utf-8'))

questions = [q['effect'] for q in questions]

possible_answers = [-1, -0.5, 0, 0.5, 1]

max_scores = {"econ": 0, "dipl": 0, "govt": 0, "scty": 0}
for q in questions:
    for k, v in q.items():
        max_scores[k] += abs(v)

def calc_final_score(score, maxi):
    return round(100*(maxi+score)/(2*maxi), 1)

def empty_scores():
    return {"econ": 0, "dipl": 0, "govt": 0, "scty": 0}

def get_target_ideology(ideology_name):
    for ideology in ideologies:
        if ideology['name'] == ideology_name:
            return ideology["stats"]
    return None

def calculate_distance(scores, target_ideology):
    dist = 0
    final_scores = {k: calc_final_score(v, max_scores[k]) for k, v in scores.items()}
    dist += abs(final_scores["econ"] - target_ideology["econ"]) ** 2
    dist += abs(final_scores["dipl"] - target_ideology["dipl"]) ** 1.73856063
    dist += abs(final_scores["govt"] - target_ideology["govt"]) ** 2
    dist += abs(final_scores["scty"] - target_ideology["scty"]) ** 1.73856063
    return dist

def calculate_ideology(answers):
    scores = empty_scores()
    for i, a in enumerate(answers):
        for k, v in answer_question(i, a).items():
            scores[k] += v
    min_distance = float('inf')
    best_ideology = None
    for ideology in ideologies:
        distance = calculate_distance(scores, ideology["stats"])
        if distance < min_distance:
            min_distance = distance
            best_ideology = ideology
    return best_ideology

def calculate_distance_of_answers(answers, target_ideology):
    scores = empty_scores()
    for i, a in enumerate(answers):
        for k, v in answer_question(i, a).items():
            scores[k] += v
    return calculate_distance(scores, target_ideology)

def answer_question(question_index, answer:int):
    return {k : v*answer for k, v in questions[question_index].items()}

def pointless_decision(answers, target_ideology):
    for a in possible_answers:
        if calculate_distance_of_answers(answers + [a], target_ideology) != calculate_distance_of_answers(answers, target_ideology):
            return False
    return True

def find_path(target_ideology_name):
    target_ideology = get_target_ideology(target_ideology_name)
    if target_ideology is None:
        return None
    answers = [0] * len(questions)
    previous_answers = answers.copy()
    while calculate_ideology(answers)["name"] != target_ideology_name:
        answers = previous_answers.copy()
        for i in range(len(answers)):
            best_answer = 0
            possible_answer_chains = [answers[:i] + [a] + answers[i+1:] for a in possible_answers]
            possible_distances = [calculate_distance_of_answers(a, target_ideology) for a in possible_answer_chains]
            best_answer = possible_answers[possible_distances.index(min(possible_distances))]
            answers[i] = best_answer
        if previous_answers == answers:
            break
        previous_answers = answers.copy()
    if calculate_ideology(answers)["name"] != target_ideology_name:
        return []
    return answers

# def find_path_recursive(target_ideology_name):
#     target_ideology = get_target_ideology(target_ideology_name)
#     if target_ideology is None:
#         return None
#     def backtrack(answers, target_ideology):
#         print(answers, calculate_ideology(answers)["name"])
#         if len(answers) == len(questions) or calculate_ideology(answers)["name"] == target_ideology_name:
#             return answers
#         min_distance = float('inf')
#         best_answers = None
#         if pointless_decision(answers, target_ideology):
#             return backtrack(answers + [0], target_ideology)
#         for answer in possible_answers:
#             answers.append(answer)
#             distance = calculate_distance_of_answers(answers, target_ideology)
#             if distance < min_distance:
#                 min_distance = distance
#                 best_answers = backtrack(answers, target_ideology)
#             answers.pop()
#         return best_answers
#     answers = backtrack([], target_ideology)
#     return answers

def find_paths():
    found = {k["name"]: [] for k in ideologies}
    for ideology in ideologies:
        found[ideology["name"]] = find_path(ideology["name"])
    return found

def print_results(answers):
    answer_names = ["Absolument pas d'accord", "Pas d'accord", "Neutre", "D'accord", "Absolument d'accord"]
    for i, a in enumerate(answers):
        print(f"Question {i + 1}: {answer_names[int(2*(a+1))]}")

if __name__ == "__main__":
    # json.dump(find_paths(), open('testing/found_paths.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    found_paths = json.load(open('testing/found_paths.json', encoding='utf-8'))
    print_results(found_paths["Bulgare"])