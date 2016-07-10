# coding: utf-8

from datetime import datetime, timedelta
from flask import Flask
from flask import session, request
from flask import render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import gen_salt
from flask_oauthlib.provider import OAuth2Provider


app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'secret'
app.config.update({
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///db.sqlite',
})
db = SQLAlchemy(app)
oauth = OAuth2Provider(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)


class Client(db.Model):
    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), nullable=False)

    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User')

    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    @property
    def client_type(self):
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


class Grant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')

    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    code = db.Column(db.String(255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id')
    )
    user = db.relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

# main db app model
class Category(db.Model):
    __tablename__ = 'category'
    name = db.Column(db.String(256))
    description = db.Column(db.String(256))
    slug = db.Column(db.String(256))
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

class Profile(db.Model):
    __tablename__ = 'profile'
    email =db.Column(db.String(256))
    username = db.Column(db.String(256))
    password = db.Column(db.String(256))
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

class Video(db.Model):
    __tablename__ = 'video'
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    bucket = db.Column(db.String(256))
    filename = db.Column(db.String(256))
    embed = db.Column(db.String(256))
    source_id = db.Column(db.String(256))
    duration = db.Column(db.String(256))
    length = db.Column(db.String(256))
    thumb = db.Column(db.String(256))
    type = db.Column(db.Integer)
    from_source = db.Column(db.String(256))
    logo_source = db.Column(db.String(256))
    name_source = db.Column(db.String(256))
    ext = db.Column(db.String(256))
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

class Photo(db.Model):
    __tablename__ = 'photo'
    title = db.Column(db.Text,nullable=True)
    description = db.Column(db.Text,nullable=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    bucket = db.Column(db.String(256), nullable=True)
    filename = db.Column(db.String(256), nullable=True)
    version = db.Column(db.String(256), nullable=True)
    path =db.Column(db.String(256), nullable=True)
    url = db.Column(db.String(256), nullable=True)
    ext = db.Column(db.String(256), nullable=True)
    type = db.Column(db.Integer)
    from_source = db.Column(db.String(256), nullable=True)
    logo_source = db.Column(db.String(256), nullable=True)
    name_source = db.Column(db.String(256), nullable=True)
    url_source = db.Column(db.String(256), nullable=True)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

class News(db.Model):
    __tablename__ = 'news'
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    summary = db.Column(db.Text)
    url = db.Column(db.String(256))
    body = db.Column(db.Text)
    thumb = db.Column(db.String(256))
    bucket = db.Column(db.String(256))
    photos = models.ForeignKey(Photo)
    author = models.OneToOneField(Profile)

    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User')


    from_source = db.Column(db.String(256))
    logo_source = db.Column(db.String(256))
    name_source = db.Column(db.String(256))
    url_source = db.Column(db.String(256))
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)


class Tag(db.Model):
    __tablename__ = 'tag'
    name = db.Column(db.String(256))
    slug = db.Column(db.String(256))
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)


class Feed(db.Model):
    __tablename__ = 'feed'
    category = models.ForeignKey(Category)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    url = db.Column(db.String(256))
    content = models.CharField(max_length=1024, null=True)
    from_source = db.Column(db.String(256))
    logo_source = db.Column(db.String(256))
    name_source = db.Column(db.String(256))
    url_source = db.Column(db.String(256))
    type = db.Column(db.Integer)
    owner = models.ForeignKey(Profile,null=True)
    bucket = db.Column(db.String(256), nullable=True)
    thumb = db.Column(db.Text)
    likes = db.Column(db.Integer)
    shares = db.Column(db.Integer)
    pins = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    pins = db.Column(db.Integer)
    views = db.Column(db.Integer)
    popular = db.Column(db.Integer)
    tags = models.ManyToManyField(Tag)
    status = db.Column(db.Integer)
    video = models.OneToOneField(Video, on_delete=models.CASCADE,null=True)
    images = models.ManyToManyField(Photo, related_name='images',null=True)
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE,null=True)
    news = models.OneToOneField(News, on_delete=models.CASCADE,null=True)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)


class Input(db.Model):
    __tablename__ = 'input'
    logo = db.Column(db.String(256))
    name = db.Column(db.String(256))
    url = db.Column(db.Text)
    channel_id = db.Column(db.String(256))
    olikes = db.Column(db.Integer)
    ofollows = db.Column(db.Integer)
    osubcribles = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    follows = db.Column(db.Integer)
    subribles = db.Column(db.Integer)
    tags = models.ForeignKey(Tag)
    categories = models.ForeignKey(Category)
    from_source = db.Column(db.String(256))
    logo_source = db.Column(db.String(256))
    name_source = db.Column(db.String(256))
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

class Activity(db.Model):
    __tablename__ = 'activity'
    user = models.ForeignKey(Profile, related_name='user')
    following = models.ForeignKey(Profile, related_name='following')
    feed = models.ForeignKey(Feed)
    action = db.Column(db.Text)
    action_type = db.Column(db.Integer)
    content = models.CharField(max_length=1024, null = True)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)


class Comment(db.Model):
    __tablename__ = 'comment'
    feed = models.ForeignKey(Feed)
    user = models.ForeignKey(Profile)
    content = models.CharField(max_length=1024, null = True)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)


class Notification(db.Model):
    __tablename__ = 'notification'
    message = db.Column(db.Text)
    activity = models.ForeignKey(Activity)
    to = models.ForeignKey(Profile)
    status = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

# end maindb app model


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


@app.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        session['id'] = user.id
        return redirect('/')
    user = current_user()
    return render_template('home.html', user=user)


@app.route('/client')
def client():
    user = current_user()
    if not user:
        return redirect('/')
    item = Client(
        client_id=gen_salt(40),
        client_secret=gen_salt(50),
        _redirect_uris=' '.join([
            'http://localhost:8000/authorized',
            'http://127.0.0.1:8000/authorized',
            'http://127.0.1:8000/authorized',
            'http://127.1:8000/authorized',
            ]),
        _default_scopes='email',
        user_id=user.id,
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(
        client_id=item.client_id,
        client_secret=item.client_secret,
    )


@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=current_user(),
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(
        client_id=request.client.client_id,
        user_id=request.user.id
    )
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.pop('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(tok)
    db.session.commit()
    return tok


@app.route('/oauth/token', methods=['GET', 'POST'])
@oauth.token_handler
def access_token():
    return None


@app.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    user = current_user()
    if not user:
        return redirect('/')
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        kwargs['user'] = user
        return render_template('authorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'


@app.route('/api/me')
@oauth.require_oauth()
def me():
    user = request.oauth.user
    return jsonify(username=user.username)


if __name__ == '__main__':
    db.create_all()
    app.run()
