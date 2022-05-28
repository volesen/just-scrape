from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Product:
    id: str
    name: str
    description: Optional[str]
    price: float

    @classmethod
    def from_xml(cls, xml):
        return cls(
            id=xml.find("id").text,
            name=xml.find("nm").text,
            description=xml.find("ds").text,
            price=float(xml.find("pc").text),
        )

    def insert_into_db(self, cursor, restaurant_id, category_id):
        cursor.execute(
            """
            INSERT INTO products (
                id,
                name,
                description,
                price,
                restaurant_id,
                category_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO NOTHING;
            """,
            (
                self.id,
                self.name,
                self.description,
                self.price,
                restaurant_id,
                category_id,
            ),
        )


@dataclass
class Category:
    id: str
    name: str
    description: str

    products: List[Product]

    @classmethod
    def from_xml(cls, xml):
        return cls(
            id=xml.find("id").text,
            name=xml.find("nm").text,
            description=xml.find("ds").text,
            products=[Product.from_xml(product) for product in xml.iterfind(".//pr")],
        )

    def insert_into_db(self, cursor, restaurant_id):
        cursor.execute(
            """
            INSERT INTO categories (
                id,
                name,
                description,
                restaurant_id
            )
            VALUES (?, ?, ?, ?) 
            ON CONFLICT(id) DO NOTHING;
            """,
            (self.id, self.name, self.description, restaurant_id),
        )

        for product in self.products:
            product.insert_into_db(cursor, restaurant_id, self.id)


@dataclass
class Restaurant:
    id: str
    name: str
    slogan: Optional[str]

    street: str
    postal_code: str
    city: str

    lat: float
    lng: float

    categories: List[Category]

    @classmethod
    def from_xml(cls, xml):
        return cls(
            id=xml.find("ri").text,
            name=xml.find("nm").text,
            slogan=xml.find("oo/sl").text,
            street=xml.find("ad/st").text,
            postal_code=xml.find("ad/pc").text,
            city=xml.find("ad/tn").text,
            lat=float(xml.find("ad/lt").text),
            lng=float(xml.find("ad/ln").text),
            categories=[
                Category.from_xml(category) for category in xml.iterfind("mc/cs/ct")
            ],
        )

    def insert_into_db(self, cursor):
        cursor.execute(
            """
            INSERT INTO restaurants (
                id,
                name,
                slogan,
                street,
                postal_code,
                city,
                lat,
                lng
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO NOTHING;
            """,
            (
                self.id,
                self.name,
                self.slogan,
                self.street,
                self.postal_code,
                self.city,
                self.lat,
                self.lng,
            ),
        )

        for category in self.categories:
            category.insert_into_db(cursor, self.id)
