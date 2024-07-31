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

def Del_access(book_id, user_id):
    book_access = BookAccess.query.filter_by(book_id=book_id, user_id=user_id).first()
    books=Books.query.filter_by(id=book_id).first()
    if book_access:
        db.session.add(History(book_id=book_id, user_id=user_id, issue_date=book_access.issue_date, return_date=book_access.return_date,name=books.name,author=books.author))
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