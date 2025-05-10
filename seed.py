# seed.py

from SukiScan import app, db
from SukiScan.models import Waifu, Husbando, Other

with app.app_context():
    # Clear existing data if needed
    Waifu.query.delete()
    Husbando.query.delete()
    Other.query.delete()

    # Add your entries (adjust fields as per your models)
    waifus = [
        Waifu(w_char_id=1, first_name="Asuka", last_name="Langley", hair_colour="Red", personality="TSUN", profession="Pilot", body_type="Slim"),
        Waifu(w_char_id=2, first_name="Rei", last_name="Ayanami", hair_colour="Blue", personality="SHY", profession="Pilot", body_type="Slim"),
    ]

    husbandos = [
        Husbando(h_char_id=1, first_name="Levi", last_name="Ackerman", hair_colour="Black", personality="COOL", profession="Captain", body_type="Fit"),
    ]

    others = [
        Other(o_char_id=1, first_name="Totoro", last_name="", hair_colour="Grey", personality="CUTE", profession="Forest Spirit", body_type="Round"),
    ]

    db.session.add_all(waifus + husbandos + others)
    db.session.commit()
    print("Database seeded with characters.")
