from db import  db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy = 'dynamic')            # lazy = 'dynamic' mean: Do not create item model for every item in store. Create it once for a store

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'stores': [item.json() for item in self.items.all()]}             # We use .all() query builder because we use dynamic loading relationships

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()                # SELECT * FROM ITEMS WHERE name=name LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

