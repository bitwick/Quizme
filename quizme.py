import os
import random
from datetime import datetime

# GLOBALS
QUIZES_LOCATION = "quizes"

# FUNCTIONS
def GetAvailableQuizes(location):
    quizes = []
    for root, dirs, files in os.walk(location):
        for file in files:
            if not file == ".gitignore":
                quizes.append(file)
    return quizes

def PickQuiz(quizes):
    i = 1
    for quiz in quizes:
        print("%d.) %s" %(i,quiz))
        i += 1
    choice = int(input("Select: "))
    return quizes[choice-1]

def BuildQuiz(quiz):
    
    # Local Variables
    filepath = os.path.join(QUIZES_LOCATION, quiz)
    terms = []
    termsLibrary = []

    # Reading quiz file and creating a term array
    with open(filepath, "r", encoding="utf8") as termData:
        for line in termData:
           terms.append(line.rstrip('\n'))

    # Processing Glossary Terms for quiz output
    termsLibrary = ProcessTermsForQuiz(terms)

    return RandomizeSelection(termsLibrary)    

def ProcessTermsForQuiz(terms):
    termsLibrary = []
    for term in terms:
        pair = term.split('\t', 1 )
        termsLibrary.append({"Term":pair[0], "Definition":pair[1]})
    return termsLibrary

def GetRandomNumber(minSize, maxSize):
    randNumb = random.randint(minSize, maxSize - 1)
    return randNumb

def RandomizeSelection(termsLibrary):
    
    # Variables
    maxChoice = 3
    totalChoices= [0,1,2,3]
    currentPosition = 0
    finalQuiz = []
    questionDict = {"Term":"", "Definition":"","Answer":False}
    questionArrayStraight = []
    questionArrayRandom = []
    randomNumberSelection = []

    # Process Answers into groups of questions
    for term in termsLibrary:

        # Randomize order of choices
        random.shuffle(totalChoices)
        
        # Record correct Answer
        questionDict['Term'] = term['Term']
        questionDict['Definition'] = term['Definition']
        questionDict['Answer'] = True
        qdCopy = questionDict.copy()
        questionArrayStraight.append(qdCopy)
        randomNumberSelection.append(currentPosition)
        
        # Add 3 additional definitions to multipe choices
        for i in range(maxChoice):
            # Pull definition from array from random position    
            randomNumber = GetRandomNumber(0, len(termsLibrary))

            # Cannot add defition if it is current term
            while randomNumber == currentPosition:
                randomNumber = GetRandomNumber(0, len(termsLibrary))

            # Cannot add defition if defition already has been selected
            for number in randomNumberSelection:
                while number == randomNumber:
                    randomNumber = GetRandomNumber(0, len(termsLibrary))

            # Add defition to list of possible answers
            randomNumberSelection.append(randomNumber)
            questionDict['Term'] = termsLibrary[randomNumber]['Term']
            questionDict['Definition'] = termsLibrary[randomNumber]['Definition']
            questionDict['Answer'] = False
            qdCopy = questionDict.copy()
            randomNumberSelection.append(currentPosition)
            questionArrayStraight.append(qdCopy)                 

        
        # Randomize Answer positions
        for i in totalChoices:
            questionArrayRandom.append(questionArrayStraight[i])
        
        # Add subset answers to final quiz
        finalQuiz.append(questionArrayRandom)
        
        # Increment and Reset
        currentPosition += 1
        questionArrayStraight = []
        questionArrayRandom = []
        randomNumberSelection = []
    
    random.shuffle(finalQuiz)
    return finalQuiz

def Clear():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

def PlayQuizGame(quiz):

    totalQuestions = len(quiz)
    correctAnswer = 0
    grade = 0
    quitFlag = False

    print("####################################################")
    print("# Welcome to the quiz game.")
    print("# There are a total of %d questions." %(totalQuestions))
    print("# You can quit anytime by entering '5' as a choice.")
    print("####################################################\n\n\n")

    for questions in quiz:
        i = 1
        answer = ""

        for question in questions:
            if question['Answer'] == True:
                print("Select best definition for %s\n" %(question['Term']))
                answer = question['Definition']
        
        for question in questions:
            print("%d.) %s\n" %(i,question['Definition']))
            i += 1

        choiceMade = int(input("Select Answer: ")) - 1

        if choiceMade == 4:
            quitFlag = True
            break
        elif (questions[choiceMade]['Answer'] == True):
            correctAnswer += 1
        else:
            print("Correct Answer:\n %s" %(answer))
            input("Hit any key for next question.")

        if quitFlag == True:
            break
        
        Clear()
    # Calculate Grade
    grade = (correctAnswer / totalQuestions) * 100
    print("Answers: %d / %d" %(correctAnswer, totalQuestions))
    print("Grade: %d%% " %(grade))
    input("Hit any key to exit.")

# MAIN
if __name__ == "__main__":
    # Get all available quizes
    quizes = GetAvailableQuizes(QUIZES_LOCATION)
    
    # Select which quiz user wants to take
    quizName = PickQuiz(quizes)

    # Build Quiz
    quiz = BuildQuiz(quizName)

    # Start Quiz
    PlayQuizGame(quiz)

    