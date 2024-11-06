# To be corrected

- detect `o` as a bullet
- handle this (white space at the end of a line when no white space should be inserted ex: "ci- dessous")
  ex.
  "de résistivité (résistance spécifique d’une substance). Le tableau ci- dessous retrace les différentes caractéristiques de ces matières"

## To be done after the major refactoring on the line's processing

- the production of the md-string elements could be postponed to after the "classification" and "qualification" steps of the data chunks
- some kind of raw text formatting should be implemented to be able to use Spacy and other NLP tools

## Problems identified in the tests

- STIFF p. 1

```md
**STIF** Société anonyme de droit français au capital de 1 554 000 euros Siège social : Zone d’activité de la Lande - 49170 Saint-Georges-sur-Loire RCS Angers 481 236 974
```

should be

```md
**STIF**
Société anonyme de droit français au capital de 1 554 000 euros
Siège social : Zone d’activité de la Lande - 49170 Saint-Georges-sur-Loire
RCS Angers 481 236 974
```

- STIFF, p. 119: bottom part fully messed up ; undetected bullet formatting
