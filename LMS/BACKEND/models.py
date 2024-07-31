from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, Index
db = SQLAlchemy()
class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True ,autoincrement=True)
    user_id = db.Column( db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column( db.Integer, db.ForeignKey('role.id'))
    


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.String, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname= db.Column(db.String(255),  nullable=False)
    mobile_no=db.Column(db.Integer)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    authenticated = db.Column(db.Integer)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    # role=db.Column(db.String)
    active = db.Column(db.Boolean, default=True) 
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))
    
    @property
    def is_authorised(self):
        return self.authenticated
    
    @property
    def get_roles(self):
        return [role.name for role in self.roles]
    
    def __repr__(self):
        return '<User %r>' % self.email
class Section(db.Model):
    __tablename__ = 'Section'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.JSON, unique=True)
    date_created=db.Column(db.String)
    desc=db.Column(db.String)
    books = db.relationship("Books")
    book_sections = db.relationship('BookSection', back_populates='section')
    def __repr__(self):
        return '<Section %r>' % self.name
    @hybrid_property
    def lowercased_name(self):
        return self.name.lower()

    __table_args__ = (
        Index('ix_books_lowercased_name', func.lower(name), unique=True),
    )
class Books(db.Model):
    __tablename__ = 'Books'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,unique=True)
    content=db.Column(db.String)
    author=db.Column(db.String)
    section_id=db.Column(db.Integer, db.ForeignKey('Section.id'))
    book_sections = db.relationship('BookSection', back_populates='book')
    book_access = db.relationship('BookAccess', back_populates='book')
    @hybrid_property
    def lowercased_name(self):
        return self.name.lower()

    __table_args__ = (
        Index('ix_section_lowercased_name', func.lower(name), unique=True),
    )
class BookSection(db.Model):
    __tablename__ = 'BookSections'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('Books.id'))
    section_id = db.Column(db.Integer, db.ForeignKey('Section.id'))
    section_name=db.Column(db.String)
    section = db.relationship('Section', back_populates='book_sections')
    book = db.relationship('Books', back_populates='book_sections')
    
class BookAccess(db.Model):
    __tablename__ = 'BookAccess'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('Books.id'))
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    issue_date=db.Column(db.String)
    no_of_days=db.Column(db.Integer)
    return_date=db.Column(db.String)
    is_approved=db.Column(db.Integer)
    book = db.relationship('Books', back_populates='book_access')


class History(db.Model):
    __tablename__ = 'History'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('Books.id'))
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    issue_date=db.Column(db.String)
    return_date=db.Column(db.String)
    name=db.Column(db.String)
    author=db.Column(db.String)

class Ratings(db.Model):
    __tablename__='Ratings'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('Books.id'))
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
