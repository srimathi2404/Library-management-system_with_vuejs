from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text, cast , Text, and_
from sqlalchemy import extract
import json
from models import db, Books, Section,  User, BookSection,BookAccess,History

from flask import current_app as app, jsonify

def all_section():
    return Section.query.all()
def add_section(name, date, description):
    section = Section(name=name, date_created=date, desc=description)
    db.session.add(section)
    db.session.commit()
def get_section_by_id(id):
    return Section.query.filter_by(id=id).first()
def edit_section(id,name,desc):
    section = Section.query.filter_by(id=id).first()
    section.name = name
    section.desc = desc
    db.session.commit()
def del_section(id):
    # Start a session
    session = db.session
    
    # Check if the section exists
    section = session.query(Section).filter_by(id=id).first()
    if not section:
        return "Section not found", 404

    try:
        # Subquery to find book IDs in the given section
        book_ids_subquery = session.query(Books.id).filter(Books.section_id == id).subquery()
        
        # Delete entries in BookAccess with book IDs in the subquery
        session.query(BookAccess).filter(BookAccess.book_id.in_(book_ids_subquery)).delete(synchronize_session=False)

        # Optionally delete entries in History with book IDs in the subquery
        # session.query(History).filter(History.book_id.in_(book_ids_subquery)).delete(synchronize_session=False)
        
        # Delete books with the given section ID
        session.query(Books).filter(Books.section_id == id).delete(synchronize_session=False)

        # Delete book sections with the given section ID
        session.query(BookSection).filter(BookSection.section_id == id).delete(synchronize_session=False)
        
        # Finally, delete the section itself
        session.delete(section)
        
        # Commit the transaction to persist changes
        session.commit()
        
        return "Section and related entries deleted successfully", 200

    except Exception as e:
        # Rollback the transaction in case of an error
        session.rollback()
        return f"An error occurred: {str(e)}", 500

    finally:
        # Close the session
        session.close()



def Add_book(name, author, content, section_id):
    book = Books(name=name, author=author, content=content, section_id=section_id)
    db.session.add(book)
    db.session.commit()
   
def edit_book(id, name, author, content, section_id):
    book=Books.query.filter_by(id=id).first()
    book.name=name
    book.author=author
    book.content=content
    
    book.section_id=section_id
    db.session.commit()
def del_book(id):
    # delete the books from book access
    db.session.query(BookAccess).filter(BookAccess.book_id == id).delete()
    db.session.query(BookSection).filter(BookSection.book_id == id).delete()
    book=Books.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()

def edit_book_access(book_id,user_id,issue_date,return_date,is_approved):
    book_access = BookAccess.query.filter_by(book_id=book_id, user_id=user_id).first()
    if book_access:
        book_access.issue_date = issue_date
        book_access.return_date = return_date
        book_access.is_approved = is_approved

        db.session.commit()
        return True
    else:
        return False
def edit_is_approve(book_id, user_id, is_approved,issue_date,return_date):
    book_access = BookAccess.query.filter_by(book_id=book_id, user_id=user_id).first()
    if book_access:
        book_access.is_approved = is_approved
        book_access.issue_date = issue_date
        book_access.return_date = return_date
        db.session.commit()
        return True
    else:
        return False

from datetime import datetime

def Del_access(book_id, user_id):
    book_access = BookAccess.query.filter_by(book_id=book_id, user_id=user_id).first()
    books = Books.query.filter_by(id=book_id).first()
    if book_access:
        now = datetime.now()
        date = now.strftime("%B %d, %Y")
        
        db.session.add(History(book_id=book_id, user_id=user_id, issue_date=book_access.issue_date, return_date=date, name=books.name, author=books.author))
        db.session.delete(book_access)
        db.session.commit()
        return True
    else:
        return False
    

def exportdetails():
    result = db.session.query(
        Books.name,
        func.count(BookAccess.id).label('total_access_count')
    ).join(BookAccess, Books.id == BookAccess.book_id) \
        .group_by(Books.id).all()
    return result


def get_monthly_accessed_books(user_id, year, month):
    # Fetch books accessed by the user in a specific month and year
    result = db.session.query(BookAccess, Books).join(Books).filter(
        BookAccess.book_id == Books.id,
        BookAccess.user_id == user_id,
        extract('year', BookAccess.issue_date) == year,
        extract('month', BookAccess.issue_date) == month
    ).all()
    print(result)
    return result


from datetime import datetime
def get_returned_books_today():
    # Get today's date in the same format as stored in the database
    today = datetime.now().strftime("%B %d, %Y")
    
    # Query all book accesses that are approved
    book_accesses = BookAccess.query.filter_by(is_approved=1).all()
    
    reminders = {}

    for access in book_accesses:
        return_date = access.return_date  # This should be in the format "%B %d, %Y"
        if return_date == today:
            user_id = access.user_id
            book_id = access.book_id
            
            # Fetch the book details
            book = Books.query.filter_by(id=book_id).first()
            if book:
                book_name = book.name
                if user_id not in reminders:
                    reminders[user_id] = []
                reminders[user_id].append(book_name)
    
    return reminders

def get_other_books():
    # Get today's date in the same format as stored in the database
    today = datetime.now().strftime("%B %d, %Y")
    
    # Query all book accesses that are approved
    book_accesses = BookAccess.query.filter_by(is_approved=1).all()
    
    other_books = {}

    for access in book_accesses:
        return_date = access.return_date  # This should be in the format "%B %d, %Y"
        if return_date and return_date != today:  # Omit null values and today's date
            user_id = access.user_id
            book_id = access.book_id
            
            # Fetch the book details
            book = Books.query.filter_by(id=book_id).first()
            if book:
                book_name = book.name
                if user_id not in other_books:
                    other_books[user_id] = []
                other_books[user_id].append((book_name, return_date))
    
    return other_books



from datetime import datetime, timedelta

def get_monthly_report_data():
    first_day_of_month = datetime.now().replace(day=1)
    first_day_of_next_month = (first_day_of_month + timedelta(days=31)).replace(day=1)

    history_records = History.query.filter(
        History.return_date >= first_day_of_month.strftime("%B %d, %Y"),
        History.return_date < first_day_of_next_month.strftime("%B %d, %Y")
    ).all()
    
    report_data = {}

    for record in history_records:
        user_id = record.user_id
        book_id = record.book_id
        
        user = User.query.filter_by(id=user_id).first()
        book = Books.query.filter_by(id=book_id).first()
        
        if user and book:
            if user_id not in report_data:
                report_data[user_id] = {
                    'username': user.id,  # Use the 'id' field for the username
                    'email': user.email,
                    'books': []
                }
            report_data[user_id]['books'].append({
                'book_name': book.name,
                'author': book.author,
                'issue_date': record.issue_date,
                'return_date': record.return_date
            })
    
    return report_data

def remove_expired_book_access():
    today = datetime.now().strftime("%B %d, %Y")
    
    # Query all book accesses with return date today or before
    expired_book_accesses = BookAccess.query.filter(BookAccess.return_date <= today).all()
    
    expired_dict = []
    for access in expired_book_accesses:
        expired_dict.append({
            'user_id': access.user_id,
            'book_id': access.book_id
        })
    
    return expired_dict

import os
import csv
def export_ebook_access_to_csv():
    today = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ebook_access_{today}.csv"
    export_dir = "C:\\Users\\18049\\Desktop\\exports"  # Ensure this directory exists
    filepath = os.path.join(export_dir, filename)

    # Ensure the export directory exists
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    book_accesses = BookAccess.query.all()
    
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['User ID', 'Book ID', 'Name', 'Content', 'Author(s)', 'Date Issued', 'Return Date','is_approved']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for access in book_accesses:
            book = Books.query.filter_by(id=access.book_id).first()
            user = User.query.filter_by(id=access.user_id).first()
            writer.writerow({
                'User ID': access.user_id,
                'Book ID': access.book_id,
                'Name': book.name,
                'Content': book.content,
                'Author(s)': book.author,
                'Date Issued': access.issue_date,
                'Return Date': access.return_date,
                'is_approved': access.is_approved
            })

    return filepath