from .db_config import db

def save_option(quiz,options):
    """
    Save quiz and associated options to MongoDB.

    Args:
     quiz (dict): The quiz data to save.
     options (list of dict): The options data to save.
    """
    try:
        # Insert options into 'options' collection
        db.options.insert_many(options)

        # Insert quiz into 'quizzes' collection
        db.quizzes.insert_one(quiz)

        print("Quiz and options saved successfully!")
    except Exception as e:
        print(f"An error occurred while saving to MongoDB: {e}")
        raise

def submit_quizz(quizz_feedback):
    pass

def mark_end_of_game(request):
    pass

