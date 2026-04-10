from services.quiz_service import run_quiz
from services.history_service import view_history

while True:
    choice = input("""
Choose:
1. New Quiz
2. View History
3. Exit
> """)

    if choice == "1":
        run_quiz()

    elif choice == "2":
        view_history()

    elif choice == "3":
        break

    else:
        print("Invalid choice")