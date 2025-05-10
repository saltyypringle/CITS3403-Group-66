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
        Waifu(w_char_id=1, first_name="Asuka", last_name="Langley", hair_colour="Red", height=157, personality="TSUN", profession="Pilot", body_type="Slim"),
        Waifu(w_char_id=2, first_name="Rei", last_name="Ayanami", hair_colour="Blue", height=149, personality="SHY", profession="Pilot", body_type="Slim"),
    ]

    husbandos = [
        Husbando(h_char_id=1, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=2, first_name="Kento", last_name="Nanami", hair_colour="Blonde", height=184, personality="ISTJ", profession="Jujutsu Sorcerer", body_type="Rectangle"),
        Husbando(h_char_id=3, first_name="Suguru", last_name="Geto", hair_colour="Black", height=185, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=4, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=5, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=6, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=7, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=8, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=9, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=10, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=11, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=12, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=13, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=14, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=15, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=16, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=17, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=18, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=19, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=20, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=21, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=22, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=23, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=24, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=25, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=26, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
    ]

    others = [
        Other(o_char_id=1, first_name="Totoro", last_name="", hair_colour="Grey", height=210, personality="CUTE", profession="Forest Spirit", body_type="Round"),
    ]

    db.session.add_all(waifus + husbandos + others)
    db.session.commit()
    print("Database seeded with characters.")
