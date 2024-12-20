from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CryptoCoin(db.Model):
    __tablename__ = "crypto_coin"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    crypto_name = db.Column(db.String(5), unique=True, nullable=False)

class CryptoEntries(db.Model):
    __tablename__ = "crypto_entries"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(10), nullable=False)  
    time = db.Column(db.String(15), nullable=False)  
    from_currency = db.Column(db.String(5), db.ForeignKey('crypto_coin.crypto_name'), nullable=False)
    from_quantity = db.Column(db.Float, nullable=False)
    to_currency = db.Column(db.String(5), db.ForeignKey('crypto_coin.crypto_name'), nullable=False)
    to_quantity = db.Column(db.Float, nullable=False)

class CurrentStatus(db.Model):
    __tablename__ = "current_status"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    btc =db.Column(db.Float)
    eth =db.Column(db.Float)
    usdt =db.Column(db.Float)
    ada =db.Column(db.Float)
    sol =db.Column(db.Float)
    xrp =db.Column(db.Float)
    dot =db.Column(db.Float)
    doge =db.Column(db.Float)
    shib =db.Column(db.Float)

    def to_dict(self):
        return {
            'btc': self.btc,
            'eth': self.eth,
            'usdt': self.usdt,
            'ada': self.ada,
            'sol': self.sol,
            'xrp': self.xrp,
            'dot': self.dot,
            'doge': self.doge,
            'shib': self.shib}



