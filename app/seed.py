from .extensions import db
from .models import Movie

MOVIES = [
    ('Interestelar','Ficção Científica',2014,'Christopher Nolan','https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg','Astronautas viajam por um buraco de minhoca em busca de um novo lar para a humanidade.',8.90,34.90),
    ('A Origem','Ação / Ficção Científica',2010,'Christopher Nolan','https://image.tmdb.org/t/p/w500/9e3Dz7aCANy5aRUQF745IlNloJ1.jpg','Um ladrão que invade sonhos recebe uma missão quase impossível.',7.90,29.90),
    ('Cidade de Deus','Drama / Crime',2002,'Fernando Meirelles','https://image.tmdb.org/t/p/w500/k7eYdWvhYQyRQoU2TB2A2Xu2TfD.jpg','A trajetória de jovens envolvidos com o crime em uma comunidade do Rio de Janeiro.',6.90,24.90),
    ('O Senhor dos Anéis: A Sociedade do Anel','Fantasia / Aventura',2001,'Peter Jackson','https://image.tmdb.org/t/p/w500/omoMXT3Z7XrQwRZ2OGJGNWbdeEl.jpg','Um hobbit recebe a missão de destruir um anel poderoso.',8.90,39.90),
    ('Vingadores: Ultimato','Ação / Super-herói',2019,'Anthony e Joe Russo','https://image.tmdb.org/t/p/w500/q6725aR8Zs4IwGMXzZT8aC8lh41.jpg','Heróis sobreviventes tentam reverter os danos causados por Thanos.',9.90,44.90),
    ('Divertida Mente','Animação / Família',2015,'Pete Docter','https://image.tmdb.org/t/p/w500/62SAZfLfzhxJWUFJvfIPMw6QUpE.jpg','As emoções de uma garota lidam com grandes mudanças.',7.90,29.90),
    ('Coringa','Drama / Suspense',2019,'Todd Phillips','https://image.tmdb.org/t/p/w500/xLxgVxFWvb9hhUyCDDXxRPPnFck.jpg','A origem dramática de Arthur Fleck e sua transformação.',7.90,29.90),
    ('Matrix','Ficção Científica / Ação',1999,'Lana e Lilly Wachowski','https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg','Um programador descobre que a realidade é uma simulação.',6.90,24.90),
    ('Toy Story','Animação / Aventura',1995,'John Lasseter','https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg','Brinquedos ganham vida quando humanos não estão por perto.',6.90,24.90),
    ('Pantera Negra','Ação / Super-herói',2018,'Ryan Coogler','https://image.tmdb.org/t/p/w500/uxzzxijgPIY7slzFvMotPv8wjKA.jpg','TChalla retorna a Wakanda para assumir o trono.',8.90,34.90),
    ('Oppenheimer','Drama / Biografia',2023,'Christopher Nolan','https://image.tmdb.org/t/p/w500/ptpr0kGAckfQkJeJIt8st5dglvd.jpg','A história do físico J. Robert Oppenheimer.',10.90,49.90),
    ('Barbie','Comédia / Aventura',2023,'Greta Gerwig','https://image.tmdb.org/t/p/w500/yRRuLt7sMBEQkHsd1S3KaaofZn7.jpg','Barbie deixa seu mundo perfeito e vai ao mundo real.',9.90,39.90),
    ('Duna','Ficção Científica / Aventura',2021,'Denis Villeneuve','https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg','Paul Atreides enfrenta intrigas políticas e protege seu povo.',8.90,34.90),
    ('Duna: Parte Dois','Ficção Científica / Aventura',2024,'Denis Villeneuve','https://image.tmdb.org/t/p/w500/8b8R8l88Qje9dn9OE8PY05Nxl1X.jpg','Paul une forças com Chani e os Fremen.',11.90,54.90),
    ('Homem-Aranha: Através do Aranhaverso','Animação / Super-herói',2023,'Joaquim Dos Santos','https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg','Miles Morales encontra novos Homens-Aranha.',9.90,39.90),
    ('John Wick 4','Ação / Suspense',2023,'Chad Stahelski','https://image.tmdb.org/t/p/w500/gh2bmprLtUQ8oXCSluzfqaicyrm.jpg','John Wick enfrenta novos inimigos em busca de liberdade.',9.90,39.90),
    ('Avatar: O Caminho da Água','Ficção Científica / Aventura',2022,'James Cameron','https://image.tmdb.org/t/p/w500/mbYQLLluS651W89jO7MOZcLSCUw.jpg','Jake Sully e sua família exploram novas regiões de Pandora.',8.90,34.90),
    ('Top Gun: Maverick','Ação / Drama',2022,'Joseph Kosinski','https://image.tmdb.org/t/p/w500/62HCnUTziyWcpDaBO2i1DX17ljH.jpg','Maverick retorna para treinar uma nova geração de pilotos.',8.90,34.90),
    ('Parasita','Suspense / Drama',2019,'Bong Joon-ho','https://image.tmdb.org/t/p/w500/igw938inb6Fy0YVcwIyxQ7Lu5FO.jpg','Uma família pobre se infiltra na vida de uma família rica.',7.90,29.90),
    ('Whiplash','Drama / Música',2014,'Damien Chazelle','https://image.tmdb.org/t/p/w500/7fn624j5lj3xTme2SgiLCeuedmO.jpg','Um jovem baterista enfrenta métodos extremos para alcançar excelência.',6.90,24.90),
    ('Batman: O Cavaleiro das Trevas','Ação / Crime',2008,'Christopher Nolan','https://image.tmdb.org/t/p/w500/iGZX91hIqM9Uu0KGhd4MUaJ0Rtm.jpg','Batman enfrenta o Coringa pelo destino de Gotham.',7.90,29.90),
    ('Gladiador','Ação / Drama',2000,'Ridley Scott','https://image.tmdb.org/t/p/w500/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg','Um general romano busca vingança após perder família e honra.',6.90,24.90),
    ('Titanic','Romance / Drama',1997,'James Cameron','https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg','Um romance nasce durante a viagem do famoso navio Titanic.',6.90,24.90),
    ('Super Mario Bros. O Filme','Animação / Aventura',2023,'Aaron Horvath e Michael Jelenic','https://image.tmdb.org/t/p/w500/ktU3MIeZtuEVRlMftgp0HMX2WR7.jpg','Mario e Luigi entram em uma aventura pelo Reino dos Cogumelos.',8.90,34.90),
]

def seed_movies():
    for title, genre, year, director, poster, desc, rent, buy in MOVIES:
        movie = Movie.query.filter_by(title=title).first()
        if not movie:
            movie = Movie(title=title)
            db.session.add(movie)
        movie.genre = genre
        movie.year = year
        movie.director = director
        movie.poster_url = poster
        movie.description = desc
        movie.rent_price = rent
        movie.buy_price = buy
    db.session.commit()
