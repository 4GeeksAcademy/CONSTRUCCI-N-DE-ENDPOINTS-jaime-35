from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

db = SQLAlchemy()
class Favorite_types(Enum):
    planet =1
    people = 2

class User(db.Model):
    _tablename_ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    #first_name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    #last_name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    #password: Mapped[str] = mapped_column(nullable=False)
   
    favorites:Mapped[list["Favorite"]] = relationship(back_populates="user")  
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
            # do not serialize the password, its a security breach
        }
class People (db.Model):
    _tablename_ ="people"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(120),nullable=False)
    favorites:Mapped[list["Favorite"]] = relationship(back_populates="people")    
    #user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    #user: Mapped[User] = relationship(back_populates="people")
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "favoriteCount": len(self.favorites)
        }

    def serialize(self):
        favorites = list(map(lambda f:f.serialize(),self.favorites))
        return{
            "id":self.id,
            "name":self.name,
            "favoriteCount" : len(self.favorites),
            #"favoriteUsers": favorites.user
        }

class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="planet")
   

    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "favoriteCount": len(self.favorites)

        }

class Favorite(db.Model):
    __tablename__ = "favorites" 
    id: Mapped[int] = mapped_column(primary_key=True)  
    type: Mapped[Favorite_types]= mapped_column(SQLAlchemyEnum(Favorite_types))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"),nullable=False)
    planet: Mapped[Planet] = relationship(back_populates="favorites")
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=True)
    people : Mapped[People] = relationship(back_populates="favorites")
    user: Mapped[User] = relationship(back_populates="favorites")

    def serialize(self):
        
        favorite_item=None
        Favorite_types=""
        if self.type == Favorite_types.people :
            
            Favorite_types="people"
            favorite_item = self.people.serialize()
        elif self.type == Favorite_types.planet:
            
            Favorite_types="planet"
            favorite_item = self.planet. serialize()
        
        return{
            "id": self.id,
            "type": Favorite_types,
            
            "favoriteItem": favorite_item
        }
    

