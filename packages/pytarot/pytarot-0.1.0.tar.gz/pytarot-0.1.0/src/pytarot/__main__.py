import pytarot.truelover as truelover_module
import pytarot.luckyday as luckyday_module
import pytarot.answersofwisdom as answers_of_wisdom_module
import pytarot.positive_action as positive_action_module
import sys


def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "get_trueLover":
            get_trueLover()
        elif command == "get_luckyDay":
            get_luckyDay()
        elif command == "get_answersOfWisdom":
            get_answersOfWisdom()
        elif command == "get_positiveAction":
            get_positiveAction()
        else:
            print("Invalid command. Please choose from get_trueLover, get_luckyDay, get_answersOfWisdom, or get_positiveAction.")
    else:
        print(
            "Welcome to Pytarot!\n"
            "Choose a command to receive your reading:\n"
            "  - get_trueLover: Get details about your true lover\n"
            "  - get_luckyDay: Find out your lucky day\n"
            "  - get_answersOfWisdom: Receive some words of wisdom\n"
            "  - get_positiveAction: Get a positive action message"
        )

def get_trueLover():
    line = truelover_module.get_true_lover()
    print(line)

def get_luckyDay():
    line = luckyday_module.get_lucky_day()
    print(line)

def get_answersOfWisdom ():
    line = answers_of_wisdom_module.get_answers_of_wisdom()
    print(line)

def get_positiveAction ():
    line = positive_action_module.get_positive_action()
    print(line)


if __name__ == "__main__":
    main()
