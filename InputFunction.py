def get_values(): 
    questions = ["How would you like to weigh the random walk model?", "How would you like to weigh the density model?", "How would you like to weigh the cloud model?", "How would you like to weigh the cluster model?", "How much would you like the kid nodes' angles to vary from their parents'?","How much would you like the sibling nodes' angles to vary from each other?","How much would you like the kid nodes' angles to vary from the guiding angle?"]
    answers = []
    index = 0
    while index < len(questions):
        print(questions[index])
        answer = input()
        index += 1
        try:
            num_answer = float(answer)
            answers.append(num_answer)
        except (ValueError, TypeError):
            index -= 1
    return answers

print(get_values())
