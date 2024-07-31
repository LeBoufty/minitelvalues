import json
import random
import re

ideologies = json.load(open('testing/ideologies.json', encoding='utf-8'))
questions = json.load(open('testing/questions.json', encoding='utf-8'))

questions = [q['effect'] for q in questions]

possible_answers = [-1, -0.5, 0, 0.5, 1]

def empty_scores():
    return {"econ": 0, "dipl": 0, "govt": 0, "scty": 0}

def get_target_ideology(ideology_name):
    for ideology in ideologies:
        if ideology['name'] == ideology_name:
            return ideology["stats"]
    return None

def calculate_distance(scores, target_ideology):
    dist = 0
    dist += abs(scores["econ"] - target_ideology["econ"]) ** 2
    dist += abs(scores["dipl"] - target_ideology["dipl"]) ** 1.73856063
    dist += abs(scores["govt"] - target_ideology["govt"]) ** 2
    dist += abs(scores["scty"] - target_ideology["scty"]) ** 1.73856063
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

def find_paths():
    try: found = json.load(open('testing/found_paths.json', encoding='utf-8'))
    except: found = {k["name"]: None for k in ideologies}
    for j in range(100000):
        answers = [random.choice(possible_answers) for _ in range(len(questions))]
        if found[calculate_ideology(answers)["name"]] is None:
            found[calculate_ideology(answers)["name"]] = answers
    return found

# def find_path(target_ideology_name):
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

def print_results(answers):
    answer_names = ["Absolument pas d'accord", "Pas d'accord", "Neutre", "D'accord", "Absolument d'accord"]
    for i, a in enumerate(answers):
        print(f"Question {i + 1}: {answer_names[int(2*(a+1))]}")

if __name__ == "__main__":
    found = json.load(open('testing/found_paths.json', encoding='utf-8'))
    print_results(found["REACH OUT TO THE TRUTH"])