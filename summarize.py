from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

summarizer = LexRankSummarizer()

text = '''Esports, short for electronic sports, is a form of competition using video games.[1] Esports often takes the form of organized, multiplayer video game competitions, particularly between professional players, individually or as teams. Although organized competitions have long been a part of video game culture, these were largely between amateurs until the late 2000s, when participation by professional gamers and spectatorship in these events through live streaming saw a large surge in popularity.[2][3] By the 2010s, esports was a significant factor in the video game industry, with many game developers actively designing and providing funding for tournaments and other events.

The most common video game genres associated with esports are multiplayer online battle arena (MOBA), first-person shooter (FPS), fighting, card, battle royale and real-time strategy (RTS) games. Popular esports franchises include League of Legends, Dota, Counter-Strike, Valorant, Overwatch, Street Fighter, Super Smash Bros. and StarCraft, among many others. Tournaments such as the League of Legends World Championship, Dota 2's International, the fighting game-specific Evolution Championship Series (EVO) and Intel Extreme Masters are among the most popular in esports. Many other competitions use a series of league play with sponsored teams, such as the Overwatch League. Although the legitimacy of esports as a true sporting competition remains in question, they have been featured alongside traditional sports in some multinational events in Asia, with the International Olympic Committee also having discussed their inclusion into future Olympic events.'''

parser = PlaintextParser.from_string(text, Tokenizer("english"))

summary = summarizer(parser.document, 4)

summarized = ""

for sentence in summary:
    summarized += str(sentence)
print(summarized)
