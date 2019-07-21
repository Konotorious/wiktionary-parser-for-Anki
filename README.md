# wiktionary-parser-for-Anki

I wrote this little script in order to generate [Anki](https://apps.ankiweb.net/) cards of Esperanto words derived from French and Spanish words. It goes parses the relevant Wiktionary category pages (namely, [this](https://en.wiktionary.org/wiki/Category:Esperanto_terms_derived_from_French) and [that](https://en.wiktionary.org/wiki/Category:Esperanto_terms_derived_from_Spanish)) and outputs a text file in a format importable by Anki, assuming fields for word, definition, part of speech and etymology. Default output provided as an example.

What category pages are parsed, which langgaue is targeted, as well as which parts of speech are extracted (nouns, proper nouns, verbs, adjectives, adverbs, prepositions and interjections by default) can be easily edited at the top of the file.

Requires Beautifulsoup4 to run. 
