from SukiScan import app, db
from SukiScan.models import Waifu, Husbando, Other

with app.app_context():
    # Clear existing data if needed
    Waifu.query.delete()
    Husbando.query.delete()
    Other.query.delete()

    waifus = [
        Waifu(w_char_id=1, first_name="Rem", last_name="", hair_colour="Blue", height=154, personality="ISFJ", profession="Maid", body_type="Hourglass"),
        Waifu(w_char_id=2, first_name="Tohru", last_name="", hair_colour="Blonde", height=176, personality="ESFP", profession="Maid", body_type="Inverted Triangle"),
        Waifu(w_char_id=3, first_name="Hinata", last_name="Hyūga", hair_colour="Black", height=163, personality="ISFJ", profession="Ninja", body_type="Hourglass"),
        Waifu(w_char_id=4, first_name="Erza", last_name="Scarlet", hair_colour="Red", height=175, personality="ESTJ", profession="Mage", body_type="Hourglass"),
        Waifu(w_char_id=5, first_name="Zero Two", last_name="", hair_colour="Pink", height=170, personality="ESTP", profession="Parasite", body_type="Hourglass"),
        Waifu(w_char_id=6, first_name="Power", last_name="", hair_colour="Blonde", height=170, personality="ESFP", profession="Public Safety Devil Hunter", body_type="Inverted Triangle"),
        Waifu(w_char_id=7, first_name="Mikasa", last_name="Ackerman", hair_colour="Black", height=170, personality="ISTJ", profession="Soldier", body_type="Inverted Triangle"),
        Waifu(w_char_id=8, first_name="Yoruichi", last_name="Shihouin", hair_colour="Purple", height=156, personality="ESTP", profession="Shinigami", body_type="Hourglass"),
        Waifu(w_char_id=9, first_name="Miyo", last_name="Saimori", hair_colour="Black", height=160, personality="INFP", profession="House Wife", body_type="Hourglass"),
        Waifu(w_char_id=10, first_name="Mitsuri", last_name="Kanroji", hair_colour="Pink", height=164, personality="ESFJ", profession="Demon Slayer", body_type="Hourglass"),
        Waifu(w_char_id=11, first_name="Makima", last_name="", hair_colour="Auburn", height=168, personality="ENFJ", profession="Public Safety Devil Hunter", body_type="Hourglass"),
        Waifu(w_char_id=12, first_name="Fern", last_name="", hair_colour="Purple", height=165, personality="ISTJ", profession="Mage", body_type="Rectangle"),
        Waifu(w_char_id=13, first_name="Frieren", last_name="", hair_colour="Silver", height=160, personality="INTP", profession="Mage", body_type="Rectangle"),
        Waifu(w_char_id=14, first_name="Nami", last_name="", hair_colour="Orange", height=170, personality="ESTJ", profession="Navigator", body_type="Hourglass"),
        Waifu(w_char_id=15, first_name="Yor", last_name="Forger", hair_colour="Black", height=165, personality="ISFJ", profession="Assassin", body_type="Hourglass"),
        Waifu(w_char_id=16, first_name="Chizuru", last_name="Ichinose", hair_colour="Brown", height=158, personality="ESTJ", profession="Girlfriend", body_type="Hourglass"),
        Waifu(w_char_id=17, first_name="Raphtalia", last_name="", hair_colour="Brown", height=150, personality="ISFJ", profession="Sword Fighter", body_type="Hourglass"),
        Waifu(w_char_id=18, first_name="Utahime", last_name="Iori", hair_colour="Black", height=163, personality="ISTJ", profession="Jujutsu Sorcerer", body_type="Hourglass"),
        Waifu(w_char_id=19, first_name="Shoko", last_name="Nishimiya", hair_colour="Brown", height=160, personality="ISFJ", profession="Student", body_type="Hourglass"),
        Waifu(w_char_id=20, first_name="Touka", last_name="Kirishima", hair_colour="Blue", height=162, personality="ISFJ", profession="Waitress", body_type="Hourglass"),
        Waifu(w_char_id=21, first_name="Mai", last_name="Sakurajima", hair_colour="Black", height=162, personality="ISTJ", profession="Student", body_type="Hourglass"),
        Waifu(w_char_id=22, first_name="Asuna", last_name="Yuuki", hair_colour="Brown", height=166, personality="ENFJ", profession="Student", body_type="Hourglass"),
        Waifu(w_char_id=23, first_name="Marin", last_name="Kitagawa", hair_colour="Blonde", height=164, personality="ENFP", profession="Student", body_type="Hourglass"),
        Waifu(w_char_id=24, first_name="Altria", last_name="Pendragon", hair_colour="Blonde", height=154, personality="ISTJ", profession="Saber-class Servant", body_type="Inverted Triangle"),
        Waifu(w_char_id=25, first_name="Kaguya", last_name="Shinomiya", hair_colour="Black", height=158, personality="INTJ", profession="Student Council Vice President", body_type="Rectangle")
    ]

    husbandos = [
        Husbando(h_char_id=1, first_name="Satoru", last_name="Gojo", hair_colour="White", height=190, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=2, first_name="Kento", last_name="Nanami", hair_colour="Blonde", height=184, personality="ISTJ", profession="Jujutsu Sorcerer", body_type="Rectangle"),
        Husbando(h_char_id=3, first_name="Suguru", last_name="Geto", hair_colour="Black", height=185, personality="ENTP", profession="Jujutsu Sorcerer", body_type="Inverted Triangle"),
        Husbando(h_char_id=4, first_name="Levi", last_name="Ackerman", hair_colour="Black", height=160, personality="ISTJ", profession="Captain", body_type="Rectangle"),
        Husbando(h_char_id=5, first_name="Eren", last_name="Yeager", hair_colour="Brown", height=183, personality="INFJ", profession="Attack Titan", body_type="Inverted Triangle"),
        Husbando(h_char_id=6, first_name="Armin", last_name="Arlert", hair_colour="Blonde", height=190, personality="INFP", profession="Colossal Titan", body_type="Rectangle"),
        Husbando(h_char_id=7, first_name="Loid", last_name="Forger", hair_colour="Blonde", height=187, personality="ENTJ", profession="Spy", body_type="Inverted Triangle"),
        Husbando(h_char_id=8, first_name="Naruto", last_name="Uzamaki", hair_colour="Blonde", height=180, personality="ENFP", profession="Hokage", body_type="Inverted Triangle"),
        Husbando(h_char_id=9, first_name="Sasuke", last_name="Uchiha", hair_colour="Black", height=182, personality="INTJ", profession="Hokage Right Hand", body_type="Inverted Triangle"),
        Husbando(h_char_id=10, first_name="Kakashi", last_name="Hataka", hair_colour="Silver", height=181, personality="INFP", profession="Shinobi", body_type="Rectangle"),
        Husbando(h_char_id=11, first_name="Jinshi", last_name="Shen", hair_colour="Purple", height=180, personality="INTJ", profession="Royalty", body_type="Inverted Triangle"),
        Husbando(h_char_id=12, first_name="Toji", last_name="Fushiguro", hair_colour="Black", height=187, personality="ISTP", profession="Assessin", body_type="Inverted Triangle"),
        Husbando(h_char_id=13, first_name="Kazuto", last_name="Kirigaya", hair_colour="Black", height=173, personality="INTJ", profession="Black Swordswan", body_type="Rectangle"),
        Husbando(h_char_id=14, first_name="Anos", last_name="Voldigoad", hair_colour="Black", height=178, personality="ENTP", profession="Demon King", body_type="Inverted Triangle"),
        Husbando(h_char_id=15, first_name="Escanor", last_name="", hair_colour="Blonde", height=270, personality="ESTP", profession="The Lion Sin of Pride", body_type="Inverted Triangle"),
        Husbando(h_char_id=16, first_name="Ban", last_name="", hair_colour="White", height=177, personality="ESFP", profession="The Fox Sin of Greed", body_type="Hourglass"),
        Husbando(h_char_id=17, first_name="Meliodas", last_name="", hair_colour="Blonde", height=152, personality="ENFP", profession="The Dragon Sin of Wrath", body_type="Rectangle"),
        Husbando(h_char_id=18, first_name="Gilgamesh", last_name="", hair_colour="Blonde", height=182, personality="ENTJ", profession="King", body_type="Inverted Triangle"),
        Husbando(h_char_id=19, first_name="Cu", last_name="Chulainn", hair_colour="Blue", height=185, personality="ESTP", profession="Lancer", body_type="Inverted Triangle"),
        Husbando(h_char_id=20, first_name="Shirou", last_name="Emiya", hair_colour="White", height=187, personality="INFJ", profession="Archer", body_type="Inverted Triangle"),
        Husbando(h_char_id=21, first_name="Cid", last_name="Kagenou", hair_colour="Black", height=175, personality="INTJ", profession="Eminence in Shadow", body_type="Inverted Triangle"),
        Husbando(h_char_id=22, first_name="Ichigo", last_name="Kurosaki", hair_colour="Orange", height=181, personality="ISFP", profession="Substitute Shinigami", body_type="Inverted Triangle"),
        Husbando(h_char_id=23, first_name="Byakuya", last_name="Kuchiki", hair_colour="Black", height=180, personality="ISFP", profession="Captain", body_type="Rectangle"),
        Husbando(h_char_id=24, first_name="Howl", last_name="Pendragon", hair_colour="Blonde", height=185, personality="ENFP", profession="Wizard", body_type="Hourglass"),
        Husbando(h_char_id=25, first_name="Jin-Woo", last_name="Sung", hair_colour="Black", height=178, personality="ISFJ", profession="Shadow Monarch", body_type="Inverted Triangle")
    ]

    others = [
        Other(o_char_id=1, first_name="Rimuru", last_name="Tempest", hair_colour="Blue", height=150, personality="ENTP", profession="Slime", body_type="Oval"),
        Other(o_char_id=2, first_name="Felix", last_name="Argyle", hair_colour="Blonde", height=160, personality="ENFJ", profession="Healer", body_type="Hourglass"),
        Other(o_char_id=3, first_name="Astolfo", last_name="", hair_colour="Pink", height=155, personality="ESFP", profession="Rider", body_type="Hourglass"),
        Other(o_char_id=4, first_name="Haku", last_name="", hair_colour="Black", height=160, personality="ISFJ", profession="Shinobi", body_type="Hourglass"),
        Other(o_char_id=5, first_name="Appa", last_name="", hair_colour="White", height=400, personality="ISFP", profession="Sky Bison", body_type="Oval"),
        Other(o_char_id=6, first_name="Totoro", last_name="", hair_colour="Gray", height=200, personality="ENFP", profession="Forest Spirit", body_type="Oval"),
        Other(o_char_id=7, first_name="Pikachu", last_name="", hair_colour="Yellow", height=40, personality="ESFP", profession="Companion", body_type="Rectangle"),
        Other(o_char_id=8, first_name="Meowth", last_name="", hair_colour="Cream", height=43, personality="ENTP", profession="Thief", body_type="Diamond"),
        Other(o_char_id=9, first_name="Luna", last_name="", hair_colour="Black", height=35, personality="INFJ", profession="Guide", body_type="Diamond"),
        Other(o_char_id=10, first_name="Arcanine", last_name="", hair_colour="Orange", height=190, personality="ISFJ", profession="Guardian", body_type="Inverted Triangle"),
        Other(o_char_id=11, first_name="Mokona", last_name="", hair_colour="White", height=30, personality="ENFP", profession="Messenger", body_type="Oval"),
        Other(o_char_id=12, first_name="Chopper", last_name="", hair_colour="Brown", height=90, personality="INFP", profession="Doctor", body_type="Oval"),
        Other(o_char_id=13, first_name="Happy", last_name="", hair_colour="Blue", height=40, personality="ENFP", profession="Support", body_type="Rectangle"),
        Other(o_char_id=14, first_name="Jiji", last_name="", hair_colour="Black", height=30, personality="ISTP", profession="Companion", body_type="Rectangle"),
        Other(o_char_id=15, first_name="Moogle", last_name="", hair_colour="White", height=50, personality="INTP", profession="Guide", body_type="Oval"),
        Other(o_char_id=16, first_name="Koromon", last_name="", hair_colour="Pink", height=20, personality="ESTJ", profession="Baby Digimon", body_type="Oval"),
        Other(o_char_id=17, first_name="Calcifer", last_name="", hair_colour="Flame", height=10, personality="ENTP", profession="Fire Demon", body_type="Diamond"),
        Other(o_char_id=18, first_name="Lotor", last_name="Beast Form", hair_colour="Purple", height=180, personality="INTJ", profession="General", body_type="Inverted Triangle"),
        Other(o_char_id=19, first_name="Kirara", last_name="", hair_colour="Cream", height=35, personality="ESFJ", profession="Companion", body_type="Hourglass"),
        Other(o_char_id=20, first_name="BMO", last_name="", hair_colour="Teal", height=50, personality="ENFP", profession="Game Console", body_type="Rectangle"),
        Other(o_char_id=21, first_name="Muffin", last_name="", hair_colour="Blue", height=25, personality="ISFP", profession="Toddler", body_type="Rectangle"),
        Other(o_char_id=22, first_name="Plankton", last_name="", hair_colour="Green", height=10, personality="ENTJ", profession="Business Owner", body_type="Rectangle"),
        Other(o_char_id=23, first_name="Snorlax", last_name="", hair_colour="Blue", height=210, personality="ISFP", profession="Sleeper", body_type="Oval"),
        Other(o_char_id=24, first_name="Onion", last_name="", hair_colour="White", height=60, personality="??", profession="??", body_type="Oval"),
        Other(o_char_id=25, first_name="Shenron", last_name="", hair_colour="Green", height=2000, personality="INTJ", profession="Dragon God", body_type="Diamond"),
    ]


    db.session.add_all(waifus + husbandos + others)
    db.session.commit()
    print("Database seeded with characters.")
