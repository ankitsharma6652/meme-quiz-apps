from app import app, db, Comment, Upvote, QuizScore
from sqlalchemy import inspect

with app.app_context():
    inspector = inspect(db.engine)
    existing_tables = inspector.get_table_names()
    
    if 'comments' not in existing_tables:
        print("Creating comments table...")
        Comment.__table__.create(db.engine)
    else:
        print("Comments table already exists.")
        
    if 'upvotes' not in existing_tables:
        print("Creating upvotes table...")
        Upvote.__table__.create(db.engine)
    else:
        print("Upvotes table already exists.")
        
    if 'quiz_scores' not in existing_tables:
        print("Creating quiz_scores table...")
        QuizScore.__table__.create(db.engine)
    else:
        print("QuizScores table already exists.")
        
    print("Social tables migration completed.")
