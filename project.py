from pyfiglet import figlet_format as font
from random import choice
import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()


# Top display of the application.


print(font("Dune Entertainments."))


class Trivia:

    def __init__(self, categories=None, name=None, cate_choice=[], score=0):
        self.name = name
        self.cate_choice = cate_choice
        self.score = score
        self.categories = categories

    # Collect user information.

    def user_info(self):
        self.name = str(input("Enter your name here: "))
        if len(self.name) < 3 or self.name.strip() == "" or self.name == None:
            print("You've inputted an invalid name.")
            self.name = str(input("Enter your name here: "))

        return f"\nWelcome to the game {self.name.split(' ')[0]}."

    # Display available categories.

    def display_available_categories(self):
        categories = cur.execute('SELECT DISTINCT category FROM Questions;')
        self.categories = [''.join(category) for category in categories]
        [print(f"{index} - {category}")
         for index, category in enumerate(self.categories, start=1)]
        conn.commit()
        return "\nThese are the available categories.\nYou can only get one question each from three (3) categories.\nEach question earn you one (1) point which make the total of three (3) points.\nBe careful not to submit a blank question.\nThat's all it takes to qualify.\n\nMay the odds be ever in your favor.\n"

    # Allow user to make 3 choices of category from the available selection.

    def category_selection(self):
        try:
            while True:
                selection1 = int(
                    input("Select your first (1) category using it index number: "))

                if selection1 > len(self.categories):
                    print("You cannot choose an index outside the option.\n")
                else:
                    self.cate_choice.append(self.categories[selection1-1])
                    print(self.cate_choice)
                    break

            while True:
                selection2 = int(
                    input("Select your second (2) category using it index number: "))

                if (selection2 == selection1):
                    print("\nYou cannot choose same category multiply times.\n")

                elif selection2 > len(self.categories):
                    print("You cannot choose an index outside the option.\n")

                else:
                    self.cate_choice.append(self.categories[selection2-1])
                    print(self.cate_choice)
                    break

            while True:
                selection3 = int(
                    input("Select the last category using it index number: "))

                if (selection3 == selection2) or (selection3 == selection1):
                    print("\nYou cannot choose same category multiply times.\n")

                elif selection3 > len(self.categories):
                    print("You cannot choose an index outside the option.\n")

                else:
                    self.cate_choice.append(self.categories[selection3-1])
                    return f"{self.cate_choice}\n"
        except ValueError:
            return 'A number is expected as the index of the category, not an alphabet.'

    # Generate question for the user and keep score.

    def display_question(self):
        for i in range(3):
            question_from_cate = cur.execute(
                f"SELECT question, id FROM Questions WHERE category='{self.cate_choice[i]}' LIMIT 10")
            questions = [f"\nCatergory: {self.cate_choice[i]}\n\n{''.join(question)} - {_id}"
                         for question, _id in question_from_cate]

            question = choice(questions)
            question, _id = question.split(" - ")
            print(question)
            answer = cur.execute(
                f"SELECT answer FROM Answers INNER JOIN Questions ON {_id} = Answers.question_id")
            answer = [''.join(ans) for ans in answer][0]

            user_input = str(
                input("\nEnter your answer here by inputing either option a, b, c or d: ")).upper()

            if user_input == " " or len(user_input) == 0:
                print(
                    f"\n{self.name}, you cannot choose 'blank' as your answer.\n")

            elif answer.startswith(user_input):
                self.score += 1
                print(
                    f"\nCorrect!... You've now earned {self.score} point(s).\n")

            else:
                print(
                    f"\nOops!...That's incorrect. The correct answer is {answer}.\nYou still have {self.score} point(s).\n")

        conn.commit()
        return f"\nCongratulations!... You finished the round with {self.score} point(s).\n"

    # Add the name of the winners to the list.

    def collate_name(self):
        if self.score == 3:
            with open("winner_list.txt", "a+") as file:
                file.write(f"{self.name}\n")
                # file.seek(0)
                # return f"These are the names of the winners from the Quest.\n\n - {self.name}"
                return f"\nBig Congratulations to you {self.name} on qualifying for the main event of the Dune Entertainment.\n\n"
        return f"\nBetter luck next time {self.name}\n\n"


callback = Trivia()

print(callback.user_info())
print(callback.display_available_categories())
print(callback.category_selection())
print(callback.display_question())
print(callback.collate_name())


if __name__ == "__main__":
    conn.close()
