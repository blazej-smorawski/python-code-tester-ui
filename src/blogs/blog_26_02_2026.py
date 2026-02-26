from src.blog import display_blog

text="""
### Szanowni Państwo

Zachęcamy do udziału w 16 edycji konkursu programistycznego dla uczniów szkół podstawowych i gimnazjalnych. Zapraszamy do udziału zarówno szkoły publiczne, jak i prywatne.

Pomorski Czarodziej to kolejna odsłona Potyczek z Komputerem - konkursu organizowanego rokrocznie w porozumieniu z Kuratorium Oświaty. Tradycyjnie już, gala finałowa konkursu odbędzie się w siedzibie firmy Intel Technology Poland w Gdańsku, a na laureatów czekają fantastyczne i cenne nagrody.

Konkurs składa się z 3 etapów - szkolnego, rejonowego oraz wojewódzkiego.

Etap Szkolny: 2.03-29.03

Etap Rejonowy: 13.04-26.04

Etap Wojewódzki: 18-22.05


Link do regulaminu : [Regulamin konkursu 📝](./app/static/Pomorski-Czarodziej-2026-Regulamin.pdf)

Zgłoszenia na adres: [pomorski.czarodziej@intel.com](mailto:pomorski.czarodziej@intel.com)
"""

display_blog(text, {})