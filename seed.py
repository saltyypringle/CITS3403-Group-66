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
        Husbando(h_char_id=4, first_name="Levi", last_name="Ackerman", hair_colour="Black", height=160, personality="ISTJ", profession="Captain", body_type="Inverted Triangle"),
        Husbando(h_char_id=5, first_name="Eren", last_name="Yeager", hair_colour="Brown", height=183, personality="INFJ", profession="Attack Titan", body_type="Inverted Triangle"),
        Husbando(h_char_id=6, first_name="Armin", last_name="Arlert", hair_colour="Blonde", height=190, personality="INFP", profession="Colossal Titan", body_type="Inverted Triangle"),
        Husbando(h_char_id=7, first_name="Loid", last_name="Forger", hair_colour="Blonde", height=187, personality="ENTJ", profession="Spy", body_type="Inverted Triangle"),
        Husbando(h_char_id=8, first_name="Naruto", last_name="Uzamaki", hair_colour="Blonde", height=180, personality="ENFP", profession="Hokage", body_type="Inverted Triangle"),
        Husbando(h_char_id=9, first_name="Sasuke", last_name="Uchiha", hair_colour="Black", height=182, personality="INTJ", profession="Hokage Right Hand", body_type="Inverted Triangle"),
        Husbando(h_char_id=10, first_name="Kakashi", last_name="Hataka", hair_colour="Silver", height=181, personality="INFP", profession="Shinobi", body_type="Inverted Triangle"),
        Husbando(h_char_id=11, first_name="Jinshi", last_name="Shen", hair_colour="Purple", height=180, personality="INTJ", profession="Royalty", body_type="Inverted Triangle"),
        Husbando(h_char_id=12, first_name="Toji", last_name="Fushiguro", hair_colour="Black", height=187, personality="ISTP", profession="Assessin", body_type="Inverted Triangle"),
        Husbando(h_char_id=13, first_name="Kazuto", last_name="Kirigaya", hair_colour="Black", height=173, personality="INTJ", profession="Black Swordswan", body_type="Inverted Triangle"),
        Husbando(h_char_id=14, first_name="Anos", last_name="Voldigoad", hair_colour="Black", height=178, personality="ENTP", profession="Demon King", body_type="Inverted Triangle"),
        Husbando(h_char_id=15, first_name="Escanor", last_name="", hair_colour="Blonde", height=270, personality="ESTP", profession="The Lion Sin of Pride", body_type="Inverted Triangle"),
        Husbando(h_char_id=16, first_name="Ban", last_name="", hair_colour="White", height=177, personality="ESFP", profession="The Fox Sin of Greed", body_type="Inverted Triangle"),
        Husbando(h_char_id=17, first_name="Meliodas", last_name="", hair_colour="Blonde", height=152, personality="ENFP", profession="The Dragon Sin of Wrath", body_type="Inverted Triangle"),
        Husbando(h_char_id=18, first_name="Gilgamesh", last_name="", hair_colour="Blonde", height=182, personality="ENTJ", profession="King", body_type="Inverted Triangle"),
        Husbando(h_char_id=19, first_name="Cu", last_name="Chulainn", hair_colour="Blue", height=185, personality="ESTP", profession="Lancer", body_type="Inverted Triangle"),
        Husbando(h_char_id=20, first_name="Shirou", last_name="Emiya", hair_colour="White", height=187, personality="INFJ", profession="Archer", body_type="Inverted Triangle"),
        Husbando(h_char_id=21, first_name="Cid", last_name="Kagenou", hair_colour="Black", height=175, personality="INTJ", profession="Eminence in Shadow", body_type="Inverted Triangle"),
        Husbando(h_char_id=22, first_name="Ichigo", last_name="Kurosaki", hair_colour="Orange", height=181, personality="ISFP", profession="Substitute Shinigami", body_type="Inverted Triangle"),
        Husbando(h_char_id=23, first_name="Byakuya", last_name="Kuchiki", hair_colour="Black", height=180, personality="ISFP", profession="Captain", body_type="Inverted Triangle"),
        Husbando(h_char_id=24, first_name="Howl", last_name="Pendragon", hair_colour="Blonde", height=185, personality="ENFP", profession="Wizard", body_type="Inverted Triangle"),
        Husbando(h_char_id=25, first_name="Jin-Woo", last_name="Sung", hair_colour="Black", height=178, personality="ISFJ", profession="Shadow Monarch", body_type="Inverted Triangle"),
    ]

    others = [
        Other(o_char_id=1, first_name="Totoro", last_name="", hair_colour="Grey", height=210, personality="CUTE", profession="Forest Spirit", body_type="Round"),
    ]

    db.session.add_all(waifus + husbandos + others)
    db.session.commit()
    print("Database seeded with characters.")
