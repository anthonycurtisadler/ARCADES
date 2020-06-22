# ARCADES
sophisticated academic notetaking software inspired by Walter Benjamin's Arcades Project. 


ARCADES is an SQLITE-based notetaking application built around the needs of academic users in the humanities.
Design goals include quick, command-driven, workflow; elimation of redundancy in data entry (keywords specific to a given project can automatically be added to each note; the greatest possible logical expressiveness in searching; and organizational flexibility.  

Each note consists in a UNIQUE INDEX (a sequence of natural numbers), KEYWORDS and keyword TAGS, and a string of unicode text.

Notes can be linked by including the index of another note among the keywords. 

Tags can be subordinated into higher order genuses (Kant/German philosopher=philosopher=thinker)
Keywords can also be organized through relations. (Kant influenced Fichte, Fichte influenced Hegel)
Special "sequence keywords" can be used to keep track of page numbers, dates, or even index values.

It is possible to search over nearly all attributes of the note, and the seerch phrase permits full logical argiculativeness by combining terms with AND (&), OR (|), NOT (~), and nested parentheses.

The non-GUI display allows for RAPID cycling through notes with a variety of different iteration modes. 

The presentation of notes is simple yet elegant.

The structure of the notebook can be manipulated with powerful text commands, and it is possible to "feed" the result of searches back into other commands. 




EXAMPLES OF VALID SEARCH QUERIES


SINGLE TERMS 
(1) ?:Heidegger 					        # Search for all notes containing “Heidegger” in the text
(2) search:Heidegger				      # variant form of (1)
(3) ?:HEIDEGGER 				          # Like (1), but capitalized or non-capitalized variants.
(4) ?:<Heidegger> 				        # Like (1), but searches for a keyword.
(5) ?:<HEIDEGGER> 				        # Like (1), but for keywords.
(6) ?:*egge*	                    # Search for all notes with words containingt “egge”
(7) ?:<*egge*>					          # (6) for keywords
(8) ?:Hei*					              # Like (6), but starting with “Hei”
(9) ?:<Hei*>					            # Like (7), but for keywords.
(10) ?:<#philosopher>		`		      # Finds all notes with keywords tagged “philosopher”
(11) ?:<##theoretician>	          # Find all notes with tags subsumed under the genus “intellectual”
(12) ?:<?Husserl?infleunced?> 	  #Search for all note with keywords “influenced” by #“Husserl”
(13) ?:<?Husserl?influenced*> 	  #Like (13) but searches over the entire tree of |influences
(14) ?:<page@1/page@10>			      #Searches for sequence keyword “page” with values
						                      # between 1 and 9
(15) ?:Being$and$Time$				    # Search for the exact phrase  “Being and Time”
(16) ?:$Being$Time$				        # Search for a phrase beginning with “Being”
						                      # and ending with “Time”
(17) ?:$$ing$im$$	                # Wildcard phrase search for a phrase beginning *ing* and ending *im*

QUALIFIED TERMS
(18) ?:Heidegger"date=2020-1/2020-6"		           # (1), restricted to notes between 2020-1 and 2020-6
(19) ?:<Heidegger>"index=/1000"		                 # (4), restricted to notes with indexes <= 1000
(20) ?:<Heidegger>"index=/1000!depth=1/1"	         # (19), but also restricted to notes with indexes of depth 1
(21) ?:Heidegger"count=3/"			                   # Notes in which “Heidegger” appears at least 3 times
(22) ?:Heidegger"slice=.1.1.1.1.1.1/.1.1.1.1.1.1"	 # (1), restricted to notes with Index elements rank 2-7 = 1
(23) ?:Heidegger”user=USER”			                   # (1), restricted to notes by USER
(24) ?:Heidegger”size=30/70”			                 # (1), restricted to notes of size <=70 and >=30.
(25) ?:_ALLNOTES_”depth=/1”		                     # Retrieve all notes in search scope with depthj <=1

COMPLEX PHRASES
(26) ?:Heidegger & Husserl                        	      #Notes containing both “Heidegger” and “Husserl” in the text
(27) ?:<HEIDEGGER> | <HUSSERL> 	                          # Notes with keyword “Heidegger” or “Husserl”
(28) ?:(Heidegger & Husserl) & (<HEIDEGGER> | <HUSSERL>)  # Must satisfy conditions of (26) and (27)
(29)   ?:((Heidegger | Husserl) & Kant) | (Deleuze & Spinoza)
(30)   ?:((Heidegger"count=3/4" | Husserl) & Kant"count=5/6") | (Deleuze & Spinoza) & <#scientist>

REFEEDING 
(31) ?:Heidegger => show:? 			            # Execute (1) and feed the result into the show.

LIMITING
(32) ?:Heidegger %%1-100			              # Limit (1) to the indexes 1-100

There is no inherent limit to the logical complexity of the search phrase. 
		  	

						







