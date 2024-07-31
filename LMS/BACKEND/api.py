from flask_restful import Resource, Api, marshal, reqparse, fields, marshal_with
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from Cache import cache
# from model_func import AddProduct, DeleteCategory, DeleteProduct, EditCategory, ProductUpdate, addcart, cartProducts, \
#     deleteProductCart, product, profileItems, updateQuantity, validateCategory_id, \
#     validateCategory_name, validateProduct, Adminsignin, Managersignin, fetch_all_user, AddCategory, all_product, \
#     validateProduct_name, fetch_category, fetch_category_unapproved, EditCategory_ia, EditCategory_name, \
#     fetch_cat_by_id, get_all_prod_by_cat_id, validateCategoryApproved, fetch_pending_user, validateManager, deleteUser
from flask import abort, jsonify, request,make_response
from model_func import all_section,add_section,get_section_by_id,edit_section,del_section,Add_book,edit_book,del_book,edit_book_access,edit_is_approve,Del_access
from models import db, Books,History
# from task import send_welcome_msg, generate_csv
import datetime
from models import db, Books, Section,  User, BookSection,BookAccess,RolesUsers,Ratings
from flask_security import SQLAlchemySessionUserDatastore, Security, login_user, logout_user
from flask_security import current_user, auth_required, login_required, roles_required, roles_accepted,login_user, logout_user,auth_token_required
from sqlalchemy import and_

api = Api(prefix='/api')





class Homepage(Resource):
    def get(self):
        return {"hello": "World"}


##############################  LIBRARIAN FUNCTIONALITY ##########################################3

now = datetime.datetime.now()
date = now.strftime("%B %d, %Y")
# Output: April 12, 2023

def add_days_to_date(date_str, days_to_add):
    # Parse the input date string
    date_obj = datetime.datetime.strptime(date_str, "%B %d, %Y")
    
    # Add the specified number of days
    final_date_obj = date_obj + datetime.timedelta(days=days_to_add)
    
    # Convert the final date back to the desired string format
    final_date_str = final_date_obj.strftime("%B %d, %Y")
    
    return final_date_str


sec=reqparse.RequestParser()
sec.add_argument('name')
sec.add_argument('desc')

section_update=reqparse.RequestParser()
section_update.add_argument('name')
section_update.add_argument('desc')


SECTION_ALL = {
    'name': fields.String,
    'id': fields.Integer,
    'date_created': fields.String,
    'desc' : fields.String
}


class add_sec(Resource):
    # @cache.cached(timeout=15)
    @auth_required('token')
    def get(self):
        sec=all_section()
        return jsonify(marshal(sec,SECTION_ALL))
    @auth_required('token')
    @roles_accepted('librarian')
    # @cache.cached(timeout=15)
    def post(self):
        data=sec.parse_args()
        name=data['name']
        desc=data['desc']
        print(name,desc)
        add_section(name,date,desc)
        response_data = {"message": "Section added"}
        response = make_response(jsonify(response_data), 200)  
        return response
    
class sec_update_del(Resource):
    @marshal_with(SECTION_ALL)
    @auth_required('token')
    def get(self,id):
        section_update=get_section_by_id(int(id))
       
        if section_update:
            
            return marshal(section_update,SECTION_ALL)

        else:
         
            return "error"
   
    @auth_required('token')
    @roles_accepted('librarian')
    def put(self,id):
        data=section_update.parse_args()
        name=data['name']
        desc=data['desc']
       
        flag=db.session.query(Section).filter(Section.id==id).first()
        if flag:
            edit_section(id,name,desc)
            return jsonify({"message":"section name and description changed"})
        else:
            return "error"
    @auth_required('token')
    @roles_accepted('librarian')
    def delete(self, id):
        flag=db.session.query(Section).filter(Section.id==id).first()
        if flag:
            x=del_section(id)
            print(x)
            return jsonify({"message":"section deleted"})
        else:
            return "error"
        


api.add_resource(Homepage, '/')
api.add_resource(add_sec, '/sections')
api.add_resource(sec_update_del, '/sections/<id>')


###### BOOKS CRUD ######

book=reqparse.RequestParser()
book.add_argument('name')
book.add_argument('author')
book.add_argument('content')
book.add_argument('section_id')
# book.add_argument('section_id')

BOOK_ALL = {
    'name': fields.String,
    'id': fields.Integer,
    'section_id': fields.Integer,
    'author' : fields.String,
    'content': fields.String,
    'avg_rating': fields.Float  # Add this field to include average rating
    
}

class add_book(Resource):
    @auth_required('token')

    def get(self):
        books = Books.query.all()
        book_list = []

        for book in books:
            avg_rating = db.session.query(func.avg(Ratings.rating)).filter(Ratings.book_id == book.id).scalar()
            avg_rating = avg_rating if avg_rating is not None else 0
            book_data = {
                'name': book.name,
                'id': book.id,
                'section_id': book.section_id,
                'author': book.author,
                'content': book.content,
                'avg_rating': avg_rating
            }
            book_list.append(book_data)
        
        return jsonify(book_list)
    @auth_required('token')
    @roles_accepted('librarian')
    def post(self):
        data=book.parse_args()  
        name=data['name']
        author=data['author']
        content=data['content']
        section_id=data['section_id']
        Add_book(name, author, content, section_id)

        return jsonify({"message":"book added"})

class book_update_del(Resource):
    @marshal_with(BOOK_ALL)

    def get(self, id):
        book_update = Books.query.filter_by(id=id).first()

        if book_update:
            # Calculate the average rating for the book
            avg_rating = db.session.query(func.avg(Ratings.rating)).filter(Ratings.book_id == book_update.id).scalar()
            avg_rating = avg_rating if avg_rating is not None else 0
            book_update.avg_rating = avg_rating

            return book_update
        else:
            return {"message": "Book not found"}, 404
    @auth_required('token')
    @roles_accepted('librarian')

    def put(self, id):
        data=book.parse_args()
        name=data['name']
        author=data['author']
        content=data['content'] 
        section_id=data['section_id']
        flag=db.session.query(Books).filter(Books.id==id).first()
        ## check if the section id is a part of secondary section
        
        if flag:
            flag1=db.session.query(BookSection).filter_by(section_id=section_id, book_id=id).first()
            if flag1:
                return "Already exist as secondary section"
            edit_book(id, name, author, content, section_id)
            return jsonify({"message":"book updated"})
        else:
            return "error"
    @auth_required('token')
    @roles_accepted('librarian')
    def delete(self, id):
        flag=db.session.query(Books).filter(Books.id==id).first()
        if flag:
            del_book(id)
            return jsonify({"message":"book deleted"})
        else:
            return "error"
        

api.add_resource(add_book, '/books')
api.add_resource(book_update_del, '/books/<id>')

### ADD SECONDARY SECTIONS TO BOOKS #####

book_section=reqparse.RequestParser()
book_section.add_argument('section_id')
book_section.add_argument('book_id')
book_section.add_argument('section_name')


BOOK_SEC_ALL={
    'section_id': fields.Integer,
    'book_id': fields.Integer,
    'section_name': fields.String

}

class book_sec(Resource):
    @auth_required('token')
    def get(self):
        books=BookSection.query.all()
        print(books)
        return marshal(books, BOOK_SEC_ALL)
    # @auth_required('token')
    def post(self):
        data=book_section.parse_args()
        section_id=data['section_id']
        book_id=data['book_id']
        section_name=data['section_name']
        ## check if it is already a primary section in book db
        flag1=db.session.query(Books).filter_by(id=book_id, section_id=section_id).first()
        flag=db.session.query(BookSection).filter_by(section_id=section_id, book_id=book_id).first()
        if flag :
            return "Already exist as secondary section"
        if flag1:
            return "Already exist as primary section"
        # try:
        new_section = BookSection(section_id=section_id, book_id=book_id, section_name=section_name)
        db.session.add(new_section)
        db.session.commit()
        #except:
            #return "error"
        return jsonify({"message":"book secondary section added"})
    @auth_required('token')
    def delete(self):
        data=book_section.parse_args()
        section_id=data['section_id']
        book_id=data['book_id']
        flag=db.session.query(BookSection).filter_by(section_id=section_id, book_id=book_id).first()
        if flag:
            db.session.delete(BookSection.query.filter_by(section_id=section_id, book_id=book_id).first())
            db.session.commit()
            return jsonify({"message":"book secondary section deleted"})
        else:
            return "error"
api.add_resource(book_sec, '/secondarysection')

####### BOOK ACCESS #######

book_access=reqparse.RequestParser()
book_access.add_argument('user_id')
book_access.add_argument('no_of_days')
book_access.add_argument('book_id')

put_access=reqparse.RequestParser()
put_access.add_argument('user_id')
put_access.add_argument('no_of_days')
put_access.add_argument('issue_date')
put_access.add_argument('is_approve')
put_access.add_argument('book_id')

edit_access=reqparse.RequestParser()
edit_access.add_argument('is_approved')
edit_access.add_argument('user_id')
edit_access.add_argument('book_id')

del_access=reqparse.RequestParser()
del_access.add_argument('user_id')
del_access.add_argument('book_id')



BOOK_ACCESS = {
    'user_id': fields.String,
    'is_approved': fields.Integer,
    'no_of_days': fields.Integer,
    'issue_date': fields.String,
    'return_date': fields.String,
    'book_id': fields.Integer
}

class Book_access(Resource):
    @auth_required('token')

    def get(self):
        books=BookAccess.query.all()
        return marshal(books, BOOK_ACCESS)
    @auth_required('token')
    def post(self):
        token = request.headers.get('Authentication-Token')
        print("Received Token:", token)  # Add this line for debugging
        data=book_access.parse_args()
        user_id=data['user_id']
        book_id=data['book_id']
        is_approved=0
        issue_date=None
        return_date=None
        no_of_days=data['no_of_days']
        
        ## count the number of books got by user
        print(user_id)
        check = db.session.query(BookAccess).filter(
    and_(
        BookAccess.user_id == user_id,
        BookAccess.book_id == book_id,
        BookAccess.is_approved != -1
    )
).count()
        if check>0:
            return jsonify({"message":"book already requested or curretly accessed"})
        x = db.session.query(BookAccess).filter(and_(BookAccess.user_id == user_id,BookAccess.is_approved != -1)).count()
        if x>=5:
           print(x)
           return jsonify({"message":"you can't request more than 5 books"})
        
        
        z=y = db.session.query(BookAccess).filter(
    and_(
        BookAccess.user_id == user_id,
        BookAccess.book_id == book_id,
        BookAccess.is_approved == -1
    )
).count()
        if z>0:
            book_access1 = BookAccess.query.filter_by(book_id=book_id, user_id=user_id).first()
            book_access1.is_approved=0
            book_access1.no_of_days=no_of_days
            db.session.commit()
            return jsonify({"message":"book requested again after rejection"})
        db.session.add(BookAccess(user_id=user_id, is_approved=is_approved,  issue_date=issue_date, return_date=return_date, book_id=book_id,no_of_days=no_of_days))
        db.session.commit()
        return jsonify({"message":"book requested"})
    @auth_required('token')
    @roles_accepted('librarian')
    def put(self):
        data=book_access.parse_args()
        user_id=data['user_id']
        is_approved=data['is_approved']
        issue_date=data['issue_date']
        no_of_days=data['no_of_days']
        return_date=add_days_to_date(issue_date, int(no_of_days))
        book_id=data['book_id']
        flag=db.session.query(BookAccess).filter_by(book_id=book_id,user_id=user_id).first()
        if flag:
            edit_book_access(book_id, user_id, is_approved,  issue_date, return_date,no_of_days)
            return jsonify({"message":"book access updated"})
        else:
            return "error"
    @auth_required('token')
    @roles_accepted('librarian')
    def patch(self):
        data=edit_access.parse_args()
        user_id=data['user_id']
        id=data['book_id']
        is_approved=data['is_approved']
        
        
        print(is_approved)
        flag=db.session.query(BookAccess).filter_by(book_id=id, user_id=user_id).first()
        print(flag)
        if flag:
            if int(is_approved)==1:

                issue_date=date
                return_date=add_days_to_date(issue_date, int(flag.no_of_days))
                edit_is_approve(id, user_id, is_approved,issue_date,return_date)
                return jsonify({"message":"book is_approve updated"})
            elif int(is_approved)==-1:
                print("hi")
                book_access1 = BookAccess.query.filter_by(book_id=id, user_id=user_id).first()
                print(book_access1)
                book_access1.is_approved=-1
                db.session.commit()
                return jsonify({"message":"book is_approve updated"})
            
            else:
                return jsonify({"message":"error book is_approve"})
        else:
            return jsonify({"message":"errorrrr"})
    
    def delete(self):
        data=del_access.parse_args()
        user_id=data['user_id'] 
        id=data['book_id']
        flag=db.session.query(BookAccess).filter_by(book_id=id, user_id=user_id).first()
        if flag:
            t=Del_access(id, user_id)
            if t:
                return jsonify({"message":"book access deleted"})
        else:
            return "error"

api.add_resource(Book_access, '/bookaccess')

USER_ALL={
    'lname': fields.String,
    'fname': fields.String,
    'mobile_no': fields.String,
    'email': fields.String,
    'id': fields.String
}
class users(Resource):
    @auth_required('token')
    @roles_accepted('librarian')
    def get(self):
        subquery = db.session.query(RolesUsers.user_id).filter(RolesUsers.role_id == 2).subquery()
        users=db.session.query(User).filter(User.id.in_(subquery)).all()
        return marshal(users, USER_ALL)

api.add_resource(users, '/users')
        
    
HISTORY_ACCESS = {
    'user_id': fields.String,
    'name': fields.String,
    'author': fields.String,
    'issue_date': fields.String,
    'return_date': fields.String,
    'book_id': fields.Integer
}
class history(Resource):
    @auth_required('token')
    def get(self):
        history=History.query.all()
        return marshal(history, HISTORY_ACCESS)
api.add_resource(history, '/history')

RATING_FIELDS = {
    'id': fields.Integer,
    'book_id': fields.Integer,
    'user_id': fields.String,
    'rating': fields.Integer,
}

class RatingsResource(Resource):
    @auth_required('token')
    def get(self, book_id, user_id):
        rating = Ratings.query.filter_by(book_id=book_id, user_id=user_id).first()
        if not rating:
            return {'rating': None}
        return {'rating': rating.rating}
    
    @auth_required('token')
    def post(self):
        data = request.get_json()
        rating = Ratings.query.filter_by(book_id=data['book_id'], user_id=data['user_id']).first()
        if rating:
            rating.rating = data['rating']
        else:
            rating = Ratings(book_id=data['book_id'], user_id=data['user_id'], rating=data['rating'])
            db.session.add(rating)
        db.session.commit()
        return {'message': 'Rating added/updated successfully'}

api.add_resource(RatingsResource, '/ratings/<int:book_id>/<string:user_id>', '/ratings')


BOOK_ALL = {
    'name': fields.String,
    'id': fields.Integer,
    'section_id': fields.Integer,
    'author' : fields.String,
    'content': fields.String,
}

SECTION_ALL = {
    'name': fields.String,
    'id': fields.Integer,
    'date_created': fields.String,
    'desc' : fields.String
}
class search(Resource):
    @auth_required('token')
    def get(self, searchQuery):
        searchQuery = searchQuery.lower()

        # Search for sections by name
        sections = Section.query.options(joinedload(Section.books)).filter(func.lower(Section.name).contains(searchQuery)).all()

        # Search for books by name or author
        books = Books.query.filter(
            func.lower(Books.name).contains(searchQuery) |
            func.lower(Books.author).contains(searchQuery)
        ).all()

        # Collect section IDs of the found books
        book_section_ids = {book.section_id for book in books}
        
        # Fetch sections of the found books
        book_sections = Section.query.options(joinedload(Section.books)).filter(Section.id.in_(book_section_ids)).all()

        results = {
            'sections': [],
            'books': [marshal(book, BOOK_ALL) for book in books]
        }

        # Prepare section results with their books
        for section in set(sections + book_sections):
            section_data = marshal(section, SECTION_ALL)
            section_data['books'] = [marshal(book, BOOK_ALL) for book in section.books]
            results['sections'].append(section_data)

        return jsonify(results)


api.add_resource(search, '/search/<string:searchQuery>')

class AvgRatings(Resource):
    @auth_required('token')
    def get(self, book_id):
        ratings = Ratings.query.filter_by(book_id=book_id).all()
        if not ratings:
            return {'ratings': []}
        ratings_list = [{'user_id': rating.user_id, 'rating': rating.rating} for rating in ratings]
        return {'ratings': ratings_list}
api.add_resource(AvgRatings,'/ratings/<int:book_id>')