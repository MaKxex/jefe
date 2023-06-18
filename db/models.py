from sqlalchemy import Boolean, Sequence, Text, Integer, REAL, String, BigInteger
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Embroidery(Base):
    __tablename__ = "embroidery"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    height = Column(REAL)
    width = Column(REAL)
    photo_link = Column(Text)
    rel_path = Column(Text)


    def __repr__(self):
        return f"<Embroidery(id={self.id}, name={self.name}, height={self.height}, width={self.width}, photo_link={self.photo_link}, rel_path={self.rel_path})>"

    def row_in_array(self):
        return f"{self.name}\n/{self.__tablename__}{self.id}\n"
    
    def get_page(self):
        return self.name, self.height, self.width, self.photo_link

    def get_threadList(self):
        pass

    # def get_short_command(self):
    #     return f"/emb_{self.id}"
    
class Catalog(Base):
    __tablename__ = "catalog"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    
    def __repr__(self):
        return f"<Catalog(id={self.id}, name={self.name})>"


class Color(Base):
    __tablename__ = "color"
    id = Column(Integer, primary_key=True)
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    name = Column(String)
    count = Column(Integer)

    def __repr__(self):
        return f"<Color(id={self.id}, catalog_id={self.catalog_id}, name={self.name})>"
    
    def row_in_array(self):
        return f"{self.id} {self.name}: {0 if self.count == None else self.count}\n"



class Thread(Base):
    __tablename__ = "thread"
    color_id = Column(Integer, ForeignKey('color.id'))
    embroidery_id = Column(Integer, ForeignKey('embroidery.id'), primary_key=True)
    index = Column(Integer, primary_key=True)
    length = Column(REAL)

    def __repr__(self):
        return f"<Thread(color_id={self.color_id}, embroidery_id={self.embroidery_id}, length={self.length})>"
    

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"
    

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(REAL)
    description = Column(Text)

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, description={self.description})>"
    
    def get_short_command(self):
        return f"/product_{self.id}"


class Category_Product(Base):
    __tablename__ = "category_product"
    category_id = Column(Integer, ForeignKey('category.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    embroidery_id = Column(Integer, ForeignKey('embroidery.id'))

    def __repr__(self):
        return f"<CategoryProduct(category_id={self.category_id}, product_id={self.product_id}, embroidery_id={self.embroidery_id})>"

class Buttons(Base):
    __tablename__ = "buttons"
    id = Column(Integer, primary_key=True)
    sub = Column(String)
    link_to = Column(String)
    f_name = Column(String)
    args = Column(String)
    show_on = Column(String)
    pr = (Integer)



if __name__ == "__main__":

    print(globals())