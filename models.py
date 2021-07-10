from app import db



class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link =  db.Column(db.String(120)) ## i added this Column as in the colomn
    seeking_description = db.Column(db.String(200)) ## i added this Column as in the colomn
    genres = db.Column(db.ARRAY(db.String), nullable=False)  ## i update type of the  Column based on the reviwer recomedndation.
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'),nullable=True)
    seeking_talent = db.Column(db.Boolean, default=False , server_default="false")
    deleted = db.Column(db.Boolean, default=False)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate - done
              ## I have did that by adding the missing fields as Columns in the spefied tables
    def __repr__(self):
        return f'< ID: {self.id}, name: {self.name}, state: {self.state}, address: {self.address}, phone: {self.phone}, image_link: {self.image_link}, facebook_link: {self.facebook_link}, facebook_link: {self.facebook_link}, website_link: {self.website_link}, seeking_description: {self.seeking_description}, genres: {self.genres}, show_id: {self.show_id}, seeking_talent: {self.seeking_talent}, deleted: {self.deleted}>'


class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)  ## i update type of the  Column based on the reviwer recomedndation.
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link =  db.Column(db.String(120)) ## i added this Column as in the colomn
    seeking_description = db.Column(db.String(200)) ## i added this Column as in the colomn
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'),nullable=True)
    seeking_venue = db.Column(db.Boolean, default=False , server_default="false") # this is for the check box in the create_venue page

    def __repr__(self):
        return f'< ID: {self.id}, name: {self.name}, state: {self.state}, phone: {self.phone},  genres: {self.genres}, image_link: {self.image_link}, facebook_link: {self.facebook_link}, facebook_link: {self.facebook_link}, website_link: {self.website_link}, seeking_description: {self.seeking_description}, genres: {self.genres}, show_id: {self.show_id}, seeking_venue: {self.seeking_venue}>'


## here i will defind the show model
class Show(db.Model):
    __tablename__ = "shows"
    id = db.Column(db.Integer, primary_key=True)
    start_time= db.Column(db.DateTime(timezone=True))
    Artists_id = db.relationship('Artist', backref='shows_id', lazy=True)
    Venues_id= db.relationship('Venue', backref='shows_id', lazy=True)
    def __repr__(self):
       return f'< ID: {self.id}, start_time: {self.start_time}>'
