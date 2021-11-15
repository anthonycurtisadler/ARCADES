class GetNotes:

    def __init__ (self,text):

        self.text = text
        self.divider = 'Highlight'
        self.break_mark = '/###/'
        self.size = 0 

    def return_iterator (self):

        def get_between (x,y,z):
            try:
                return x.split(y)[1].split(z)[0].strip()
            except:
                return ''

        def structured_output(phrase):

            lines = phrase.split('\n')
            head = lines[0]
            text = '\n'.join(lines[1:])
            note = ''
            if 'NOTE' in text:
                text_temp = text.split('NOTE')[0]
                note = text.split('NOTE')[1]
                text = text_temp
            

            highlight_color = get_between(head,'(',')')
            part = get_between(head,'PART','>')
            page = get_between(head,'Page','·')
            location = get_between(head,'Location','XX')

            return (highlight_color,part,page,location,text,note)
            

        def iterator ():
            self.position = 0

            self.text = self.text.replace(self.divider,self.break_mark+self.divider)
            all_notes = self.text.split(self.break_mark)
            self.size = len(all_notes)
            if len(all_notes)>1:
                all_notes = all_notes[1:]

            for x in all_notes:
                self.position +=  1
                yield structured_output(x)

        return iterator 


            
            
sample_text ="""
Notes and highlights for
Dead Souls (Penguin Classics S.)
DEAD SOULS
Highlight (yellow) - PART I > Page 6 · Location 975
In the corner shop , or , rather , in its window , a purveyor of hot spiced honey drinks had installed himself , with a samovar of red copper and a face just as red as the samovar , so that from a distance you might think that there were two samovars standing in the window , if one samovar hadn’t been wearing a beard black as pitch .
Highlight (yellow) - PART I > Page 7 · Location 986
In this tiny kennel he set up a narrow little three - legged bed against the wall , and covered it with a small semblance of a mattress , which had been beaten flat as a pancake and was perhaps just as greasy as the pancake he had managed to wheedle out of the innkeeper .
Highlight (yellow) - PART I > Page 7 · Location 989
As to what these common rooms are like , any traveller knows very well : the same walls , covered with oil paint , darkened above by tobacco smoke and rubbed shiny below by the backs of various travellers , and still more by those of the local merchants , since the merchants , on market days , would come here in sixes and sevens to drink their well - known serving of tea ; 7 the same soot - begrimed ceiling ; the same smoked chandelier , with its multitude of glass pendants which danced and tinkled every time the houseman ran across the worn oilcloth strips , boldly brandishing a tray on which perched a flock of teacups thick as birds on a seashore ; the same pictures , painted in oil , that took up an entire wall – in a word , everything was the same as it is everywhere , the sole difference being that one painting depicted a nymph with breasts so enormous that the reader has probably never seen their like .
Highlight (yellow) - PART I > Page 7 · Location 999
As for bachelors , I can’t say for sure who performs this service , Lord only knows : I have never worn such scarves .
Highlight (yellow) - PART I > Page 8 · Location 1005
As in enlightened Europe , so too in enlightened Russia there are now a great many respectable people who cannot dine at an inn without striking up a conversation with a servant , sometimes even having a good laugh at his expense .
Highlight (yellow) - PART I > Page 8 · Location 1010
how many peasant souls so - and - so possessed , how far he lived from town , even what sort of character he had and how often he came to town .
Highlight (yellow) - PART I > Page 8 · Location 1014
This distinction , though to all appearances entirely innocent , nonetheless earned him much respect on the part of the inn - servant , so much so that every time he heard this sound , he gave his hair a toss , drew himself up more deferentially and , inclining his head from on high , asked whether the gentleman required anything
Highlight (yellow) - PART I > Page 9 · Location 1021
Collegiate Councillor Pavel Ivanovich Chichikov , 10 landowner , on private business ’ .
Highlight (yellow) - PART I > Page 10 · Location 1050
As it was , there was nothing particularly noteworthy in the bill : a drama by Mr Kotzebue15 was being presented , with Rolla played by Mr Poplyovin , and Cora by Miss Zyablova .
Highlight (yellow) - PART I > Page 10 · Location 1053
He then turned it over to see if there was anything on the other side , but finding nothing , rubbed his eyes , folded it neatly and placed it in the small box to which he habitually consigned everything that came to hand .
Highlight (yellow) - PART I > Page 11 · Location 1061
A pity that it’s rather difficult to remember all the powerful ones of this world ; but suffice it to say that the newcomer displayed extraordinary activity in the matter of visits : he even went to present his compliments to the Inspector of the Medical Board and the town architect .
Highlight (yellow) - PART I > Page 12 · Location 1085
There were carriages with lanterns , two gendarmes stationed in front of the porch , the distant shouts of postilions – in a word , everything was as it should be .
Highlight (yellow) - PART I > Page 13 · Location 1092
Sated by the riches of summer , which in any event sets out tasty dishes at every turn , they have decidedly not flown here for the purpose of eating , but merely to display themselves , to strut back and forth over the heap of sugar , to rub their back or front legs against each other , or to use them to scratch under their wings or , extending both front legs , to rub them together above their heads , then turn about and again fly off , and again fly back in fresh , importunate squadrons .
Highlight (yellow) - PART I > Page 13 · Location 1100
The men here , as everywhere , were of two types . The first consisted of very thin ones , who kept hovering about the ladies . Some of these were of the kind that could be distinguished from their St Petersburg counterparts only with difficulty : they had the same very neatly , carefully considered and tastefully combed side - whiskers , or else simply pleasant - looking , very smooth - shaven ovals for faces . They seated themselves next to the ladies in the same casual way , spoke French in the same way and made the ladies laugh in the same way as in Petersburg . The second type was made up of fat men or of those like Chichikov , that is , not overly fat but not overly thin either .
Highlight (yellow) - PART I > Page 14 · Location 1108
These were the highly respected officials of the town . Alas ! The fat ones of this world know how to manage their affairs better than the thin ones . The thin ones are mostly employed on special assignments or are merely carried on the civil service list , and flit about hither and yon . Their existence is weightless , insubstantial and utterly insecure . The fat men , on the other hand , never occupy peripheral positions but always central ones , and if they do sit down somewhere , then they sit securely and firmly , and the seat would sooner crack and sag beneath them than they would fly off it .
Highlight (yellow) - PART I > Page 14 · Location 1116
At length the fat man , having rendered service to God and Tsar , having earned the respect of one and all , leaves his position , transfers his household and becomes a landowner , a glorious Russian lord and master , the soul of hospitality , and he lives , and lives well .
Highlight (yellow) - PART I > Page 14 · Location 1118
After he is gone , his thin little heirs once again , in the time - honoured Russian way , gallop through the paternal fortune at full tilt .
Highlight (yellow) - PART I > Page 15 · Location 1139
To propitiate his opponents even further on this point or that , he would offer them , on each occasion , his enamelled silver snuff - box , at the bottom of which they noticed two violets that had been placed there for fragrance .
Highlight (yellow) - PART I > Page 16 · Location 1143
inasmuch as the first thing he wanted to know was how many peasant souls each of them owned , and what was the condition of their estates , and only then did he inquire about their first names and patronymics .
Highlight (yellow) - PART I > Page 17 · Location 1164
Whatever the topic of conversation , he always knew how to hold up his end : if the talk was of a stud - farm , he too would talk of stud - farms ; if people were chatting about fine dogs , here too he would venture some very sensible observations ; if the matter under consideration touched upon an investigation being conducted by the Fiscal Chamber , 25 he showed that he was not ignorant of judicial hanky - panky ; if the discussion turned to billiards , he didn’t let his end down when it came to billiards either ; if people were talking about virtue , then he could discourse on virtue very well too , and even with tears in his eyes ; if about the distilling of spirits , then he knew a lot about spirits as well ; if about customs inspectors and officials , then he could also expatiate on them as if he himself had been both an official and an inspector .
Highlight (yellow) - PART I > Page 18 · Location 1178
Such was the opinion , highly flattering to the guest , that was formed of him in the town , and it remained unchanged until such time as a certain strange characteristic of the guest , and an enterprise , or , as they say in the provinces , a turn of events , of which the reader will presently learn , threw virtually the entire town into utter bewilderment .
Highlight (yellow) - PART I > Page 19 · Location 1189
It will not be superfluous for the reader to make the acquaintance of these two serfs who belonged to our hero . Although as characters they are not , of course , so prominent , but are rather what is called secondary or even tertiary , and although the main levers and springs of this poem do not rest on them and only here and there touch and lightly catch at them – still , the author likes to be extremely circumstantial in everything , and in this respect too , despite being a Russian himself , he wishes to be as thoroughgoing as a German .
Highlight (yellow) - PART I > Page 20 · Location 1209
– Lord only knows ; it’s hard to know what a house serf is thinking while his master is taking him to task . And so , that’s what can be said about Petrushka for the nonce .
Highlight (yellow) - PART I > Page 22 · Location 1233
In a word , these were familiar scenes .
Highlight (yellow) - PART I > Page 24 · Location 1271
But if you take all these other gentlemen , of whom there are many in the world , and who greatly resemble one another in appearance , yet in whom , as soon as you look more closely , you will perceive many highly elusive traits – such gentlemen are dreadfully difficult to portray .
Highlight (yellow) - PART I > Page 24 · Location 1275
Perhaps only God could have said what sort of character Manilov had . There is a species of people who are known as ‘ just plain folks ’ , ‘ neither one thing nor another ’ or , as the saying has it , ‘ neither fish nor fowl ’ .
Highlight (yellow) - PART I > Page 25 · Location 1282
You would wait in vain for any lively or even arrogant word , such as you might hear from almost anyone else if you broached some subject that touched him to the heart .
Highlight (yellow) - PART I > Page 25 · Location 1290
At home he spoke very little , and for the most part cogitated and pondered , but what he pondered was also known only to God .
Highlight (yellow) - PART I > Page 25 · Location 1295
‘ Master , let me go off to find outside work , to earn enough for the soul - tax , ’
Highlight (yellow) - PART I > Page 26 · Location 1310
His wife … however , they were utterly content with each other . Even though more than eight years had passed since they had become one , each still continued to bring the other either a bit of apple , or a sweet , or a nut , and would say , in a touchingly tender tone that expressed perfect love : ‘ Open that cute little mouth of yours , my pet , and I’ll just pop this bit into it . ’
Highlight (yellow) - PART I > Page 27 · Location 1317
In a word , they were what is called happy .
Highlight (yellow) - PART I > Page 27 · Location 1322
And in boarding schools , as we know , three main subjects constitute the foundation of human virtues : the French language , which is indispensable for a happy family life ; the piano , for affording one’s spouse some pleasant moments ; and , finally , in the specifically homemaking skills , the knitting of purses and other surprises .
Highlight (yellow) - PART I > Page 29 · Location 1353
‘ How well he can , so to speak , you know , receive anyone at all , observe delicacy in all his actions , ’ Manilov interjected with a smile and nearly squeezed his eyes shut with pleasure , like a tomcat that is being lightly tickled behind the ears with a finger .
Highlight (yellow) - PART I > Page 33 · Location 1430
‘ Permit me not to permit you to do so , ’ said Manilov with a smile . ‘ This armchair has always been assigned to guests : like it or not , this is where you must sit . ’
Highlight (yellow) - PART I > Page 35 · Location 1466
‘ No , what I’m referring to is not exactly peasants , ’ said Chichikov . ‘ I wish to have the dead ones
Highlight (yellow) - PART I > Page 36 · Location 1478
‘ And so , I would like to know whether you can transfer to me , or let me have , or however you deem it best , those souls that are not actually living , but are living as far as legal form is concerned . ’
Highlight (yellow) - PART I > Page 37 · Location 1496
But permit me to put it to you this way : will not this undertaking , or , to express myself more , so to speak , precisely , this negotiation , will not this negotiation prove incompatible with the civil decrees and the future prospects of Russia ? ’
Highlight (yellow) - PART I > Page 37 · Location 1498
Here Manilov , making a slight movement of his head , directed a very significant look at Chichikov’s face , displaying , in every feature of his own face and in his compressed lips , an expression of such profundity as has never perhaps been seen on a human face , except possibly on that of some overly clever government minister , and then only when some utterly head - breaking business was at issue .
Highlight (yellow) - PART I > Page 38 · Location 1505
‘ What do you mean , a price ? ’ Manilov spoke again , and stopped . ‘ Do you really suppose that I would take money for souls who have , in a certain sense , ended their existence ? If a desire as imaginative , so to speak , as this has entered your head , then I , for my part , will transfer them to you without any thought of gain and will take the deed of purchase upon myself . ’
Highlight (yellow) - PART I > Page 38 · Location 1518
What harassments , what persecutions have I not known , what grief have I not tasted , and for what ? For upholding the truth , for being pure of conscience , for extending a hand both to the helpless widow and to the orphan in distress ! ’ Here he employed his handkerchief to wipe away a tear that rolled down his cheek .
Highlight (yellow) - PART I > Page 41 · Location 1559
Chichikov’s strange request suddenly put an end to all his reveries . The thought of it , in particular , somehow resisted absorption by his brain . However much he turned it this way and that , he simply could not explain it to himself , and all this time he was sitting and smoking his pipe , and so continued right up to suppertime .
Highlight (yellow) - PART I > Page 43 · Location 1577
Then he shouted at all of them : ‘ Hey there , you beauties ! ’ and he flicked all three with the whip , now no longer by way of punishment , but in order to demonstrate his satisfaction with them .
Highlight (yellow) - PART I > Page 45 · Location 1626
Why shouldn’t you use the whip , if there’s good reason ? It’s all up to the master . There has to be whippin ’ ’ cause the peasant acts up , you gotta keep order . If there’s good reason , then go ahead an ’ use the whip , why not use the whip ? ’
Highlight (yellow) - PART I > Page 48 · Location 1673
he felt relieved , for he realized that the clock on the wall had conceived a desire to strike .
Highlight (yellow) - PART I > Page 51 · Location 1715
Once dressed , he went up to the mirror and sneezed again , so loudly that a turkey - cock that had come up to the window at the same moment – the window was very close to the ground – suddenly set up a very rapid gobbling in its strange language , probably ‘ God bless you , ’ in response to which Chichikov called it a fool .
Highlight (yellow) - PART I > Page 52 · Location 1738
The reader , I think , has already noticed that Chichikov , despite his affable air , was nonetheless speaking with greater freedom than he had done with Manilov , and stood on no ceremony whatsoever . It must be said that in this Rus of ours , if we have not yet kept pace with foreigners in this or that respect , then we have far outstripped them in our knowledge of the proper way to behave .
Highlight (yellow) - PART I > Page 53 · Location 1748
I invite you to have a look at him when he is sitting among his subordinates – why , you’d be too scared to breathe a word ! Pride and nobility and who knows what else is expressed on his face ? Just pick up your brush and start painting : a Prometheus , 7 a veritable Prometheus ! He has the gaze of an eagle , and a stride that’s smooth and measured . But this very same eagle , as soon as he leaves his room and approaches his superior’s office , scurries along , papers tucked under his arm , like such a partridge that there’s no enduring it .
Highlight (yellow) - PART I > Page 53 · Location 1753
In society and at an evening party , if all present are not of any great rank , Prometheus will simply remain Prometheus , but the moment anyone slightly higher than himself appears , Prometheus will undergo a metamorphosis such as even Ovid8 couldn’t invent : he’s a fly , even less than a fly , he’s reduced to a grain of sand !
Highlight (yellow) - PART I > Page 54 · Location 1778
‘ God spared us such a misfortune ; a fire would have been even worse ; he burned up all by himself , dear sir . Something inside him started burning somehow , he’d had too much to drink . A blue flame just came out of him , and he smouldered and smouldered all over , and turned black as charcoal , and he was such a really skilful blacksmith ! And now there’s nothing for me to go out for a drive in ; there’s no one to shoe the horses . ’
Highlight (yellow) - PART I > Page 56 · Location 1810
‘ Listen here , dear lady … ugh , what sort of person are you ! What can they possibly be worth ? Look at it this way : they’re just dust , after all . Do you understand ? They’re simply dust . You take any worthless , utterly insignificant thing , for instance even an ordinary rag , and the rag has its price : it can at least be sold to a paper - mill , but these … these souls are totally useless . Well , you tell me , what are they useful for ? ’
Highlight (yellow) - PART I > Page 60 · Location 1875
The author is certain that there are readers curious enough to wish to learn about the plan and internal layout of the casket . That’s fine with me : indeed , why not satisfy them ! Here it is , the internal layout .
Highlight (yellow) - PART I > Page 61 · Location 1894
He was especially struck by a certain Pyotr Savelyev Neuvazhay - Koryto , so much so that he could not help saying : ‘ Heavens , that’s a long one ! ’ Another had Korovy Kirpich hooked on to his name , and another appeared simply as Koleso Ivan . 14 As he was finishing his writing , he drew several deep breaths through his nose and smelled the enticing aroma of something hot and buttery .
Highlight (yellow) - PART I > Page 62 · Location 1926
Whether Korobochka , or Manilov’s wife , whether household life or non - household life – let us pass them by ! That is not what is cause for wonder in this world : in an instant joy can turn into sadness , if only you linger too long before it , and then God only knows what will pop into your head .
Highlight (yellow) - PART I > Page 63 · Location 1929
Is the chasm really so great that separates her from her sister , who is shut up inaccessibly behind the walls of an aristocratic house with its fragrant wrought - iron staircases , its gleaming copper , its mahogany and its carpets , yawning over an unfinished book as she awaits a witty visit from society , which will afford her an arena where she can let her intelligence shine and give expression to ready - made views , views which , according to the laws of fashion , occupy the town for an entire week , views not concerning what is going on in her home and on her estates , all of which are in total confusion and disarray , thanks to her ignorance of good management , but rather concerning the kind of political upheaval that is brewing in France , and the direction that has been taken by fashionable Catholicism . 16 But
Highlight (yellow) - PART I > Page 63 · Location 1935
But why then in the midst of unthinking , happy , carefree moments , does another wondrous mood flash upon us suddenly , all of itself ? Scarcely has laughter completely died from the lips when it has already become something else among these very same people , and already the face is illumined in a different light .
Highlight (yellow) - PART I > Page 64 · Location 1953
The dappled horse felt extremely unpleasant lashes falling on his plump and broad parts . ‘ Well , well , he’s really got carried away ! ’ he thought to himself , with a slight twitch of his ears . ‘ I guess he knows where to hit ! He doesn’t lash you straight across the back , but just picks the most sensitive spot – a tickle on the ears , or a lash under the belly . ’
Highlight (yellow) - PART I > Page 67 · Location 1991
In the room he encountered all the old friends that one always encounters in wooden inns of modest size , which have been built along the roads in no small number , namely : a samovar covered with what looked like hoar frost ; smoothly planed pine walls ; a three - cornered cupboard with teapots and teacups , in one corner ; small gilt porcelain eggs hanging from blue and red ribbons in front of the icons ; a cat that had recently had kittens ; a mirror that reflected back four eyes instead of two and instead of a face some sort of flat cake ; and , finally , fragrant herbs and carnations stuck in bunches behind the icons , but so dried out that anyone wishing to smell them could only sneeze , and nothing more .
Highlight (yellow) - PART I > Page 67 · Location 1996
‘ Is there any suckling pig ? ’ Such was the question that Chichikov put to the old woman standing there . ‘ There is . ’ ‘ With horseradish and sour cream ? ’ ‘ With horseradish and sour cream . ’ ‘ Bring it on ! ’ The old woman began to rummage about , and brought a plate , a napkin that was so starched that it buckled like dried bark , then a knife with a blade as thin as a penknife and a yellowed bone handle , a two - tined fork and a salt cellar , which simply could not be stood upright on the table .
Highlight (yellow) - PART I > Page 69 · Location 2026
Chichikov recognized Nozdryov , the same man whom he had met at the Public Prosecutor’s dinner , and who in just a few minutes had put himself on such an intimate footing that he had already begun addressing him in a familiar manner , although Chichikov , for his part , had given him no reason to do so .
Highlight (yellow) - PART I > Page 76 · Location 2155
Nozdryov’s type is probably already rather familiar to the reader . Everyone has had occasion to meet no small number of such people .
Highlight (yellow) - PART I > Page 77 · Location 2172
which he was present ever went off without its story . Some event would inevitably occur : either the gendarmes would
Highlight (yellow) - PART I > Page 83 · Location 2263
in a word , snatch it up and in it went , as long as the dish was hot , and the result would probably be a taste of some sort .
Highlight (yellow) - PART I > Page 86 · Location 2320
‘ What should I tell him ? ’ Chichikov thought , and after a moment’s reflection he declared that he needed the dead souls in order to acquire some standing in society , that he did not possess estates of any great size , so until such time as he did , he could use a few peasant souls .
Highlight (yellow) - PART I > Page 87 · Location 2334
He did not like even to permit anyone to treat him in a familiar manner , unless the person was of a very high rank . And for that reason he was now thoroughly offended .
Highlight (yellow) - PART I > Page 91 · Location 2406
That night he slept very badly . Some kind of small , very lively insects kept biting him and caused unbearable pain , forcing him to scrape the afflicted places , with all his fingers , while muttering : ‘ Oh , may the Devil take you along with Nozdryov ! ’
Highlight (yellow) - PART I > Page 95 · Location 2474
He saw his britska , which was all ready to go , with Selifan apparently awaiting a wave of his hand to bring it up to the steps , but there was absolutely no possibility of escaping from the room : standing in the doorway were two hefty serf - fools .
Highlight (yellow) - PART I > Page 96 · Location 2503
‘ You were involved in a matter involving the infliction of a personal offence , by means of birch rods , upon the landowner Maksimov while in a state of intoxication . ’
Highlight (yellow) - PART I > Page 99 · Location 2535
The graceful little oval of her face had the roundness of a delicate fresh egg , and , like it , glowed with a certain translucent whiteness , as when , fresh and newly laid , it is held against the light in the swarthy hands of the housekeeper testing it , and allows the rays of the beaming sun to pass through it .
Highlight (yellow) - PART I > Page 100 · Location 2541
As matters stood now , the dappled horse was so pleased with his new acquaintance that he didn’t have the slightest desire to try pulling himself out of the rut in the road where he had landed by courtesy of the unforeseen forces of fate , and laying his muzzle on the neck of his new friend , he seemed to be whispering what was probably some dreadful nonsense into his ear , because the new arrival kept twitching his ears incessantly .
Highlight (yellow) - PART I > Page 101 · Location 2566
Everywhere , in whatever realm of life , whether among its callous , coarsely impoverished and messily moldering lower ranks , or among its monotonously gelid and tediously tidy upper strata , everywhere , if but once , a person will encounter a phenomenon on his journey that is unlike anything he has chanced to see heretofore and that , at least once will awaken in him a feeling unlike any he is fated to feel for the rest of his life .
Highlight (yellow) - PART I > Page 102 · Location 2579
‘ A glorious litle wench ! ’ he said , opening his snuff - box and inhaling a pinch of snuff . ‘ But when you come right down to it , what’s really so nice about her ? What’s nice is that she’s obviously just graduated from some boarding school or institute , that as yet there’s nothing femalish , as they say , about her , nothing , that is , of what’s most unpleasant about these creatures .
Highlight (yellow) - PART I > Page 104 · Location 2618
It is well known that in this world there are many such faces , over whom nature has not taken any great pains when it comes to the finishing touches , has not employed any fine tools such as files , gimlets , and the like , but has simply hewn them out with full swings from the shoulder : one swing of the axe and there’s the nose ; another swing and there you have the lips ; she gouges out the eyes with a huge auger ,
Highlight (yellow) - PART I > Page 106 · Location 2648
The table , the armchairs , the straight - backed chairs – all had a profoundly cumbersome and unsettling quality to them . In a word , each object , each chair seemed to be saying : ‘ And I’m Sobakevich too ! ’ or ‘ And I too am very much like Sobakevich ! ’
Highlight (yellow) - PART I > Page 108 · Location 2679
The small table was set for four places . At the fourth place there soon appeared – it was hard to say definitely who she was , a married lady or a spinster , a relative , the housekeeper , or a woman simply living in the house – something without a cap , about thirty , and wearing a multicoloured shawl . There are people that exist on this earth not as objects in themselves , but as extraneous specks or tiny spots on objects .
Highlight (yellow) - PART I > Page 108 · Location 2691
‘ That’s how it seemed to you . But you see , I know what they buy at the market . Their scoundrel of a cook , who’s been trained by a Frenchman , will buy a cat , skin it and serve it at the table as rabbit . ’
Highlight (yellow) - PART I > Page 109 · Location 2698
You can plaster a frog with all the sugar you want , I won’t take it into my mouth , and I won’t take an oyster either :
Highlight (yellow) - PART I > Page 111 · Location 2742
Sobakevich went on listening , his head inclined as before , with nothing even vaguely resembling an expression on his face . It seemed as if there were no soul at all in his body , or rather , that if there were , then it was certainly not where it was supposed to be . Instead , as with Koshchey the Deathless , 11 it dwelt somewhere far , far away , hidden in a shell so thick that anything stirring in its depths created not the slightest ripple on the surface .
Highlight (yellow) - PART I > Page 117 · Location 2853
What’s more , you now have muzhiks under your sway , you’re on good terms with them and , of course , you won’t mistreat them , because they’re yours and it would be the worse for you ; but then you would have had clerks under you , and you would have made their lives miserable , having figured out that they were not your own serfs , or else you would have helped yourself to official funds !
Highlight (yellow) - PART I > Page 120 · Location 2899
A noun was also added by him to ‘ patched ’ , which was very felicitous but is not used in polite conversation , and we will therefore omit it .
Highlight (yellow) - PART I > Page 121 · Location 2911
Just as a countless multitude of churches , of monasteries with cupolas , domes and crosses is scattered across holy , pious Rus , so countless multitudes of tribes , generations and peoples throng in motley diversity and rush over the face of the earth . And each people that bears within it the pledge of mighty powers , and is filled with the creative capacities of soul , with its own bright singularity and other gifts from God , each has marked itself in its own original way with its own word , through which , in giving expression to any subject at all , it reflects , in so expressing , a part of its own character . With a deep knowledge of the heart and a wise grasp of life will the word of the Briton resound ; like a flippant fop will the ephemeral word of the Frenchman glitter and burst ; ingeniously will the German contrive his shrewdly spare word , which is not accessible to all ; but there is no word so sweeping , so bold , so torn from under the heart itself , so bubbling and quivering with life , as the aptly uttered Russian word .
Highlight (yellow) - PART I > Page 121 · Location 2919
Once , long ago , in the years of my youth , in the years of my childhood , which have flashed irretrievably by , it was a joy for me to drive up for the very first time to a place unknown . Whether humble hamlet , dreary district town , village or small settlement , it mattered not : much that was curious opened up to the curious eye of the child . Every structure , everything that bore the impress of some perceptible peculiarity , everything arrested and struck my attention . Whether a government house of stone , familiar in design , with half its windows false , jutting solitary and single from among a hewn - log cluster of ordinary little one - storey tradesmen’s houses , whether a rounded and perfect cupola , clad all over in sheets of white iron , raised up above a new church whitewashed like snow , whether a marketplace , whether a rural dandy who had landed in town – nothing escaped my fresh , fine attention , and , with nose thrust out of my travelling cart , I looked at the cut , hitherto unseen , of some frock - coat , and at wooden boxes of nails , of sulphur glowing yellow from afar , of raisins and soap glimpsed through the door of a grocer’s along with jars of stale Moscow sweets . I looked as well at an infantry officer walking off to one side , blown by some wind from God knows what province into the boredom of a district town , and at a merchant in a short Siberian caftan flashing by in a sulky , and in my thoughts I whirled along after them into their paltry lives . Were a district clerk to pass , I was already deep in thought : where was he going , whether to an evening at one of his fellow clerk’s , or straight to his own home , where , after spending half an hour or so on his porch , until dusk had not quite thickened into night , he would sit down to an early supper with his mother , his wife , his wife’s sister , and all the family , and what would they be talking about while a serving girl in a coin necklace or a boy in a quilted jacket brought in , after the soup , a tallow candle in an ancient , homemade candlestick . On driving up to the estate of some landowner , I looked with curiosity at the tall , narrow wooden belfry or at the spacious , dark old wooden church . The red roof and white chimneys of the landowner’s house flickered enticingly from afar through the green leafage , and I waited , impatient , till the gardens which screened it parted on both sides and it showed itself in its full and , alas ! in those days , by no means ordinary exterior , and from it I would try to guess what sort of man was the landowner himself , whether he was fat , and whether he had sons or a whole troop , six strong , of daughters with ringing girlish laughter , and their games and the youngest sister inevitably the prettiest , and whether they had dark eyes , and whether he himself was a jovial sort or gloomy as September in its final days , as he looked at the calendar1 and talked about rye and wheat , topics so tedious for young people .
Highlight (blue) - PART I > Page 125 · Location 2981
In a word , all was somehow desolate and splendid , as it is given to neither nature nor art to devise , but as happens only when they join together , when across the often senselessly accumulated toil of man , nature passes a finishing touch of the chisel , lightens the heavy masses , eliminates the crudely palpable symmetry and the beggarly rips through which peers the unconcealed , bare plan , and confers a wondrous warmth on everything that has been created in the chill of calculated purity and tidiness . 3
Highlight (blue) - PART I > Page 126 · Location 2992
Near one of the buildings Chichikov presently noticed a figure , which had begun to squabble with the muzhik who had arrived in the wagon . It took him a long time to make out the sex to which this figure belonged : peasant woman or muzhik . Its clothing was utterly indeterminate , but it very much resembled a woman’s garment ; on its head was a cap of the kind worn by female house servants in the country ; only the voice struck him as being rather husky for a woman . ‘ Oh , it’s a female ! ’ he thought to himself , and immediately added : ‘ Oh , it’s not ! ’ – ‘ Of course , a female ! ’ he finally said , having scrutinized it more intently .
Highlight (blue) - PART I > Page 127 · Location 3008
On a writing desk , inlaid with mother - of - pearl mosaic which had fallen out in places , leaving shallow , yellowish grooves filled with glue , lay a host of odds and ends : a pile of small papers covered in a small hand , and pressed under a marble paperweight green with age and topped by an egg - shaped handle ; an ancient book bound in leather binding and with red edging ; a lemon , completely shrivelled and no bigger than a wild hazelnut ; the broken - off arm of a chair ; a glass containing some liquid and three flies , which was covered with a letter ; a scrap of sealing wax ; a scrap of rag that had been picked up somewhere ; two quills smudged with ink and dried up as if from consumption ; a toothpick , completely yellowed , which the owner might perhaps have used to pick his teeth before the French invasion of Moscow .
Highlight (blue) - PART I > Page 128 · Location 3019
What precisely the heap contained was difficult to determine , for dust lay on it so thick that the hands of anyone touching it would come to resemble gloves .
Highlight (blue) - PART I > Page 128 · Location 3020
Protruding from the pile , more conspicuously than anything else , were the broken - off piece of a wooden shovel and the old sole of a boot . It would have been quite impossible to say that a living being inhabited this room , if it had not been proclaimed by the presence of an old , frayed nightcap lying on a table .
Highlight (blue) - PART I > Page 128 · Location 3027
‘ What about the master , then ? Is he at home , or not ? ’ ‘ The proprietor is here , ’ said the steward . ‘ Where is he , then ? ’ Chichikov repeated . ‘ What’s wrong with you , my good man , are you blind or what ? ’ said the steward . ‘ Come now ! The proprietor is me ! ’
Highlight (blue) - PART I > Page 129 · Location 3033
His tiny little eyes had not yet dimmed , and they darted about from under his high bushy eyebrows like mice when , thrusting their sharp little snouts from their dark holes , pricking up their ears and twitching their whiskers , they peer out to see whether a cat or a mischievous boy is lurking in wait somewhere , and give the air a suspicious sniff .
Highlight (blue) - PART I > Page 129 · Location 3043
Were anyone to glance into his work yard , where a huge reserve of all sorts of wood and utensils never destined to be used had been laid in , he would have wondered whether he had not somehow wandered into the Woodenware Market in Moscow , to which efficient mothers - in - law repair daily , cooks in tow , to stock up for their households , and where wood of every kind – fastened , lathed , dovetailed , finished and plaited – rises in white mountains : barrels , compartmented casks , tubs , buckets , jugs with spouts and without spouts , honeypots , punnets , hampers into which peasant women put their flax and other such rubbish , baskets of thin bent aspen wood , canisters of plaited birch - bark , and much else that serves the needs of Rus , rich and poor .
Highlight (blue) - PART I > Page 130 · Location 3049
An entire lifetime would not have been long enough for him to make use of them even on two such estates as his , but even so , these did not seem enough to him . Not content with such a state of affairs , he also walked through the streets of his village every day , peering under footbridges , under duckboards , and everything he came upon – an old sole , a peasant woman’s rag , an iron nail , a shard of earthenware – he would haul off to his house and place on the heap which Chichikov had noticed in a corner of the room . ‘ Look , there goes the fisherman , off to catch something ! ’ the muzhiks would say , when they saw him going in pursuit of his booty .
Highlight (blue) - PART I > Page 130 · Location 3056
If , however , a sharp - eyed muzhik caught him in the act , he didn’t argue and handed the plundered object back ; but once it had joined the heap , that was the end of it : he would swear that the object was his and had been bought by him at such - and - such a time , from so - and - so , or had come down to him from his grandfather . In his room he would pick everything up off the floor that he saw : sealing wax , a scrap of paper , a quill , and all this he would put on the writing desk or the window sill .
Highlight (blue) - PART I > Page 130 · Location 3061
The grain and fulling mills4 kept turning , the cloth manufactories , joiners ’ benches and spinning frames worked away ; the master’s sharp eye penetrated into everything , and like an industrious spider he ran , bustling yet efficient , to every corner of his domestic web . No very strong feelings registered on his features , but in his eyes there were signs of intelligence .
Highlight (blue) - PART I > Page 131 · Location 3079
The son , having been sent off to the provincial capital to learn in a government office what constituted real service in his father’s opinion , instead joined a regiment and wrote to his father only after he had been commissioned to request money for his uniforms . It was quite natural that in reply he received what in popular parlance is called a fig . Finally , the second daughter , who had remained at home with him , died , and the old man found himself the sole custodian , guardian and possessor of his riches .
Highlight (blue) - PART I > Page 132 · Location 3083
A life of solitude provided rich food for avarice , which , as we know , has the appetite of a wolf , and the more it devours , the more insatiable it becomes . Human feelings , which in any event did not run deep in him , grew shallower by the minute , and each day something more disappeared from that decaying ruin .
Highlight (blue) - PART I > Page 132 · Location 3090
He became increasingly intractable toward the buyers who would come to take away the products of his estate ; the buyers would haggle and haggle , and finally dropped him altogether , saying that he was a demon , and not a human being .
Highlight (blue) - PART I > Page 133 · Location 3106
It must be said that such a phenomenon is rarely encountered in Rus , where everything likes to expand rather than contract , and it is all the more striking by virtue of the fact that in the same neighbourhood lives a landowner who carouses with all the expansiveness of the Russian nature , reckless and lordly , burning the candle at both ends , as they say .
Highlight (blue) - PART I > Page 134 · Location 3113
Half the province , in all its finery , strolls gaily beneath the trees , and no one finds anything weird or sinister in this forced lighting , not even when an artificially illuminated branch , stripped of its bright greenery , leaps out dramatically from a wooded thicket , and because of that , the night sky above is darker and more austere and twenty times more sinister , and with their leaves trembling as they recede more deeply into the impenetrable gloom , the austere summits of the trees wax indignant at this tawdry brilliance that has illuminated their roots below .
Highlight (blue) - PART I > Page 137 · Location 3179
Why Proshka was wearing such big boots can be ascertained without further ado . For all the domestic servants , however many there were in the house , Plyushkin had only one pair of boots , which were always supposed to be kept in the entryway . Anyone summoned to the master’s chambers usually capered across the yard on bare feet , but once he had come into the entryway , he would put on the boots and appear in the room thus shod .
Highlight (blue) - PART I > Page 140 · Location 3225
And suddenly across that wooden face glided a warm ray . It was not a feeling that had found expression , but some pale reflection of a feeling , a phenomenon like the unexpected appearance of a drowning man on the surface of the water , which evokes a joyful shout from the crowd gathered on the bank . But in vain do the rejoicing brothers and sisters throw a rope from the bank and wait for another glimpse of the back or the arms exhausted from struggling – his one appearance was the final one . Everything is dead quiet , and thereafter the becalmed surface of the unresponsive element becomes even more dreadful and desolate . So too the face of Plyushkin , in the wake of the feeling that had glided across it for just an instant , became even more unfeeling and more ordinary .
Highlight (blue) - PART I > Page 142 · Location 3255
And such was the paltriness , pettiness and vileness to which a man could sink ! How could he have changed so much ! And is this true to life ? All this is true to life , for anything can happen to a man . The fiery youth of today would recoil in horror if you were to show him a portrait of himself in old age . So take with you on your journey , as you emerge from the tender years of youth into harsh , coarsening manhood , take with you all the human impulses , do not leave them along the way , you will not be able to pick them up later ! Dreadful and fearsome is the old age which will come , for it gives nothing back , nothing in return ! The grave is more merciful than it . On the grave will be written : ‘ Here lies a man ! ’ but you will read nothing in the cold , unfeeling features of inhuman old age .
Highlight (blue) - PART I > Page 143 · Location 3273
‘ How much would you give , then ? ’ asked Plyushkin , and he suddenly became all Jew : his hands started trembling like quicksilver .
Highlight (blue) - PART I > Page 145 · Location 3314
Dusk had already thickened when they reached the town . Shadow and light were thoroughly intermingled , and objects themselves seemed to have intermingled as well . The striped barrier - pole had taken on some indeterminate colour ; the moustaches of the soldier standing guard seemed to be growing on his forehead , much higher than his eyes , and his nose appeared to be missing altogether .
Highlight (blue) - PART I > Page 146 · Location 3322
town . Now and then some exclamations , apparently female , reached his ear : ‘ You’re lying , you drunkard ! I never allowed him any such crude behaviour ! ’ or : ‘ No fighting , you lout , off to the police station with you , and I’ll show you a thing or two there ! ’ In short , those words that will suddenly pour like boiling water on some daydreaming youth of twenty , when , on his way back from the theatre , his head is filled with a street in Spain , the night , the wonderful image of a woman with a guitar and wonderful curls . What isn’t lodged in his head , and what isn’t dreamed of there ? He is in heaven , and he has dropped in on Schiller10 for a visit – and suddenly the fateful words resound above him , like thunder , and he sees that once again he is back on earth , and even in Haymarket Square , 11 and close by a pothouse , and that once again life has began to strut its workaday self before him .
Highlight (blue) - PART I > Page 147 · Location 3339
‘ But I did open them , ’ said Petrushka , and he lied . However , his master knew that he had lied , but did not bother to object . After the journey he had made , he felt utterly exhausted . Ordering the lightest of suppers , which consisted only of suckling pig , he immediately undressed , and , crawling under the covers , fell into a deep and sound sleep , into that wonderful sleep which only those fortunate folk enjoy who are unacquainted either with haemorrhoids , or fleas , or overly powerful mental capacities .
Highlight (yellow) - PART I > Page 149 · Location 3357
But such is not the lot , and different is the fate of the writer who has made bold to summon forth everything that at every moment lies before the eyes and is not perceived by indifferent eyes , all the dreadful , appalling morass of trifles that mires our lives , all that lies deep inside the cold , fragmented , quotidian characters with which our earthly , at times bitter and tedious , path swarms , and who with the robust strength of an implacable chisel has made bold to set them forth in full and bright relief for all the people to see ! It is not for him to reap the plaudits of all the people , not for him to behold the grateful tears and unanimous enthusiasm of the souls that have been stirred by him ;
Highlight (yellow) - PART I > Page 149 · Location 3366
For the judgement of the time does not acknowledge that equally wondrous are the lenses that survey suns and those that convey the movements of imperceptible insects ; for the judgement of the time does not acknowledge that much spiritual depth is needed to illumine a picture drawn from ignoble life and elevate it into a pearl of creation ;
Highlight (yellow) - PART I > Page 149 · Location 3368
for the judgement of the time does not acknowledge that lofty enraptured laughter is worthy of taking its place beside the lofty lyrical impulse and that a whole abyss lies between it and the posturings of a clown in a fair - booth !
Highlight (yellow) - PART I > Page 150 · Location 3375
And distant as yet is that time when through a different font2 the awesome blizzard of inspiration will gush from a head invested in sacred horror and effulgence , and people will harken , in confused trepidation , to the majestic thunder of other speeches …
Highlight (yellow) - PART I > Page 150 · Location 3378
Let us take a sudden , headlong plunge into life , with all its noiseless chatter and tinkling bells , and have a look at what Chichikov is doing .
Highlight (yellow) - PART I > Page 151 · Location 3396
Each of the entries seemed to have some character all its own , and in consequence , it was as if the muzhiks themselves had taken on characters all their own .
Highlight (yellow) - PART I > Page 152 · Location 3416
“ Drunk as a cobbler , ” so goes the saying . I know you , my dear friend , I know you : if you want , I’ll tell you the whole story of your life . You were apprenticed to a German , who fed you and the other apprentices together , flogged you on the back with a strap for sloppiness and wouldn’t let you out of the house to have a little fun , and you were a wonder , not a cobbler , and the German couldn’t praise you enough whenever he spoke with his wife or with a Kamerad .
Highlight (yellow) - PART I > Page 156 · Location 3496
The gentleman uttered a cry ; it was Manilov . They immediately enfolded each other in an embrace and remained standing in the street for a good five minutes in this position .
Highlight (yellow) - PART I > Page 156 · Location 3498
Such was Manilov’s joy that the only thing that could still be seen on his face were a nose and lips ; his eyes had completely disappeared .
Highlight (yellow) - PART I > Page 156 · Location 3500
In the most refined and pleasant turns of speech he related how he had flown to town to embrace Pavel Ivanovich ; his outpouring ended with a compliment of the kind that is appropriate perhaps only for some young lady whom one has asked to dance .
Highlight (yellow) - PART I > Page 160 · Location 3557
Ivan Antonovich looked as if he was well past forty ; his hair was black and thick ; the entire middle part of his face protruded and ran all to nose ; in a word , it was the kind of face that in common parlance is called a jug - snout .
Highlight (yellow) - PART I > Page 160 · Location 3560
‘ My business is as follows : I have bought peasants from various owners in this district for relocation . I have the deeds of purchase , all that remains is to execute them . ’ ‘ Are the sellers present ? ’ ‘ Some are here , and I have powers of attorney from the others . ’
Highlight (yellow) - PART I > Page 163 · Location 3607
I’ll go ahead and give instructions now , ’ he said , and opened the door into the chancellery office , which was filled with clerks , who looked like industrious bees scattered over honeycombs , provided that honeycombs can be likened to official papers .
Highlight (yellow) - PART I > Page 164 · Location 3626
‘ Well , I myself see that I could not have undertaken a sounder business . Say what you like , a man’s purpose is not yet determined until he has planted a firm foot on a solid foundation , and not on some youthful , free - thinking fancy . ’ Here he castigated , and most appropriately , all young people for their liberalism , and rightly so .
Highlight (yellow) - PART I > Page 170 · Location 3741
and to Sobak - evich he began reciting Werther’s verse - letter to Charlotte , 28 in
Highlight (yellow) - PART I > Page 171 · Location 3754
Their eyes met , and instinctively they understood each other : the master is dead to the world , and we can look in on a certain place . Without further ado , after taking the tail - coat and pantaloons back into the room , Petrushka went downstairs , and they set out together , saying nothing to each other about the goal of their journey , and bantering along the way about completely irrelevant things .
Highlight (yellow) - PART I > Page 174 · Location 3794
The second enemy is the habit of a life of vagrancy that the peasants will inevitably acquire while they’re in the process of being relocated .
Highlight (yellow) - PART I > Page 175 · Location 3809
The opinions were of every stripe : there were those that smacked far too strongly of military cruelty and a severity that was almost excessive ; however , there were also those that were the very soul of mildness .
Highlight (yellow) - PART I > Page 175 · Location 3810
The Postmaster noted that Chichikov was faced with a sacred obligation , that he could become a kind of father to his peasants , as he put it , and even introduce the benefits of enlightenment , whereupon he spoke in a highly laudatory manner of the Lancaster School3 of mutual instruction .
Highlight (yellow) - PART I > Page 176 · Location 3829
The Postmaster had gone in more for philosophy and was reading most diligently , even at night , Young’s Nights and Eckartshausen’s Key to the Mysteries of Nature , 6 from which he made extremely lengthy excerpts covering whole pages , though just what sorts of things were contained in these extracts , no one had the slightest idea .
Highlight (yellow) - PART I > Page 176 · Location 3835
He also larded his speech rather effectively with a winking and squinting of one eye , all of which imparted a highly caustic tone to many of his satirical innuendos . The rest were also more or less enlightened people : some were reading Karamzin , some were reading the Moscow Gazette , 7 and some were even reading absolutely nothing at all .
Highlight (yellow) - PART I > Page 176 · Location 3841
All were the sort to whom their wives , in the tender exchanges that occur in private , would give names like Little Dumpling , Fattie - Pie , Plumpy - Poo , Darkie - Warkie , Kiki , Jou - Jou , and so on .
Highlight (yellow) - PART I > Page 177 · Location 3851
The ladies who lived in the town that will remain nameless were … no , I simply can’t ; a timid feeling of sorts comes over me .
Highlight (yellow) - PART I > Page 177 · Location 3855
The ladies who lived in the town that will remain nameless were what is called presentable , and in this respect they could be boldly held up as an example to all others .
Highlight (yellow) - PART I > Page 178 · Location 3868
In their morals the ladies living in the town that will remain nameless were strict , filled with noble indignation against vice of any kind , and against temptations of any kind , and they punished weaknesses of any kind without mercy of any kind .
Highlight (yellow) - PART I > Page 179 · Location 3878
‘ This glass is not behaving well , ’ or something of the kind . By way of ennobling the Russian language even more , virtually half its words had been banished from conversation , and it was therefore very often necessary to resort to the French language , and in French it was a different matter : there , words were permitted of a kind much coarser than the aforementioned .
Highlight (yellow) - PART I > Page 179 · Location 3893
At the same time it was said , even rather insultingly , that a markedly thin man was nothing more than something resembling a toothpick and not a human being .
Highlight (yellow) - PART I > Page 181 · Location 3926
Several bows were rendered to the mirror , accompanied by vague sounds that bore a slight resemblance to French , although Chichikov had absolutely no knowledge of French .
Highlight (yellow) - PART I > Page 182 · Location 3932
and though he never danced , he executed an entrechat . This entrechat had a small innocent consequence : the dresser began to shake and a brush fell from the table .
Highlight (yellow) - PART I > Page 182 · Location 3943
In a word , Chichikov spread joy and extraordinary cheer . There was not a face on which pleasure or at least a reflection of the universal pleasure did not register .
Highlight (yellow) - PART I > Page 185 · Location 3982
Their eyes alone are such an infinite realm , and once a man strays into it – then it’s goodbye to him ! There’s no pulling him out of there by hook or by crook .
Highlight (yellow) - PART I > Page 186 · Location 3999
Of course , the female half of the human race is an inscrutable lot ; but our esteemed readers , it must be acknowledged , can be even more inscrutable
Highlight (yellow) - PART I > Page 189 · Location 4049
if they notice any particularly good point about themselves , be it the forehead , or the mouth , or the hands , then they are bound to think that their best feature will be the first thing to strike everyone’s eye , and that everyone will suddenly begin to say , in one voice : ‘ Look , just look what a beautiful Grecian nose she has ! ’ or ‘ What a shapely , enchanting brow ! ’
Highlight (yellow) - PART I > Page 190 · Location 4074
It is even doubtful that gentlemen of this kind , that is , not exactly fat , and yet not exactly thin either , are capable of love ;
Highlight (yellow) - PART I > Page 190 · Location 4077
The violins and trumpets were scraping and blowing somewhere far , far away , and everything was shrouded in a mist that looked like the carelessly daubed ground of a picture .
Highlight (yellow) - PART I > Page 191 · Location 4082
She seemed to resemble a toy that had been painstakingly carved out of ivory ; she alone stood out , white , as she emerged , translucent and radiant , from the turbid and opaque crowd .
Highlight (yellow) - PART I > Page 191 · Location 4083
Evidently that is the way of the world ; evidently even the Chichikovs , for a few moments of their lives , turn into poets ; but the word ‘ poet ’ would really be too much .
Highlight (yellow) - PART I > Page 192 · Location 4101
this , and she even brushed the thick rouleau
Highlight (yellow) - PART I > Page 192 · Location 4109
The neglect that Chichikov had shown , almost unwittingly , even restored among the ladies a certain harmony that had been on the verge of disintegration after some of them had tried to appropriate the chair .
Highlight (yellow) - PART I > Page 192 · Location 4112
These verses were immediately ascribed to Chichikov . Indignation mounted , and in various corners of the room the ladies began talking about him in a most unfavourable manner , while the poor institute girl was completely annihilated , and already the verdict on her was pronounced .
Highlight (yellow) - PART I > Page 195 · Location 4150
But mortal man – in truth , it is difficult even to grasp how mortal man is fashioned : no matter how vulgar a piece of news may be , provided it is news , he will unfailingly communicate it to another mortal , even if for the sole purpose of saying , ‘ Just see what a lie they’ve been spreading ! ’ And the other mortal will incline his ear with pleasure , even though he himself will later say , ‘ Yes , it’s a downright vulgar lie that isn’t worth paying any attention to ! ’
Highlight (yellow) - PART I > Page 197 · Location 4187
ball is just a lot of nonsense , it’s not in the Russian spirit , not in the Russian nature , the Devil only knows what sort of thing it is : an adult , a full - grown man suddenly leaps out all in black , plucked
Highlight (yellow) - PART I > Page 197 · Location 4191
It’s all from aping others , all from aping others ! 26 The
Highlight (yellow) - PART I > Page 197 · Location 4193
feel as if you’ve committed some sin ;
Highlight (yellow) - PART I > Page 197 · Location 4197
of this ball ? Well , what if we suppose that some writer were to take it into his head to attempt a description of this whole scene exactly as it is ?
Highlight (yellow) - PART I > Page 197 · Location 4201
His vexation was mainly directed not at the ball , but at the fact that he had stumbled badly on this occasion , that he had suddenly shown himself for all to see in God knows what light , that he had played some strange , ambiguous role .
Highlight (yellow) - PART I > Page 198 · Location 4204
But man is a strange being : he was greatly pained by the ill will of those very people whom he did not respect and of whom he had spoken harshly , reviling their vain pursuits and fancy clothes .
Highlight (yellow) - PART I > Page 202 · Location 4264
Such , evidently , is the mood that’s in the air . It suffices merely to say that in a certain town there lives a stupid person , and that already makes them a real person . Suddenly a gentleman of respectable appearance will leap out and start shouting : ‘ But I’m also a person , and therefore I’m also stupid ’ ; in a word , he’ll instantly figure out what’s going on .
Highlight (yellow) - PART I > Page 202 · Location 4267
she was called by virtually one and all in the town that will remain nameless , to wit : the Lady Pleasant in All Respects . This name she had received in a legitimate manner , for , indeed , she spared nothing to make herself amiable to the nth degree . Although , of course , through the amiability there would dart – oh ! a sudden flash of the female character ! And although sometimes out of every pleasant word of hers there would stick ! – oh ! such a pin ! And God protect us from what was seething in her heart against any woman who somehow and in some way insinuated herself into the front ranks ! But all that was cloaked in the most refined manners that could possibly be found in a provincial capital . Every movement she made was in good taste , she even liked poetry , she even sometimes knew how to hold her head in a dreamy manner , and all agreed that she was indeed a Lady Pleasant in All Respects . As for the other lady , that is , the one who had come to visit , she was not possessed of so versatile a character , and therefore we shall call her the Merely Pleasant Lady .
Highlight (yellow) - PART I > Page 206 · Location 4335
But however filled the author is with veneration of the salutary benefits conferred on Russia by the French language , however filled with veneration towards our higher society’s praiseworthy custom of expressing itself in French at every hour of the day , out of a deep feeling of love for our fatherland , of course ; still , all that notwithstanding , he cannot bring himself to introduce a sentence from any foreign language , whatever it may be , into this Russian poem of his . And so , we shall continue in Russian .
Highlight (yellow) - PART I > Page 208 · Location 4371
But the Merely Pleasant Lady could find nothing to say . She was capable only of being upset , she simply did not have the resources to come up with any clever theory , and for that reason , she had a need , more than any other lady , for tender friendship and advice .
Highlight (yellow) - PART I > Page 208 · Location 4377
Thus a Russian lord and master , a dog - lover and doughty hunter , when riding up to a wood into which a hare has been driven by the beaters and is about to leap forth , is transformed in one single frozen moment , along with his mount and his raised whip , into gunpowder to which a flame is about to be applied . His eyes transfix the turbid air , and he will certainly overtake the beast , and will certainly finish it off , relentless as he is , no matter if the whole turbulent snowy steppe rises against him , hurling silvery stars into his lips , his moustache , his eyes , his brows and his beaver hat .
Highlight (yellow) - PART I > Page 210 · Location 4402
Now let it not seem strange to the reader that the two ladies could not agree on what they had seen at virtually one and the same time . There really are many things in this world that have this very peculiarity : if one lady looks at them , they will come out completely white , while if another lady looks at them , they will come out red , red as whortleberries .
Highlight (yellow) - PART I > Page 211 · Location 4420
it was just that in the course of their conversation a small desire to needle each other was born , all on its own . One simply slipped in a rather brisk little jibe when the occasion arose , for the sake of a small gratification : Here , this is for you ! Here , take it ! Gulp it down ! Impulses of various kinds lurk in the hearts of both the male and the female sex .
Highlight (yellow) - PART I > Page 212 · Location 4439
Our fraternity , we intelligent people , as we call ourselves , behave in almost the same way , and our learned discourses serve as proof of that . At first , the scholar approaches them like an uncommon kind of blackguard . He begins timidly , moderately , he begins with the humblest kind of inquiry : ‘ Is that not the origin ? Was it not from that particular little corner that such - and - such a country received its name ? ’ or , ‘ Does this document not belong to another , later time ? ’ or , ‘ When we say this particular people , do we really not mean this other people ? ’ He immediately cites this and that ancient writer , and as soon as he detects a hint or something that strikes him as a hint , then he hits his full stride , plucks up his courage , feels perfectly at ease in conversing with the ancient writers , puts questions to them and even answers them himself , completely forgetting that he has started out with a modest supposition . It now seems to him that he sees what’s what , that it is clear , and his discourse concludes with the words : ‘ And so , this is how it was , this is how a certain people should be understood , this is the viewpoint from which we should look at the topic ! ’ Then , from the lecture platform , he declaims it for all to hear , and a newly discovered truth embarks on its journey through the world , gathering to itself followers and admirers .
Highlight (yellow) - PART I > Page 214 · Location 4467
What was the meaning , really , what was the meaning of these dead souls ? There was absolutely no logic to the dead souls , how could dead souls possibly be bought ? Where would you find anyone fool enough for that ?
Highlight (yellow) - PART I > Page 214 · Location 4473
Still and all , they spread it , and so there must be some reason for it , mustn’t there ? But what was the reason for the dead souls ? No reason at all . So it turns out that it was all just blather , rot , nonsense , balderdash , poppycock . It was simply – the Devil take it ! …
Highlight (yellow) - PART I > Page 214 · Location 4475
In a word , rumours began to fly , and more rumours , and the entire town began talking about the dead souls and the Governor’s daughter , about Chichikov and the dead souls , about the Governor’s daughter and Chichikov , and everything and everyone was aroused .
Highlight (yellow) - PART I > Page 215 · Location 4489
another time and under other circumstances , rumours of this sort would perhaps have attracted no attention at all , but it had been a long time since the town that will remain nameless had received news of any kind . Over the course of three months there had not even been any instance of the kind of thing that in the two capital cities is called commérage , 7 which , as everyone knows , is the same for a town as the timely delivery of food supplies .
Highlight (yellow) - PART I > Page 215 · Location 4496
In this party , it must be noted to the credit of the ladies , there was incomparably more order and circumspection . For such , evidently , is their appointed task in life , to be good housekeepers and managers . With them everything quickly assumed a very definite aspect , was vested in clear and distinct forms , was explained and clarified ; in a word , the result was a finished picture .
Highlight (yellow) - PART I > Page 216 · Location 4508
For in Rus the lower orders of society are very fond of chatting about the gossip that circulates among the higher orders of society , and they therefore began to talk about all this in wretched hovels where they had never even seen Chichikov in the flesh and had no direct knowledge of him , and naturally fresh amplifications and still more clarifications began to make the rounds .
Highlight (yellow) - PART I > Page 217 · Location 4522
But no matter how stoutly the men armed themselves and put up resistance , their party had nothing like the orderliness of the women’s . With them everything was somehow coarse , unrefined , inelegant , unsuitable , unharmonious , unpleasant . Their heads were filled with tumult , hurly - burly , inconsistency and sloppy thinking – in a word , the empty nature of the male left its imprint on everything , a crude , ponderous nature , capable neither of running a household nor of holding wholehearted convictions , lacking confidence , slothful , filled with constant doubts and endless fears .
Highlight (yellow) - PART I > Page 218 · Location 4541
The term ‘ dead souls ’ had such an indefinite ring to it that people even began to suspect that it might contain some allusion to hastily buried bodies , as the result of two incidents which had occurred not so very long ago .
Highlight (yellow) - PART I > Page 222 · Location 4604
If you ask them about something directly , they will never remember anything , they won’t take it all in , they will flatly answer that they don’t know , but if you ask them about something else , they’ll proceed to drag everything in , and will relate it in more detail than you could possibly want to know .
Highlight (yellow) - PART I > Page 222 · Location 4607
All the inquiries undertaken by the officials revealed to them only that they knew nothing for certain about what Chichikov was , but that , nonetheless , Chichikov certainly had to be something .
Highlight (yellow) - PART I > Page 223 · Location 4617
weight ,
Highlight (yellow) - PART I > Page 224 · Location 4630
In the council which had gathered on this occasion , there was a highly conspicuous absence of that essential quality which among the common people is called horse sense . In general we have somehow not been created for representative bodies . In all our gatherings , from the peasants ’ village commune2 to scholarly committees and every other conceivable kind , a pretty fair degree of chaos reigns , unless one head is present to run everything .
Highlight (yellow) - PART I > Page 225 · Location 4656
‘ This , gentlemen , my dear sir , is none other than Captain Kopeykin ! ’ And when all asked , as one man : ‘ Who is this Captain Kopeykin ? ’ the Postmaster said : ‘ So you don’t know who this Captain Kopeykin is ? ’ All replied that they had absolutely no idea who this Captain Kopeykin was .
Highlight (yellow) - PART I > Page 232 · Location 4783
‘ But just a moment , Ivan Andreyevich , ’ the Chief of Police suddenly said , interrupting him , ‘ why , Captain Kopeykin , you said so yourself , had no arm or leg , while Chichikov … ’ At this the Postmaster cried out and slapped himself full force on the forehead , calling himself a stupid calf , publicly , in everyone’s presence . He could not understand how such a circumstance had not occurred to him at the very beginning of the story , and he admitted that the saying ‘ the Russian is wise after the fact ’ was fully justified .
Highlight (yellow) - PART I > Page 233 · Location 4792
From many theories , each clever in its own way , one finally emerged , strange though it is to mention : that Chichikov was Napoleon in disguise , that the English had long been envious because Russia , they said , was so great and vast , that on several occasions cartoons had even been published showing a Russian conversing with an Englishman .
Highlight (yellow) - PART I > Page 233 · Location 4806
At that time all our landowners , officials , merchants , shop assistants , and every other manner of people , literate and even illiterate , became , for eight years at least , passionate politicians .
Highlight (yellow) - PART I > Page 234 · Location 4812
The prophet had come from no one knew where , wearing bast shoes and an unlined sheepskin coat that reeked dreadfully of rotten fish , and had proclaimed that Napoleon was the Antichrist17 and was being kept on a stone chain behind six walls and beyond seven seas , but later on he would break the chain and gain mastery of the entire world . For
Highlight (yellow) - PART I > Page 235 · Location 4831
All his life he hasn’t cared a pin for doctors , but in the end he will turn to some old woman who works cures by whispering magic spells and spitting , or , even better , he himself will concoct something from who knows what rubbish , which , Lord knows why , he will imagine to be just the remedy for his illness .
Highlight (yellow) - PART I > Page 237 · Location 4874
And it became clear just what sort of creature man is : wise , intelligent and sensible in everything concerning others , but not himself .
Highlight (yellow) - PART I > Page 238 · Location 4882
was only then , as they extended condolences , that people learned that the deceased did in fact have a soul , although out of modesty he never gave any evidence of it . Yet
Highlight (yellow) - PART I > Page 238 · Location 4891
It’s enough for you to have one stupid side to your character out of nine other good ones for you to be regarded as a fool .
Highlight (yellow) - PART I > Page 239 · Location 4896
What winding , dead - end , narrow , impassable , far - straying roads have been chosen by mankind in its attempts to attain eternal truth , whereas before it the straight path lies open , like the path that leads to a magnificent temple appointed as a mansion for a tsar ! Broader and more splendid it is than all other paths , bathed in sunlight and illuminated by lamps the whole night long ; yet past it people have streamed in darkness obscure . And how many times already , guided by an intelligence that comes down from the heavens , have they , even so , managed to fall back and go astray , managed in broad daylight to blunder anew into impassable backwaters , contrived once more to becloud each other’s eyes with a blinding fog and , plodding along in pursuit of some will - o ’ - the - wisps , managed at last to come to an abyss , only then to ask each other in horror : ‘ Where is the way out , where is the road ? ’ The present generation now sees all this clearly , marvels at the blunders , laughs at the follies of its forebears , not perceiving that this chronicle is written in heavenly fire , that every letter in it cries out , that from all sides accusing fingers are pointed at it and it alone , at the present generation ; but the present generation laughs , and complacently , arrogantly embarks on a series of fresh blunders , at which its descendants will ultimately laugh as well .
Highlight (yellow) - PART I > Page 240 · Location 4922
Going out for him , as for any man who has regained his health , was truly festive . Everything he encountered took on a laughing air – houses and passing muzhiks , who , however , were rather sombre , since some of them had already contrived to clout a fellow muzhik on the ear .
Highlight (yellow) - PART I > Page 241 · Location 4941
Like a man half asleep , he wandered aimlessly through the town , being in no condition to decide whether he was the one who had gone mad , whether it was the officials who had lost their minds , whether all this was happening in a dream or whether some crazy nonsense was starting to brew in a wakeful state that was clearer than any dream .
Highlight (blue) - PART I > Page 248 · Location 5041
During that time he had the pleasure of experiencing those lovely moments that are familiar to every traveller , when everything has been packed in his bag and all that is left in the room are bits of string , scraps of paper and assorted rubbish scattered on the floor , when a man belongs neither to the road nor to a settled spot , when through the window he sees people passing by , plodding along , talking about their ten kopecks and raising their eyes in mindless curiosity only to glance at him and then continuing on their way , which is even more poisonous to the foul mood of the poor stranded traveller .
Highlight (blue) - PART I > Page 250 · Location 5080
The britska meanwhile had turned into more deserted streets ; soon came a stretch of nothing but long wooden fences that heralded the end of the town . Now the cobbled road came to an end as well , and the barrier - pole and the town were behind them , and there was nothing , and once again they were on their way . And once again , on both sides of the highroad , began the procession of verst - markers , post - station masters , wells , strings of carts , grey villages with samovars , peasant women and a jaunty bearded proprietor running out of a coaching inn with oats in hand , a wayfarer in tattered bast shoes , who had been plodding along for eight hundred versts , dreary little towns thrown up slapdash , with wretched little wooden shops , barrels of flour , bast shoes , kalaches , and other small items , striped barrier - poles , bridges under repair , fields beyond the eye’s grasp on either side of the road , the lumbering coaches of landowners , a soldier on horseback carrying a green box with lead grapeshot , labelled ‘ Such - and - Such an Artillery Battery ’ , green , yellow and freshly ploughed black strips flashing by on the steppes , a song struck up from afar , the tops of pines in the mist , the pealing of church bells fading in the distance , crows like flies and a horizon without end …
Highlight (blue) - PART I > Page 251 · Location 5089
Rus ! Rus ! I see thee , from my wondrous , beautiful far - away , thee I see : all is poor , scattered and comfortless in thee ; the gaze will be neither gladdened nor awe - struck by bold marvels of nature crowned by bold marvels of art , by towns with many - windowed lofty palaces ingrown into crags , by picturesque trees and ivies ingrown into houses , all set in the roar and eternal mist of waterfalls ; the head will not be thrown back to look at stone masses that tower above it on high without end ; there will be no gleam through dark arches piled one upon the other , entangled in grapevines , ivy , and countless millions of wild roses , no distant gleam through them of the eternal lines of shining mountains soaring into silvery , clear skies . Open , desolate and flat is everything in thee ; like dots , like specks thy low - lying towns protrude , imperceptible , amidst the plains ; there is nothing that captivates , nothing that charms the gaze . But what , then , is the inapprehensible mysterious force that draws one to thee ? Why is thy plaintive song heard , why does it resound , unremitting , in the ears , as it carries through all thy length and breadth , from sea to sea ? What is in it , in this song ? What calls , and sobs , and clutches at the heart ? What sounds are these that painfully caress me and seek to plumb my soul and twine about my heart ? Rus ! What is it that thou wantest from me ? What inapprehensible bond lies hidden between us ? Why lookest thou thus at me , and wherefore has everything within thee turned eyes filled with expectation upon me ? … And still , filled with perplexity , stand I unmoving , and already is my head o’ershadowed by an ominous cloud , heavy with oncoming rains , and benumbed is thought before thy expanse . What does this unembraceable space portend ? Is it not here , is it not in thee that a boundless thought is destined to be born , since thou thyself art without end ? Is it not here that a bogatyr is destined to live , since there is room for him to spread himself and stride about ? And awesome is the mighty expanse that will embrace me , reflecting itself with terrible force in my very depths ; by an unnatural power have my eyes been illumined . Ooh ! What a glittering , wondrous distance unknown to this world ! Rus ! …
Highlight (blue) - PART I > Page 252 · Location 5108
What a strange , and alluring , and uplifting , and wonderful something lies lodged in the word ‘ road ’ !
Highlight (blue) - PART I > Page 252 · Location 5115
The shining of the moon , now here , now there , as if white linen kerchiefs have been spread over walls , over pavements , over streets , all cut by slanting shadows black as coal ; wooden roofs lit by the sloping light shine like gleaming metal , and not a soul anywhere : all is asleep .
Highlight (blue) - PART I > Page 253 · Location 5128
How beautiful you are at times , O distant , distant road ! How often , like a man perishing and drowning , have I grasped at you , and each time you have magnanimously pulled me out and saved me ! And how many wonderful designs , poetic reveries have come to birth in you , how many marvellous impressions have been felt ! … But even our friend Chichikov was just then feeling the pull of reveries that were not altogether prosaic . Let us see precisely what it was that he was feeling .
Highlight (blue) - PART I > Page 253 · Location 5131
At first he felt nothing and merely kept glancing back now and then , wishing to assure himself that he had in fact left the town behind ; but when he perceived that the town had long since vanished , that there was no sign of smithies or mills or anything that is found in the vicinity of towns , and that even the white tops of the stone churches had long since sunk into the ground , he then began to occupy himself wholly with the road , looking only to the right and to the left , and the town that will remain nameless seemed to have left no trace in his memory , as if he had passed through it once long ago , in his childhood .
Highlight (blue) - PART I > Page 254 · Location 5144
under no circumstances will stoutness be forgiven a hero ,
Highlight (blue) - PART I > Page 254 · Location 5146
But it could happen that in this very tale other strings as yet unplucked will be heard , the incalculable richness of the Russian spirit will show forth , a male endowed with godlike prowess will pass through , or a wonderful Russian maiden , the like of which , with all the marvellous beauty of the female soul , all magnanimous aspiration and self - sacrifice , is not to be found anywhere in the world . And next to them , all the virtuous people of other tribes will seem dead , just as the book is dead beside the living word !
Highlight (blue) - PART I > Page 255 · Location 5153
the hero . And it is even possible to say why not . Because it is time , at last , to give the poor virtuous man a rest ; because the phrase ‘ virtuous man ’ comes too readily to our lips ; because the virtuous man has been made into a workhorse , and the writer does not exist who has not ridden him , goading him on with a whip and anything else that comes to hand ; because the virtuous man has been so worn down that not even a shadow of virtue remains on him , and all that remains of his body are ribs and skin ; because appeals to the virtuous man are hypocritical ; because the virtuous man is not respected . No , it’s time , at last , to put the rogue in harness too . And so , let’s harness the rogue !
Highlight (blue) - PART I > Page 256 · Location 5185
‘ Now Pavlusha , see that you do your lessons , don’t be naughty and stay out of mischief , and most of all , try to please your teachers and superiors . If you please your superiors , then even if you don’t do well in school and God has given you no talent , you will still get along and move ahead of everyone . Don’t get too friendly with your schoolmates , they won’t teach you anything good ; but if it comes to that , then make friends with those who are better off , as they can be of use to you if need be . Don’t treat or offer anyone anything ; instead , it’s best to act in such a way that you are the one being treated , and most of all , watch every kopeck and save it : it’s the one thing in this world that’s dependable . A schoolmate or a friend will deceive you , and when trouble comes he’ll be the first to betray you , but the kopeck won’t betray you , no matter what kind of trouble you’re in . You can do anything and overcome anything in the world with the kopeck . ’
Highlight (blue) - PART I > Page 258 · Location 5206
In his relations with his superiors , he conducted himself even more cleverly . No one knew how to sit as quietly on the bench as he . It must be noted that the teacher was a great lover of silence and good deportment , and could not bear clever and sharp - witted boys ; it seemed to him that they must be laughing at him .
Highlight (blue) - PART I > Page 259 · Location 5231
failing . In his sorrow the teacher took to drink , and finally he no longer had anything even for drink . Ill , without a crust of bread or any assistance , he was wasting away in some unheated , abandoned little hovel . His former pupils , the clever and sharp - witted boys whom he had constantly imagined to be guilty of unruliness and insolent behaviour , on learning of his pitiable situation proceeded to take up a collection for him , even selling many things they had need of themselves . Pavlusha Chichikov was the only one who pleaded a lack of funds , and gave nothing more than a silver five - kopeck piece , which his schoolmates promptly threw back at him , saying : ‘ Oh you skinflint ! ’ The poor teacher covered his face with his hands when he heard what his former pupils had done ; a torrent of tears gushed from his fading eyes , as if he were a helpless child . ‘ On my deathbed God has brought me to tears , ’ he murmured in a weak voice , and heaved a deep sigh when he heard about Chichikov , and went on to say : ‘ Ah , Pavlusha ! That’s how much a person can change ! There he was , so well behaved , nothing of the rebel in him , smooth as silk ! He took me in , he really took me in … ’
Highlight (blue) - PART I > Page 260 · Location 5249
And everything that had an air of wealth and sufficiency about it produced on him an impression that he himself could not explain .
Highlight (blue) - PART I > Page 261 · Location 5259
They all talked rather harshly , in the kind of voice that suggested they were plotting to knock someone down .
Highlight (blue) - PART I > Page 262 · Location 5286
Apparently this was the main purpose of his connection with the old head clerk , because he lost no time in sending his trunk off in secret , and by the following day he was installed in new quarters . He stopped calling the head clerk ‘ Papa ’ and no longer kissed his hand , and as for the wedding , that business simply came to an abrupt end , as if nothing at all had occurred . Nonetheless , whenever Chichikov ran across him , he always shook his hand amiably and invited him to tea , so that the old head clerk , despite his eternal inertness and harsh indifference , on each occasion would shake his head and mutter under his breath : ‘ He took me in , he really took me in , the Devil’s son ! ’
Highlight (blue) - PART I > Page 264 · Location 5315
May the Devil take the disinterestedness and noble - mindedness of these officials ! ’ The petitioner was , of course , right , but on the other hand , there are no bribe - takers now : all the head clerks are the most honest and noble of people , and it’s only the secretaries and copy - clerks who are crooks .
Highlight (blue) - PART I > Page 266 · Location 5341
The officials quickly grasped the temperament and character of the man . All who were under his supervision became ruthless foes of wrongdoing : everywhere , in all matters , they pursued it the way a fisherman , harpoon in hand , pursues some meaty beluga sturgeon , and they pursued it with such success that in short order each of them accumulated several thousand roubles of capital .
Highlight (blue) - PART I > Page 266 · Location 5354
It should be understood that Chichikov was the most fastidious man who had ever existed in this world . Although at first he had to rub elbows with unclean company , still , in his heart he always remained clean , and he liked offices where the writing tables were of lacquered wood and where everything was genteel .
Highlight (blue) - PART I > Page 267 · Location 5357
The reader , I think , will find it pleasant to learn that every two days he changed his linen , and in summer , during hot weather , even daily : any smell in the least unpleasant was sure to offend him .
Highlight (blue) - PART I > Page 267 · Location 5362
He had already began to fill out and develop those rounded and seemly contours in which the reader found him invested on first making his acquaintance , and more than once already , on glancing in the mirror , he had let his thoughts run to many pleasant things – a nice little woman and a nursery – and a smile would follow such thoughts ; but now when he accidentally glimpsed himself in the mirror , he could not help but cry : ‘ Holy Mother of God ! How disgusting I’ve become ! ’ And for a long time thereafter he would not look at himself .
Highlight (blue) - PART I > Page 268 · Location 5386
Even his superiors declared that he was not a human being , but a devil ; he would conduct searches in wheels , carriage shafts , horses ’ ears , and who knows what other places , into which it wouldn’t occur to any author to look and into which only customs inspectors are permitted to look .
Highlight (blue) - PART I > Page 269 · Location 5392
In a very short time Chichikov made life utterly unbearable for smugglers . He was the terror and despair of all the Polish Jews . His honesty and incorruptibility were unassailable , almost unnatural . He did not even amass a tidy little sum from the various goods that were confiscated or from certain small items that were seized , none of which was turned over to the treasury to avoid unnecessary correspondence .
Highlight (blue) - PART I > Page 269 · Location 5398
This bold enterprise held the promise of millions in profits . He had long possessed information about these smugglers , and had even turned down those who had been sent to bribe him , remarking drily , ‘ It’s not yet time . ’ But once he had acquired control over everything , he lost no time in letting the association know , saying , ‘ Now it’s time . ’
Highlight (blue) - PART I > Page 270 · Location 5408
This incident occurred just at the time when Chichikov was serving as a customs inspector . Had he not personally been involved , no Jews in the world could have succeeded in carrying off an enterprise of this sort . After three or four such ovine excursions across the border , both officials ended up with four hundred thousand in capital . Chichikov , they say , even topped five hundred thousand , because he was a bit quicker on the uptake .
Highlight (blue) - PART I > Page 271 · Location 5433
What he had left was a paltry ten thousand or so , which he had hidden away for a rainy day , and some two dozen shirts of Holland linen , and the modest - size britska that bachelors use for travel , and two serfs : the coachman Selifan and the lackey Petrushka . In addition , the customs officials , out of the goodness of their hearts , had left him five or six cakes of the soap that preserved the freshness of his cheeks – and that was all .
Highlight (blue) - PART I > Page 271 · Location 5436
Such , then , was the position in which our hero once more found himself ! Such was the mountain of calamities that had come toppling down upon his head ! This was what he referred to as ‘ suffering in government service for the truth ’ .
Highlight (blue) - PART I > Page 272 · Location 5445
In a word , he demonstrated a patience compared with which the wooden patience of the German , inherent in the slow , sluggish circulation of his blood , is as nothing .
Highlight (blue) - PART I > Page 273 · Location 5459
Once again he drew himself in like a hedgehog , once again he undertook to lead a life of hardship , once again he stinted himself in everything , once again he descended from cleanliness and a decent position into dirt and a lowly life .
Highlight (blue) - PART I > Page 273 · Location 5464
Among the commissions that came to hand was one in particular : to petition for the mortgaging of several hundred peasants to the Council of Guardians . 12 The property had fallen into utter ruin .
Highlight (blue) - PART I > Page 274 · Location 5472
half the peasants had died off , and so that there would be no awkward questions later on … ‘ Well , are they listed on the census form ? ’ asked the secretary . ‘ They are , ’ replied Chichikov . ‘ Then why be so nervous ? ’ said the secretary . ‘ One dies , another’s born , neither one is worthy of scorn . ’
Highlight (blue) - PART I > Page 274 · Location 5475
‘ Oh , aren’t I a simpleton ! ’ he said to himself . ‘ I’ve been looking for my mittens , when they’re both stuck in my belt ! Why , if I should buy up all of these , the ones that have died off , before new census lists have been sent in , if I should acquire , let’s suppose , a thousand of them , yes , and let’s suppose the Council of Guardians will give me two hundred roubles per soul , that’s two hundred thousand in capital right there !
Highlight (blue) - PART I > Page 274 · Location 5485
True enough , without land you can’t buy or mortgage them . Well , I’ll buy them for resettlement , yes , for resettlement . These days land in Tauris13 and Kherson Provinces is being given away for nothing , as long as you settle there .
Highlight (blue) - PART I > Page 276 · Location 5508
How the first purchases were made the reader has already seen , how things will proceed from this point on , what successes and failures the hero will experience , how he will have to puzzle out and overcome more difficult obstacles , how colossal images will appear , how the hidden levers of a far - reaching tale will move , how its horizons will open ever wider and the whole tale take on a majestic lyrical flow , the reader will see all in good time . Still long is the path that must be traversed by this whole travelling company , which consists of a gentleman of middling years , a carriage of the kind in which bachelors ride , the lackey Petrushka , the coachman Selifan and a troika of horses , who are already familiar by name , from Assessor to the dappled rogue .
Highlight (blue) - PART I > Page 276 · Location 5517
It would be most accurate to call him a proprietor , an acquirer . Acquisitiveness is to blame for everything ; because of it , things have been done which the world terms ‘ not very clean ’ .
Highlight (blue) - PART I > Page 276 · Location 5521
But wise is he who does not disdain any character , but instead fixes a searching eye on him and tries to determine the first causes of his being . Everything undergoes a rapid transformation in man .
Highlight (blue) - PART I > Page 276 · Location 5523
And more than once has it happened that not only an all - enveloping passion , but an insignificant little itch for something trivial has burgeoned in a man born for better deeds , compelling him to forget great and holy obligations and to see the great and the holy in worthless trinkets .
Highlight (blue) - PART I > Page 277 · Location 5525
Numberless as the sands of the sea are the passions of man , and none is like any other , and all of them , the base and the beautiful , in the beginning are submissive to man , and only later do they establish a terrible tyranny over him .
Highlight (blue) - PART I > Page 277 · Location 5527
Blessed is he who from all of these has chosen the most beautiful passion ; with every passing hour and minute his boundless bliss increases and multiplies tenfold , and deeply and ever more deeply does he enter into the infinite paradise of his soul . But there are passions that are not of man’s choosing . They have already been born within him at the moment of his birth into the world , and he is not given the strength to deny them . By higher designs are they directed , and in them lies something that calls eternally , something that never falls silent his whole life long .
Highlight (blue) - PART I > Page 277 · Location 5532
And it may be that in this very same Chichikov the passion that draws him on is no longer of his choosing , and that lodged in his cold existence is that which will later cast man on to his knees and into the dust before the wisdom of the heavens . And it remains a mystery why this image has emerged in the poem that is now making its appearance into the world .
Highlight (blue) - PART I > Page 277 · Location 5535
What weighs on me , however , is not that people will be dissatisfied with the hero , but that in my soul lives the unshakable conviction that readers might have been satisfied with the very same hero , the very same Chichikov , if the author had not looked so deeply into his soul , had not stirred up at its very bottom that which slips away and hides itself from the light , had not exposed his most secret thoughts , which no man confides to any another .
Highlight (blue) - PART I > Page 278 · Location 5546
And so the money that would have put things right is spent on various means of inducing self - oblivion . The mind that might have come upon a sudden fountainhead of great resources is asleep ; and there goes the estate , bang ! auctioned off . And the landowner sets out into the world , a beggar in search of oblivion , his soul ready , in its extremity , for any vile deeds from which he would once have recoiled in horror .
Highlight (blue) - PART I > Page 278 · Location 5549
Censure will also rain down upon the author from the camp of the so - called patriots , who quietly sit in their corners and busy themselves with completely irrelevant matters , amassing small fortunes as they shape their own destinies at the expense of others .
Highlight (blue) - PART I > Page 280 · Location 5579
Thus passed the lives of two ordinary citizens in a peaceful little nook , who unexpectedly , as from a small window , have peeked out at the end of our big poem , peeked out for the purpose of providing a modest answer to the accusation on the part of certain ardent patriots , who until now have been quietly busying themselves with some philosophy or other , or with adding to their wealth at the expense of the finances of the fatherland so tenderly beloved by them , who are not thinking about not doing wrong , but thinking only that people should not say that they are doing wrong .
Highlight (blue) - PART I > Page 280 · Location 5585
You fear the deep - penetrating gaze , you yourself are afraid to fix a deep - penetrating gaze on anything , you like to skim over everything with unthinking eyes . You will even have a hearty laugh at Chichikov , perhaps you will even praise the author , you will say : ‘ Still and all , he’s been good at spotting a thing or two , he must be a jolly sort of fellow ! ’ And after these words you will turn to yourself with redoubled pride , a self - satisfied smile will appear on your face , and you will add : ‘ Really , one must agree that there are very strange and very amusing people in certain provinces , and no small number of scoundrels too ! ’
Highlight (blue) - PART I > Page 280 · Location 5589
But who among you , filled with Christian humility , not publicly but silently , alone , at moments of solitary converse with yourself , will direct this weighty question into the deepest recesses of your own soul : ‘ And isn’t there something of Chichikov in me too ? ’
Highlight (blue) - PART I > Page 281 · Location 5602
And indeed , by now Selifan had been driving for quite some time with his eyes closed , and , in his half - awake state , gave the the reins only an occasional shake over the flanks of the horses , who were also dozing .
Highlight (blue) - PART I > Page 282 · Location 5612
and everything is flying : verst - posts are flying , merchants on the seats of their covered carts are flying towards you , the forest is flying by on either side , with its dark stands of firs and pines , its ringing axe and cawing crow , the whole road is flying who knows where , into the vanishing distance , and something dread lies within all this fleet flashing by , where a vanishing object has no time to assume firm form ; only the sky overhead , and the light clouds , and the moon breaking through them , only they seem motionless .
Highlight (blue) - PART I > Page 282 · Location 5624
Art not thou too , O Rus , rushing onwards like a spirited troika that none can overtake ? Smoking like smoke under you is the road , thundering are the bridges , all falls back and is left behind . The onlooker comes to a stop , struck by the divine miracle : is this not a lightning bolt flung down from heaven ? What is the meaning of this awe - inspiring movement ? And what manner of unknown power is contained within these steeds , who are unknown to the world ? Eh , steeds , steeds , what manner of steeds ! Do whirlwinds nest in your manes ? Does a keen ear burn in your every fibre ? They have heard from on high19 the familiar song , and at once as one they have strained their bronze chests , and barely touching the earth with their hooves , all are transformed into long straight lines that fly through the air , and on rushes the troika , all - inspired by God ! Rus , whither art thou racing ? Give an answer . She gives no answer . The bells set up a wondrous jingling : rent to shreds , the air thunders and is transformed into wind : all that exists on earth flies by , and , looking askance , other peoples and nations step aside and make way for her .
Highlight (blue) - PART II > Page 289 · Location 5680
But to speak impartially : he was not a bad person , he was simply a star - gazer . Since there is already no shortage of people in this wide world of ours who are star - gazers , then why shouldn’t Tentetnikov be one too ? However , here is an instance taken from one day in his life , a day that in every respect was like all the others .
Highlight (blue) - PART II > Page 290 · Location 5691
To begin with , Grigory , a house serf doing duty as pantryman , would be bellowing at Perfilyevna , the housekeeper , in something along the following lines :
Highlight (blue) - PART II > Page 291 · Location 5701
To complete the bedlam , a house serf’s little brat was squalling his lungs out after being whacked by his mother , a borzoi hound was sitting on its haunches and squealing after being doused with boiling water by the the cook , who had peered out of the kitchen . In a word , all were screaming and yelling unbearably . The master went on seeing and hearing . And only when everything grew so intolerable that it even prevented anyone from doing any work did he send someone out to tell them to make noise more quietly .
Highlight (blue) - PART II > Page 291 · Location 5704
Two hours before the midday meal he would withdraw to his study to take up a serious piece of writing . It was supposed to cover all of Russia from every angle – civic , political , religious , philosophical , resolving the thorny problems and questions she faced at the present time , and defining her great future clearly – in a word , putting everything in the manner and form in which the man of today likes to pose such questions .
Highlight (blue) - PART II > Page 291 · Location 5707
However , this colossal undertaking was mostly confined to cogitation . The quill would be gnawed to bits , doodles would appear on the paper , and then it all would be pushed aside , and instead a book would be taken to hand and then not put down until just before dinner .
Highlight (blue) - PART II > Page 291 · Location 5711
but precisely what was done after that until just before supper is truly difficult to say . It would seem , simply , that nothing was done .
Highlight (blue) - PART II > Page 291 · Location 5712
And thus it was that this young thirty - two - year - old man passed the time , alone as alone could be in this world , sitting around the house in a dressing gown and without a cravat . He was not up to taking a stroll or a walk , he did not even feel like going upstairs , he did not even feel like opening the windows to admit some fresh air into the room , and the attractive view of the estate , which no visitor could admire with indifference , might as well not have existed for the proprietor himself .
Highlight (blue) - PART II > Page 292 · Location 5716
From all this the reader can see that Andrey Ivanovich Tentet - nikov belonged to that species of people who are in no danger of becoming extinct in Russia , and who formerly bore such names as sluggards , lieabouts and couch - warmers , but who now should be called I really don’t know what .
Highlight (blue) - PART II > Page 293 · Location 5732
There were many pranks that he did not try to suppress , seeing in them the beginning of character development , and saying that they were as necessary to him as rashes to a doctor – to ascertain precisely what lay within a person .
Highlight (blue) - PART II > Page 293 · Location 5734
No – not even in the mad years of mad infatuations is unquenchable passion as strong as was their love for him .
Highlight (blue) - PART II > Page 293 · Location 5739
Only here did he demand of his pupil everything that others inadvisedly demand of young children – that high - mindedness which is capable of refraining from mockery but enduring every mockery , of putting up with fools and not becoming irritated , of not losing one’s temper and in no case taking revenge , and of preserving the proud serenity of an unruffled heart . Everything that was capable of forming a person into a man of substance was put into practice , and he conducted endless experiments with them . Oh , how well he knew the science of life !
Highlight (blue) - PART II > Page 294 · Location 5754
Once in the service of the state , they held their own in the shakiest positions , while many men far more intelligent than they could not persevere because of petty situations that were personally unpleasant , and threw it all over , or , sinking into apathy , sloth and dullness of mind , let themselves go and ended up in the clutches of bribe - takers and swindlers . But his special pupils remained steadfast , and , with their knowledge of both life and human beings , and made wise in the ways of wisdom , they exerted a powerful influence even on evil people .
Highlight (blue) - PART II > Page 295 · Location 5765
Strangely enough , good deportment was precisely what Fyodor Ivanovich failed to secure . Mischief - making sprang up in secret . During the day everyone stood to attention and marched two - by - two , but at night things ran riot .
Highlight (blue) - PART II > Page 295 · Location 5777
His ambition had already been awakened , but there was no outlet or area of endeavour for it . Better had it not been awakened at all .
Highlight (blue) - PART II > Page 296 · Location 5782
Thanks to his innate intelligence , he sensed only that this was not the way things should be taught ; but how they should be taught he did not know . And often he called Aleksandr Petrovich to mind , and he would feel so sad that he did not know where to turn to escape his melancholy .
Highlight (blue) - PART II > Page 296 · Location 5784
But youth is fortunate in that it has a future .
Highlight (blue) - PART II > Page 296 · Location 5789
Andrey Ivanovich’s ambitious striving for achievement , however , was nipped in the bud from the very outset by his uncle , Actual State Councillor Onufry Ivanovich . He declared that the main thing was good handwriting , and that one had to begin with the study of calligraphy .
Highlight (blue) - PART II > Page 297 · Location 5811
Soon Tentetnikov grew accustomed to his work , except that it did not become his primary concern and goal , as he had at first supposed it would , but something secondary . For him it served as a way of dividing up his time , compelling him to treasure the remaining moments even more .
Highlight (blue) - PART II > Page 298 · Location 5815
Among Andrey Ivanovich’s friends , of whom he had a goodly number , two proved to be what is called embittered people . They were the kind of restless , strange characters who cannot countenance with indifference not only injustices , but anything that even has the appearance of an injustice in their eyes . Fundamentally kind - hearted , but undisciplined in their actions , demanding indulgence towards themselves and at the same time filled with intolerance towards others , they exercised a powerful influence on him through their impassioned way of speaking and the manner in which they demonstrated their noble indignation against society .
Highlight (blue) - PART II > Page 299 · Location 5844
But the uncle’s attempts at persuasion had no effect on the nephew . The countryside was beginning to figure in his mind as a haven of freedom , a nurturing mother of thoughts and ideas , the only arena for useful activity .
Highlight (blue) - PART II > Page 300 · Location 5861
words : ‘ Well , haven’t I been a fool until now ? Fate appointed me to possess an earthly paradise , but I sold myself into bondage as a scribbler of dead papers . After studying , receiving an education , becoming cultivated , amassing a fund of knowledge necessary for the dissemination of good among those subordinate to me , and for the betterment of the entire region , for the implementation of the many and diverse obligations of a landowner , who at one and the same time is both a judge and an organizer , and a maintainer of order – to entrust this position to some ignoramus of a manager , to prefer dealing by proxy with the affairs of people I have never laid eyes on , and of whose character and qualities I have no knowledge , to prefer to real management that fantastic , paper management of provinces thousands of versts away , in which I have never set foot and where the only thing I could achieve would be countless absurdities and stupidities . ’
Highlight (blue) - PART II > Page 301 · Location 5873
And he began to take charge and organize things . He cut back the amount of obligatory labour , reduced the number of workdays the muzhiks owed the landowner and increased the amount of time they could work for themselves .
Highlight (blue) - PART II > Page 301 · Location 5879
The result was not so much that the master and the peasants somehow failed utterly to understand each other but that they were simply singing different tunes , unable to find a way of hitting one and the same note .
Highlight (blue) - PART II > Page 302 · Location 5892
That was strange . He had completely done away with all contributions of linen , berries , mushrooms and nuts , and had exempted them from half their other work , thinking that the women would apply that time to household chores , making clothes for their husbands , increasing the number of vegetable gardens . Nothing of the kind . Idleness , brawling , backbiting and quarrelling over every little thing ran rampant among the fair sex , so much so that their husbands were forever coming to him and saying things like : ‘ Master , keep this demon of a woman quiet . She’s like the Devil himself – don’t give you no peace . ’ Steeling himself , he fully intended to take stern measures .
Highlight (blue) - PART II > Page 303 · Location 5903
A school indeed ! And no one had any time for it : a boy , from the age of ten on , was already helping out with all the work , and that was where he got his schooling .
Highlight (blue) - PART II > Page 303 · Location 5904
In judicial and investigative matters , all those fine points of the law to which his philosophically minded professors had steered him proved utterly useless . Now one party would lie , and the other would lie , and only the Devil could figure it all out . And he saw that a simple knowledge of human beings was more necessary than the fine points in books on law and philosophy ; and he saw that something was lacking in him , but what , God only knew .
Highlight (blue) - PART II > Page 304 · Location 5915
Or else , with eyes firmly shut , and head thrown back towards the expanses of heaven , he would allow his sense of smell to drink in the aroma of the fields , and his hearing to marvel at the voices of the singing denizens of the air , when from all sides , from the heavens and from the earth , they joined together in one harmonious choir , without a single false note .
Highlight (blue) - PART II > Page 304 · Location 5921
highroads and towns . But even this began to bore him . Soon he stopped going into the fields altogether , ensconced himself in his rooms and refused to receive his steward even when he was bringing reports .
Highlight (blue) - PART II > Page 305 · Location 5934
The way in which this work was being pondered , the reader has already seen . A strange , disordered order was established . It cannot be said , however , that there were not moments when he seemed to awaken from his sleep .
Highlight (blue) - PART II > Page 305 · Location 5940
What was the significance of this sobbing ? Was it the means by which an ailing soul vented the doleful secret of its ailment – that the noble inner man which had begun to form within him had not succeeded in developing and maturing ; that , untested from his youth by a struggle with failure , he had not attained to that lofty state of rising above obstacles and impediments and taking strength from them ; that , though molten like metal put to the fire , his rich reserve of lofty feelings had not received a final tempering ; that his extraordinary mentor had died too soon for him , that now there was no one in the whole world who had the power to rouse his forces , weakened as they were by constant vacillating , and his impotent will , which was lacking in resiliency , no one who could cry out to his soul in a stirring cry the heartening word ‘ Onwards ! ’ for which the Russian of all classes and callings and occupations yearns , whatever the rung on which he stands .
Highlight (blue) - PART II > Page 306 · Location 5947
Where , then , is that man who in the native language of our Russian soul might be able to speak this all - powerful word ‘ Onwards ’ to us ? Who , acquainted with all the powers and properties , with all the depths of our nature , might , with a single magical wave of his hand , be able to point us towards a higher life ? With what tears , with what love would the grateful Russian repay him ! But age after age passes , all is enmeshed in the shameful sloth and mindless activity of callow youth [ … ] and no man capable of uttering this word has been sent by God !
Highlight (blue) - PART II > Page 307 · Location 5963
There was something impulsive about her . Whenever she spoke , everything in her seemed to rush after her thoughts – the expression of her face , the tone of her voice , the movement of her hands . The very folds of her dress seemed to fly impulsively in the same direction , and she herself looked as if she would fly off at any moment after her own words .
Highlight (blue) - PART II > Page 307 · Location 5968
Anyone with a glib and bold tongue would be at a loss for words and would grow flustered . But a shy person could converse with her as he had never in his life done with anyone else , and from the very beginning of their conversation , it seemed to him that he had known her once before , somewhere and at some time , and had seen those very features before , perhaps in the days of immemorial childhood , perhaps in his parents ’ house , on some festive evening when a crowd of children was happily playing games , and for a long time thereafter the years of discretion would seem boring to him .
Highlight (blue) - PART II > Page 308 · Location 5983
‘ I thank you , General , for your kindly disposition toward me . By addressing me in such a familiar manner , you call upon me to enter into a close friendship , which obligates me in turn to address you in a familiar manner . But the difference in years constitutes an impediment to such familiar intercourse between us . ’ The General was flustered . Collecting his words and his thoughts , he started to say , albeit somewhat incoherently , that the familiarity had not meant what Tentetnikov thought it did , that sometimes it was permissible for an old man to address a young man in that manner ( about his own rank he did not utter a word ) .
Highlight (blue) - PART II > Page 308 · Location 5989
Everything turned Tentetnikov to the kind of life that the reader has seen at the beginning of the chapter – lying about and doing nothing . Filth and disorder began to reign in the house . The floor brush would be left for days on end in the middle of the room , along with the rubbish . His pantaloons even found their way into the parlour . On the elegant table in front of the sofa lay a pair of greasy braces , as if they had been set out as refreshment for a guest . And his life became so trivial and somnolent that not only did his house servants cease to respect him , but the hens all but pecked at him . Taking up his quill , he would spend hours at a time mindlessly drawing little curlicues , houses , huts , carts , troikas on paper . But sometimes , forgetting everything , the quill would draw all on its own , without its wielder’s being aware , a tiny head with fine features , with a quick penetrating glance and an upswept lock of hair , and the wielder would be astonished to see emerging before his eyes a portrait that would have eluded the brush of even an eminent artist . And he grew even sadder , and , convinced that there would be no happiness on earth , he would be even more bored and depressed thereafter .
Highlight (blue) - PART II > Page 309 · Location 5999
In the gateway appeared steeds , point - for - point as they are sculpted or painted on triumphal arches : one head to the right , one head to the left , one head in the middle . Above them , on the box , a coachman and a lackey in a roomy frock - coat , belted with a handkerchief ; behind them , a gentleman in a cap and greatcoat , muffled in a scarf of rainbow colours . When the vehicle wheeled about in front of the porch , it proved to be nothing more than a light britska on springs . The gentleman , who was of an unusually respectable appearance , jumped out on to the porch with the briskness and adroitness almost of a military man .
Highlight (blue) - PART II > Page 309 · Location 6009
Tentetnikov was drawn into this society by two acquaintances who belonged to the category of embittered people , people who are kind - hearted , but who , from frequent toasts raised in the name of science , enlightenment and future service to humanity , had subsequently become out - and - out drunkards .
Highlight (blue) - PART II > Page 311 · Location 6029
He mentioned that he had had to move from post to post many a time , that he had suffered a great deal for the truth , that even his very life had been in danger more than once at the hands of his enemies ; and he related much else besides , of the kind of thing that revealed a more practical man within .
Highlight (blue) - PART II > Page 312 · Location 6047
But first it is essential to know that in this room stood three tables : one for writing , in front of the sofa ; another for card - playing , between the windows in front of the mirror ; the third a corner table , between the door to the bedroom and the door to an unused area containing disabled furniture , which now served as an ante - room , into which no one until this point had ventured for about a year .
Highlight (blue) - PART II > Page 312 · Location 6058
Everything had acquired a look of unusual cleanliness and tidiness . Not a scrap of paper , or a feather , or a speck of dirt was anywhere to be seen . The very air had somehow been ennobled : the pleasant smell of a healthy , fresh man , who does not wear his linen too long , goes to the bathhouse and wipes himself down with a wet sponge on Sundays , had established itself solidly . In the ante - room the smell of the servant Petrushka had made some attempt at establishing itself , but Petrushka was soon moved to the kitchen , as was proper .
Highlight (blue) - PART II > Page 313 · Location 6070
For example , he would take a black - and - silver snuff - box out of his pocket and , holding it firmly between two fingers of his left hand , set it spinning rapidly with one finger of his right hand , similar to the way in which the earth’s sphere revolves on its axis , or else he would drum a finger on it , while whistling an accompaniment .
Highlight (blue) - PART II > Page 314 · Location 6081
Swarms of midges and clusters of insects appeared on the marshes ; the water spider ran after them in hot pursuit , and after it every kind of bird flocked to the dry reeds from all directions . And all creatures came together to have a closer look at one another . Suddenly the earth was populated , the forests and meadows awoke . Round dancing began in the village . There was ample room for revelry . So bright the green ! So fresh the air ! So murmurous the birds in the orchards ! Paradise , joy and exultation everywhere ! The village rang and sang as if at a wedding .
Highlight (blue) - PART II > Page 315 · Location 6100
He pictured the younger generation too , whose duty it was to perpetuate the Chichikov name : an imp of a little boy and a pretty little daughter , or even two lads , two and even three adorable little daughters , so that everyone should know that he had really lived and existed , and had not passed over the earth like some shadow or spectre , so that he would feel no shame before his fatherland either .
Highlight (blue) - PART II > Page 317 · Location 6132
While engaging in chitchat with the house serfs , as he oftentimes did , he managed to find out , in passing , that the master used to pay rather frequent visits to his neighbour the General , that living in the General’s house was a young lady , that the master was sweet on the young lady and that the young lady also felt the same way about the master … but then suddenly , for some reason , they had a falling out and went their separate ways . He himself had noticed that Andrey Ivanovich kept doodling little heads , each one like the next , in pencil and pen . On one occasion , after dinner , as he engaged in his usual pastime of twirling the silver snuff - box on its axis with his finger , he said the following : ‘ You have everything , Andrey Ivanovich , there’s only one thing that’s missing . ’
Highlight (blue) - PART II > Page 318 · Location 6158
‘ That’s just a habit of generals , it’s not an action ; they address everyone in a familiar way . And besides , why not go ahead and make allowance for a distinguished and honourable man ? ’ ‘ That’s a different matter , ’ said Tentetnikov . ‘ If he had been an old man , a poor man , not proud , not boastful , not a general , then I would have allowed him to address me in a familiar way and I would even have taken it as an honour . ’
Highlight (blue) - PART II > Page 320 · Location 6188
One moment he would sit down on the sofa , the next he would get up and go to the window , the next he would pick up a book , the next he would be trying to think . A futile hope ! No thought would enter his head . Then he attempted not to think about anything – a futile attempt ! Scraps of something resembling thoughts , the tags and tail - ends of thoughts turned up from here , there and everywhere , and started pecking their way into his head . ‘ A strange state ! ’ he said , and went again to the window to look at the road , which cut through the oak grove , at the end of which still hung a cloud of dust which had not yet had time to settle . But , leaving Tentetnikov , let us follow Chichikov .
Highlight (yellow) - PART II > Page 321 · Location 6200
The air everywhere reeked of oil paint , which was renewing everything and not allowing anything to age .
Highlight (yellow) - PART II > Page 322 · Location 6214
He liked to shine , and also liked to know things other people did not know , and did not like people who knew something he did not know ; in a word , he was fond of boasting a little about his intellect .
Highlight (yellow) - PART II > Page 322 · Location 6220
From his voice to the slightest movement of his body , everything about him was dominating , commanding , inspiring if not respect in those of lower rank , then at least timidity .
Highlight (yellow) - PART II > Page 324 · Location 6244
‘ What do you mean , generals ? What generals ? ’ ‘ Generals in general , Your Excellency , in their generality . That is , strictly speaking , generals of the fatherland . ’
Highlight (yellow) - PART II > Page 325 · Location 6257
If a transparent picture , illuminated from behind by powerful lamps , had suddenly flared in a dark room , it would not have proved as startling in the suddenness of its appearance as this small figure , which revealed itself as though expressly to light up the room .
Highlight (yellow) - PART II > Page 326 · Location 6284
‘ Everyone needs to be loved , miss , ’ said Chichikov . ‘ That’s the way things are . Even an animal loves to be stroked . That’s why it sticks its muzzle out of its stall : Go on , stroke me . ’ The General burst
Highlight (yellow) - PART II > Page 334 · Location 6410
‘ No such luck . You’ve come not to his place but to mine . Pyotr Petrovich Petukh . 5 Petukh , Pyotr Petrovich , ’ the host repeated .
Highlight (yellow) - PART II > Page 336 · Location 6448
whoppers ! ’ ‘ It’s annoying even to listen to you .
Highlight (yellow) - PART II > Page 336 · Location 6450
‘ The point of being bored ? Because everything is boring . ’
Highlight (yellow) - PART II > Page 341 · Location 6533
Platonov alone thought : ‘ What’s so good about this mournful song ? It disposes the soul to even greater boredom . ’
"""

##notes = GetNotes(sample_text)
##note_iterator = notes.return_iterator()
##x = note_iterator()
##
##while True:
##    print (next(x))
##    input()
##    


