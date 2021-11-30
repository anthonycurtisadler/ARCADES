class GetNotes:

    def __init__ (self,text):

        self.text = text
        
        self.break_mark = '/###/'
        self.size = 0
        self.qualities = {}


    def load (self,term,head,tail):

        self.qualities[term] = (head,tail)

    def set_divider (self,divider):
        self.divider = divider
        
    def set_split (self,split):
        self.split = split

    def set_for_kindle (self):
            

            self.qualities['highlightcolor'] =  ('(',')')
            self.qualities['part'] = ('PART','>')
            self.qualities['page'] = ('Page','·')
            self.qualities['chapter'] = ('- ',' >')
            self.qualities['location'] = ('Location','XX')
            self.divider='Highlight'
            self.split='\n'
            self.note='NOTE'


    def return_iterator (self):

        def get_between (x,y,z):
            try:
                return x.split(y)[1].split(z)[0].strip()
            except:
                return ''

        def structured_output(phrase):

            return_dict = {}

            lines = phrase.split(self.split)
            head = lines[0]
            text = self.split.join(lines[1:])
            note = ''
            if self.note in text:
                #Get the note portion 
                text_temp = text.split(self.note)[0]
                note = text.split(self.note)[1]
                text = text_temp
            return_dict['NOTE'] = note
            return_dict['TEXT'] = text

            for qual in self.qualities:
                x = get_between(head,self.qualities[qual][0],self.qualities[qual][1])
                if x:
                    return_dict[qual] = x
            

            

            return return_dict
        
        
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
Highlight (yellow) - I > Page 27 · Location 460
‘ Yes , yes , how did it go ? ’ he thought , recalling his dream . ‘ How did it go ? Yes ! Alabin was giving a dinner in Darmstadt - no , not in Darmstadt but something American . Yes , but this Darmstadt was in America . Yes , Alabin was giving a dinner on glass tables , yes - and the tables were singing Il mio tesoro , 1 only it wasn’t Il mio tesoro but something better , and there were some little carafes , which were also women , ’ he recalled .
Note - I > Page 27 · Location 463
Dream
Highlight (yellow) - I > Page 27 · Location 464
‘ Yes , it was nice , very nice . There were many other excellent things there , but one can’t say it in words , or even put it into waking thoughts . ’
Highlight (yellow) - I > Page 27 · Location 468
And here he suddenly remembered how and why he was sleeping not in his wife’s bedroom but in his study : the smile vanished from his face , and he knitted his brows .
Highlight (yellow) - I > Page 28 · Location 480
What had happened to him at that moment was what happens to people when they are unexpectedly caught in something very shameful . He had not managed to prepare his face for the position he found himself in with regard to his wife now that his guilt had been revealed . Instead of being offended , of denying , justifying , asking forgiveness , even remaining indifferent - any of which would have been better than what he did ! - his face quite involuntarily ( ‘ reflexes of the brain ’ , thought Stepan Arkadyich , who liked physiology ) 2 smiled all at once its habitual , kind and therefore stupid smile .
Highlight (yellow) - II > Page 29 · Location 491
He could not now be repentant that he , a thirty - four - year - old , handsome , amorous man , did not feel amorous with his wife , the mother of five living and two dead children , who was only a year younger than he . He repented only that he had not managed to conceal things better from her .
Highlight (yellow) - II > Page 29 · Location 496
It even seemed to him that she , a worn - out , aged , no longer beautiful woman , not remarkable for anything , simple , merely a kind mother of a family , ought in all fairness to be indulgent . It turned out to be quite the opposite .
Highlight (yellow) - II > Page 29 · Location 503
There was no answer , except the general answer life gives to all the most complex and insoluble questions . That answer is : one must live for the needs of the day , in other words , become oblivious . To become oblivious in dreams was impossible now , at least till night - time ; it was impossible to return to that music sung by carafe - women ; and so one had to become oblivious in the dream of life .
Highlight (yellow) - II > Page 31 · Location 549
Matvei was already holding the shirt like a horse collar , blowing away something invisible , and with obvious pleasure he clothed the pampered body of his master in it .
Highlight (yellow) - III > Page 32 · Location 558
And the thought that he might be guided by those interests , that he might seek a reconciliation with his wife in order to sell the wood , was offensive to him .
Highlight (yellow) - III > Page 32 · Location 561
Stepan Arkadyich subscribed to and read a liberal newspaper , 3 not an extreme one , but one with the tendency to which the majority held . And though neither science , nor art , nor politics itself interested him , he firmly held the same views on all these subjects as the majority and his newspaper did , and changed them only when the majority did , or , rather , he did not change them , but they themselves changed imperceptibly in him .
Highlight (yellow) - III > Page 32 · Location 566
And for him , who lived in a certain circle , and who required some mental activity such as usually develops with maturity , having views was as necessary as having a hat . If there was a reason why he preferred the liberal tendency to the conservative one ( also held to by many in his circle ) , it was not because he found the liberal tendency more sensible , but because it more closely suited his manner of life . The liberal party said that everything was bad in Russia , and indeed Stepan Arkadyich had many debts and decidedly too little money . The liberal party said that marriage was an obsolete institution and was in need of reform , and indeed family life gave Stepan Arkadyich little pleasure and forced him to lie and pretend , which was so contrary to his nature . The liberal party said , or , rather , implied , that religion was just a bridle for the barbarous part of the population , and indeed Stepan Arkadyich could not even stand through a short prayer service without aching feet and could not grasp the point of all these fearsome and high - flown words about the other world , when life in this one could be so merry .
Highlight (yellow) - III > Page 32 · Location 576
And so the liberal tendency became a habit with Stepan Arkadyich , and he liked his newspaper , as he liked a cigar after dinner , for the slight haze it produced in his head .
Highlight (yellow) - III > Page 33 · Location 591
‘ I told you not to put passengers on the roof , ’ the girl shouted in English . ‘ Now pick it up ! ’
Highlight (yellow) - III > Page 33 · Location 599
He was aware that he loved the boy less , and always tried to be fair ; but the boy felt it and did not respond with a smile to the cold smile of his father .
Highlight (yellow) - III > Page 34 · Location 619
Having dismissed the captain’s wife , Stepan Arkadyich picked up his hat and paused , wondering whether he had forgotten anything . It turned out that he had forgotten nothing , except what he had wanted to forget - his wife .
Highlight (yellow) - III > Page 34 · Location 621
‘ Ah , yes ! ’ He hung his head , and his handsome face assumed a wistful expression . ‘ Shall I go or not ? ’ he said to himself . And his inner voice told him that he should not go , that there could be nothing here but falseness , that to rectify , to repair , their relations was impossible , because it was impossible to make her attractive and arousing of love again or to make him an old man incapable of love . Nothing could come of it now but falseness and deceit , and falseness and deceit were contrary to his nature .
Highlight (yellow) - IV > Page 35 · Location 643
She gave his figure radiating freshness and health a quick glance up and down . ‘ Yes , he’s happy and content ! ’ she thought , ‘ while I . . . ? And this repulsive kindness everyone loves and praises him for - I hate this kindness of his . ’ She pressed her lips together ; the cheek muscle on the right side of her pale , nervous face began to twitch .
Highlight (yellow) - IV > Page 37 · Location 691
It was Friday and the German clockmaker was winding the clock in the dining room . Stepan Arkadyich remembered his joke about this punctilious , bald - headed man , that the German ‘ had been wound up for life himself , so as to keep winding clocks ’ - and smiled . Stepan Arkadyich loved a good joke . ‘ But maybe it will shape up ! A nice little phrase : shape up , ’ he thought . ‘ It bears repeating . ’
Highlight (yellow) - V > Page 39 · Location 734
The main qualities that had earned him this universal respect in the service were , first , an extreme indulgence towards people , based on his awareness of his own shortcomings ; second , a perfect liberalism , not the sort he read about in the newspapers , but the sort he had in his blood , which made him treat all people , whatever their rank or status , in a perfectly equal and identical way ; and , third - most important - a perfect indifference to the business he was occupied with , owing to which he never got carried away and never made mistakes .
Highlight (yellow) - V > Page 41 · Location 772
Stepan Arkadyich was on familiar terms with almost all his acquaintances : with old men of sixty and with boys of twenty , with actors , ministers , merchants and imperial adjutants , so that a great many of those who were his intimates occupied opposite ends of the social ladder and would have been very surprised to learn they had something in common through Oblonsky
Highlight (yellow) - V > Page 41 · Location 781
But in spite of that , as often happens between people who have chosen different ways , each of them , while rationally justifying the other’s activity , despised it in his heart . To each of them it seemed that the life he led was the only real life , and the one his friend led was a mere illusion .
Highlight (yellow) - V > Page 42 · Location 813
Levin suddenly blushed , but not as grown - up people blush - slightly , unaware of it themselves - but as boys do , feeling that their bashfulness makes them ridiculous , becoming ashamed as a result , and blushing even more , almost to the point of tears . And it was so strange to see that intelligent , manly face in such a childish state that Oblonsky stopped looking at him .
Highlight (yellow) - V > Page 43 · Location 828
The secretary came in with familiar deference and a certain modest awareness , common to all secretaries , of his superiority to his chief in the knowledge of business , approached Oblonsky with some papers and , in the guise of a question , began explaining some difficulty . Stepan Arkadyich , without listening to the end , placed his hand benignly on the secretary’s sleeve .
Highlight (yellow) - VI > Page 45 · Location 866
Strange as it might seem , Konstantin Levin was in love precisely with the house , the family , especially the female side of it . He did not remember his own mother , and his only sister was older than he , so that in the Shcherbatskys ’ house he saw for the first time the milieu of an old , noble , educated and honourable family , of which he had been deprived by the death of his father and mother .
Highlight (yellow) - VI > Page 45 · Location 875
all this and much more that went on in their mysterious world he did not understand ; but he knew that everything that went on there was beautiful , and he was in love precisely with the mysteriousness of it all .
Highlight (yellow) - VI > Page 46 · Location 889
Levin’s conviction that it could not be rested on the idea that in the eyes of her relatives he was an unprofitable , unworthy match for the charming Kitty , and that Kitty could not love him . In their eyes , though he was now thirty - two , he did not have any regular , defined activity or position in society , whereas among his comrades one was already a colonel and imperial aide - de - camp , one a professor , one the director of a bank and a railway or the chief of an office like Oblonsky , while he ( he knew very well what he must seem like to others ) was a landowner , occupied with breeding cows , shooting snipe , and building things , that is , a giftless fellow who amounted to nothing and was doing , in society’s view , the very thing that good - for - nothing people do .
Highlight (yellow) - VI > Page 46 · Location 898
He had heard that women often love unattractive , simple people , but he did not believe it , because he judged by himself , and he could only love beautiful , mysterious and special women .
Highlight (yellow) - VII > Page 47 · Location 910
The discussion was about a fashionable question : is there a borderline between psychological and physiological phenomena in human activity , and where does it lie ? 12
Highlight (yellow) - VII > Page 47 · Location 916
Levin had come across the articles they were discussing in magazines , and had read them , being interested in them as a development of the bases of natural science , familiar to him from his studies at the university , but he had never brought together these scientific conclusions about the animal origin of man , 13 about reflexes , biology and sociology , with those questions about the meaning of life and death which lately had been coming more and more often to his mind .
Highlight (yellow) - VII > Page 47 · Location 925
‘ I can by no means agree with Keiss that my whole notion of the external world stems from sense impressions . The fundamental concept of being itself is not received through the senses , for there exists no special organ for conveying that concept . ’
Highlight (yellow) - VIII > Page 49 · Location 949
‘ Well , how are things with your zemstvo ? ’ asked Sergei Ivanovich , who was very interested in the zemstvo and ascribed great significance to it .
Highlight (yellow) - VIII > Page 49 · Location 955
‘ But it’s always like that ! ’ Sergei Ivanovich interrupted . ‘ We Russians are always like that . Maybe it’s a good feature of ours - the ability to see our own failings - but we overdo it , we take comfort in irony , which always comes readily to our tongues . I’ll tell you only that if they gave some other European nation the same rights as in our zemstvo institutions - the Germans or the English would have worked their way to freedom with them , while we just laugh . ’
Highlight (yellow) - IX > Page 52 · Location 1019
In this childlike expression of her face combined with the slender beauty of her figure lay her special loveliness , which he remembered well ; but what was always striking in her , like something unexpected , was the look in her eyes - meek , calm and truthful - and especially her smile , which always transported Levin into a magic world where he felt softened and moved to tenderness , as he could remember himself being on rare days in his early childhood .
Highlight (yellow) - IX > Page 52 · Location 1029
‘ Yes , I used to be a passionate skater ; I wanted to achieve perfection . ’ ‘ It seems you do everything passionately , ’ she said , smiling . ‘ I do so want to see you skate . Put on some skates and let’s skate together . ’ ‘ Skate together ! Can it be possible ? ’ thought Levin , looking at her . ‘ I’ll put them on at once , ’ he said . And he went to put on some skates . ‘ You haven’t been here for a long time , sir , ’ said the skating attendant as he supported his foot , tightening the screw on the heel . ‘ There have been no experts among the gentlemen since you left .
Highlight (yellow) - IX > Page 53 · Location 1057
When Levin again raced up to Kitty , her face was no longer stern , the look in her eyes was as truthful and gentle as ever , but it seemed to Levin that her gentleness had a special , deliberately calm tone . And he felt sad . After talking about her old governess and her quirks , she asked him about his life .
Highlight (yellow) - IX > Page 54 · Location 1077
‘ A nice man , a dear man , ’ Kitty thought just then , coming out of the shed with Mlle Linon and looking at him with a smile of gentle tenderness , as at a beloved brother . ‘ And can it be I’m to blame , can it be I did something bad ? Coquettishness , they say . I know it’s not him I love ; but even so , it’s fun to be with him , and he’s so nice . Only why did he say that ? . . . ’ she thought .
Highlight (yellow) - IX > Page 54 · Location 1093
‘ To the Anglia , then , ’ said Stepan Arkadyich , choosing the Anglia because he owed more in the Anglia than in the Hermitage . He therefore considered it not nice to avoid that hotel . ‘ Do you have a cab ? Excellent , because I dismissed my carriage . ’
Highlight (yellow) - X > Page 58 · Location 1157
‘ I can’t help it , ’ replied Levin . ‘ Try getting inside me , look at it from a countryman’s point of view . In the country we try to keep our hands in a condition that makes them convenient to work with ; for that we cut our nails and sometimes roll up our sleeves . While here people purposely let their nails grow as long as they can , and stick on saucers instead of cuff - links , so that it would be impossible for them to do anything with their hands . ’
Note - X > Page 58 · Location 1159
Hand
Highlight (yellow) - X > Page 58 · Location 1161
‘ Yes , it’s a sign that he has no need of crude labour . His mind works . . . ’ ‘ Maybe . But all the same it seems wild to me , just as it seems wild to me that while we countrymen try to eat our fill quickly , so that we can get on with what we have to do , you and I are trying our best not to get full for as long as possible , and for that we eat oysters . . . ’ ‘ Well , of course , ’ Stepan Arkadyich picked up . ‘ But that’s the aim of civilization : to make everything an enjoyment . ’ ‘ Well , if that’s its aim , I’d rather be wild . ’ ‘ You’re wild as it is . All you Levins are wild . ’
Highlight (yellow) - X > Page 59 · Location 1199
Stepan Arkadyich smiled . He knew so well this feeling of Levin‘s , knew that for him all the girls in the world were divided into two sorts : one sort was all the girls in the world except her , and these girls had all human weaknesses and were very ordinary girls ; the other sort was her alone , with no weaknesses and higher than everything human .
Highlight (yellow) - X > Page 60 · Location 1217
‘ Understand , ’ he said , ‘ that it isn’t love . I’ve been in love , but this is not the same . This is not my feeling , but some external force taking possession of me . I left because I decided it could not be , you understand , like a happiness that doesn’t exist on earth ; but I have struggled with myself and I see that without it there is no life . And I must resolve . . . ’
Highlight (yellow) - X > Page 60 · Location 1224
The terrible thing is that we older men , who already have a past . . . not of love , but of sins . . . suddenly become close with a pure , innocent being ; it’s disgusting , and so you can’t help feeling yourself unworthy . ’
Highlight (yellow) - X > Page 60 · Location 1229
‘ There’s one consolation , as in that prayer I’ve always loved , that I may be forgiven not according to my deserts , but out of mercy . That’s also the only way she can forgive me . ’
Highlight (yellow) - XI > Page 62 · Location 1262
‘ Excuse me , but I decidedly do not understand how I . . . just as I don’t understand how I could pass by a bakery , as full as I am now , and steal a sweet roll . ’ Stepan Arkadyich’s eyes shone more than usual . ‘ Why not ? Sometimes a sweet roll is so fragrant that you can’t help yourself .
Highlight (yellow) - XI > Page 62 · Location 1271
‘ Well , you must excuse me . You know , for me all women are divided into two sorts . . . that is , no . . . rather : there are women and there are . . . I’ve never seen and never will see any lovely fallen creatures , 22 and ones like that painted Frenchwoman at the counter , with all those ringlets - they’re vermin for me , and all the fallen ones are the same . ’ ‘ And the one in the Gospels ? ’ ‘ Oh , stop it ! Christ would never have said those words , if he’d known how they would be misused . 23 Those are the only words people remember from all the Gospels . However , I’m not saying what I think but what I feel . I have a loathing for fallen women . You’re afraid of spiders and I of those vermin . You surely have never studied spiders and don’t know their ways : it’s the same with me . ’
Highlight (yellow) - XI > Page 63 · Location 1288
‘ If you want my opinion concerning that , I’ll tell you that I don’t think there is a drama here . And here’s why . To my mind , love . . . the two loves that Plato , remember , defines in his Symposium , 25 these two loves serve as a touchstone for people . Some people understand only the one , others the other . And those who understand only non - platonic love shouldn’t talk about drama . In such love there can be no drama . “ Thank you kindly for the pleasure , with my respects ” - there’s the whole drama . And for platonic love there can be no drama , because in such love everything is clear and pure , because . . . ’
Highlight (yellow) - XI > Page 63 · Location 1295
‘ So you see , ’ said Stepan Arkadyich , ‘ you’re a very wholesome man . That is your virtue and your defect . You have a wholesome character , and you want all of life to be made up of wholesome phenomena , but that doesn’t happen . So you despise the activity of public service because you want things always to correspond to their aim , and that doesn’t happen . You also want the activity of the individual man always to have an aim , that love and family life always be one . And that doesn’t happen . All the variety , all the charm , all the beauty of life are made up of light and shade . ’
Note - XI > Page 63 · Location 1299
Chiarascuro
Highlight (yellow) - XI > Page 63 · Location 1302
Oblonsky had experienced more than once this extreme estrangement instead of closeness that may come after dinner , and knew what had to be done on such occasions .
Highlight (yellow) - XII > Page 64 · Location 1332
At least it seemed so to the princess . But with her own daughters she had experienced how this seemingly ordinary thing - giving away her daughters in marriage - was neither easy nor simple .
Highlight (yellow) - XII > Page 65 · Location 1336
The old prince , like all fathers , was especially scrupulous about the honour and purity of his daughters ; he was unreasonably jealous over them , and especially over Kitty , who was his favourite , and at every step made scenes with his wife for compromising their daughter .
Highlight (yellow) - XII > Page 65 · Location 1340
She saw that girls of Kitty’s age formed some sort of groups , attended some sort of courses , 26 freely associated with men , drove around by themselves , many no longer curtsied , and , worse still , they were all firmly convinced that choosing a husband was their own and not their parents ’ business . ‘ Nowadays girls are not given in marriage as they used to be , ’ all these young girls , and even all the old people , thought and said . But how a girl was to be given in marriage nowadays the princess could not find out from anyone . The French custom - for the parents to decide the children’s fate - was not accepted , and was even condemned . The English custom - giving the girl complete freedom - was also not accepted and was impossible in Russian society . The Russian custom of matchmaking was regarded as something outrageous and was laughed at by everyone , the princess included . But how a girl was to get married or be given in marriage , no one knew .
Highlight (yellow) - XII > Page 65 · Location 1350
And however much the princess was assured that in our time young people themselves must settle their fate , she was unable to believe it , as she would have been unable to believe that in anyone’s time the best toys for five - year - old children would be loaded pistols . And therefore the princess worried more about Kitty than she had about her older daughters .
Highlight (yellow) - XII > Page 66 · Location 1377
The princess was smiling at how immense and significant everything now happening in her soul must seem to the poor dear .
Highlight (yellow) - XIII > Page 67 · Location 1385
And it was easy for her to recall Levin . But in her recollections of Vronsky there was an admixture of something awkward , though he was in the highest degree a calm and worldly man . It was as if there were some falseness - not in him , he was very simple and nice - but in herself , while with Levin she felt completely simple and clear .
Highlight (yellow) - XIII > Page 68 · Location 1414
She was breathing heavily , not looking at him . She was in ecstasy . Her soul overflowed with happiness . She had never imagined that the voicing of his love would make such a strong impression on her . But this lasted only a moment . She remembered Vronsky . Raising her light , truthful eyes to Levin and seeing his desperate face , she hastily replied :
Highlight (yellow) - XIV > Page 69 · Location 1426
She was a dry , yellow woman , sickly and nervous , with black shining eyes .
Highlight (yellow) - XIV > Page 69 · Location 1432
She was right , because Levin indeed could not stand her and had contempt for what she took pride in and counted as a merit - her nervousness , her refined contempt and disregard for all that was coarse and common .
Highlight (yellow) - XIV > Page 70 · Location 1449
‘ Konstantin Dmitrich , ’ she said to him , ‘ explain to me , please , what it means - you know all about this - that on our Kaluga estate the muzhiks and their women drank up all they had and now don’t pay us anything ? What does it mean ? You praise muzhiks all the time . ’
Highlight (yellow) - XIV > Page 70 · Location 1457
There are people who , on meeting a successful rival in whatever it may be , are ready at once to turn their eyes from everything good in him and to see only the bad ; then there are people who , on the contrary , want most of all to find the qualities in this successful rival that enabled him to defeat them , and with aching hearts seek only the good . Levin was one of those people .
Highlight (yellow) - XIV > Page 71 · Location 1476
‘ No , not if you’re busy and are not bored with your own self , ’ Levin replied curtly .
Highlight (yellow) - XIV > Page 71 · Location 1495
‘ My opinion , ’ answered Levin , ‘ is simply that these turning tables prove that our so - called educated society is no higher than the muzhiks . They believe in the evil eye , and wicked spells , and love potions , while we . . . ’
Highlight (yellow) - XIV > Page 72 · Location 1505
‘ When electricity was found , ’ Levin quickly interrupted , ‘ it was merely the discovery of a phenomenon , and it was not known where it came from or what it could do , and centuries passed before people thought of using it . The spiritualists , on the contrary , began by saying that tables write to them and spirits come to them , and only afterwards started saying it was an unknown force . ’
Highlight (yellow) - XIV > Page 72 · Location 1512
‘ Because , ’ Levin interrupted again , ‘ with electricity , each time you rub resin against wool , a certain phenomenon manifests itself , while here it’s not each time , and therefore it’s not a natural phenomenon . ’
Highlight (yellow) - XIV > Page 72 · Location 1515
‘ Let’s try it now , Countess , ’ he began . But Levin wanted to finish saying what he thought . ‘ I think , ’ he continued , ‘ that this attempt by the spiritualists to explain their wonders by some new force is a most unfortunate one . They speak directly about spiritual force and want to subject it to material experiment . ’
Highlight (yellow) - XIV > Page 72 · Location 1518
They were all waiting for him to finish , and he felt it . ‘ And I think that you’d make an excellent medium , ’ said Countess Nordston , ‘ there’s something ecstatic in you . ’
Highlight (yellow) - XIV > Page 73 · Location 1531
Kitty sensed that , after what had happened , her father’s cordiality would be oppressive for Levin . She also saw how coldly her father finally responded to Vronsky’s bow and how Vronsky looked at her father with friendly perplexity , trying but failing to understand how and why it was possible to have an unfriendly attitude towards him , and she blushed .
Highlight (yellow) - XVI > Page 76 · Location 1592
He did not know that his behaviour towards Kitty had a specific name , that it was the luring of a young lady without the intention of marriage , and that this luring was one of the bad actions common among brilliant young men such as himself . It seemed to him that he was the first to discover this pleasure , and he enjoyed his discovery .
Highlight (yellow) - XVI > Page 76 · Location 1598
Marriage had never presented itself as a possibility to him . He not only did not like family life , but pictured the family , and especially a husband , according to the general view of the bachelor world in which he lived , as something alien , hostile and , above all , ridiculous
Highlight (yellow) - XVI > Page 76 · Location 1603
‘ The charm of it is , ’ he thought , going home from the Shcherbatskys ’ and bringing with him , as always , a pleasant feeling of purity and freshness , partly because he had not smoked all evening , and together with it a new feeling of tenderness at her love for him , ‘ the charm of it is that nothing was said either by me or by her , yet we understood each other so well in that invisible conversation of eyes and intonations , that tonight she told me more clearly than ever that she loves me . And so sweetly , simply and , above all , trustfully ! I feel better and purer myself . I feel that I have a heart and that there is much good in me . Those sweet , loving eyes ! When she said : “ and very much ” . . .
Highlight (yellow) - XVI > Page 77 · Location 1612
He went straight to his rooms at the Dussot , ordered supper served , after which he got undressed and , the moment his head touched the pillow , fell into a sound and peaceful sleep , as always .
Highlight (yellow) - XVII > Page 78 · Location 1629
‘ I think I do . Or else , no . . . I really can’t remember , ’ Vronsky replied absentmindedly , vaguely picturing to himself at the name Karenina something standoffish and dull .
Highlight (yellow) - XVII > Page 79 · Location 1642
‘ I don’t know why it is , ’ answered Vronsky , ‘ but all Muscovites , naturally excluding those I’m talking with , ’ he added jokingly , ‘ have something edgy about them . They keep rearing up for some reason , getting angry , as if they want to make you feel something
Highlight (yellow) - XVII > Page 79 · Location 1646
The approach of the train was made more and more evident by the preparatory movements in the station , the running of attendants , the appearance of gendarmes and porters , and the arrival of those coming to meet the train . Through the frosty steam , workers in sheepskin jackets and soft felt boots could be seen crossing the curved tracks . The whistle of the engine could be heard down the line , and the movement of something heavy .
Highlight (yellow) - XVII > Page 79 · Location 1658
‘ Really ! . . . I think , however , that she can count on a better match , ’ said Vronsky , and , squaring his shoulders , he resumed his pacing . ‘ However , I don’t know him , ’ he added . ‘ Yes , it’s a painful situation ! That’s why most of us prefer the company of Claras . There failure only proves that you didn’t have enough money , while here - your dignity is at stake . Anyhow , the train’s come . ’
Highlight (yellow) - XVII > Page 80 · Location 1668
Vronsky , standing beside Oblonsky , looked over the carriages and the people getting off and forgot his mother entirely . What he had just learned about Kitty had made him excited and happy . His chest involuntarily swelled and his eyes shone . He felt himself the victor .
Highlight (yellow) - XVII > Page 80 · Location 1671
The conductor’s words woke him up and forced him to remember his mother and the forthcoming meeting with her . In his soul he did not respect her and , without being aware of it , did not love her , though by the notions of the circle in which he lived , by his upbringing , he could not imagine to himself any other relation to his mother than one obedient and deferential in the highest degree , and the more outwardly obedient and deferential he was , the less he respected and loved her in his soul .
Highlight (yellow) - XVIII > Page 81 · Location 1677
He excused himself and was about to enter the carriage , but felt a need to glance at her once more - not because she was very beautiful , not because of the elegance and modest grace that could be seen in her whole figure , but because there was something especially gentle and tender in the expression of her sweet - looking face as she stepped past him . As he looked back , she also turned her head .
Highlight (yellow) - XVIII > Page 82 · Location 1723
Trite as the phrase was , Mme Karenina evidently believed it with all her heart and was glad . She blushed , bent forward slightly , offering her face to the countess’s lips , straightened up again , and with the same smile wavering between her lips and eyes , gave her hand to Vronsky .
Highlight (yellow) - XVIII > Page 82 · Location 1728
Her son was thinking the same . He followed her with his eyes until her graceful figure disappeared , and the smile stayed on his face . Through the window he saw her go up to her brother , put her hand on his arm , and begin animatedly telling him something that obviously had nothing to do with him , Vronsky , and he found that vexing . ‘ Well , so , maman , are you quite well ? ’ he repeated , turning to his mother .
Highlight (yellow) - XVIII > Page 83 · Location 1738
The maid took the bag and the lapdog , the butler and a porter the other bags . Vronsky gave his mother his arm ; but as they were getting out of the carriage , several men with frightened faces suddenly ran past . The stationmaster , in a peaked cap of an extraordinary colour , also ran past . Evidently something extraordinary had happened . People who had left the train were running back . ‘ What ? . . . What ? . . . Where ? . . . Threw himself ! . . . run over ! . . . ’ could be heard among those passing by .
Highlight (yellow) - XVIII > Page 83 · Location 1747
Oblonsky and Vronsky had both seen the mangled corpse . Oblonsky was obviously suffering . He winced and seemed ready to cry . ‘ Ah , how terrible ! Ah , Anna , if you’d seen it ! Ah , how terrible ! ’ he kept saying . Vronsky was silent , and his handsome face was serious but perfectly calm .
Highlight (yellow) - XVIII > Page 83 · Location 1758
They went out together . Vronsky walked ahead with his mother . Behind came Mme Karenina with her brother . At the exit , the stationmaster overtook Vronsky and came up to him . ‘ You gave my assistant two hundred roubles . Would you be so kind as to designate whom they are meant for ? ’ ‘ For the widow , ’ Vronsky said , shrugging his shoulders . ‘ I don’t see any need to ask . ’
Highlight (yellow) - XVIII > Page 84 · Location 1768
Mme Karenina got into the carriage , and Stepan Arkadyich saw with surprise that her lips were trembling and she could hardly keep back her tears . ‘ What is it , Anna ? ’ he asked , when they had driven several hundred yards . ‘ A bad omen , ’ she said .
Highlight (yellow) - XVIII > Page 84 · Location 1774
‘ Oh ? ’ Anna said softly . ‘ Well , now let’s talk about you , ’ she added , tossing her head as if she wanted physically to drive away something superfluous that was bothering her . ‘ Let’s talk about your affairs . I got your letter and here I am . ’
Highlight (yellow) - XIX > Page 85 · Location 1780
When Anna came in , Dolly was sitting in the small drawing room with a plump , tow - headed boy who already resembled his father , listening as he recited a French lesson . The boy was reading , his hand twisting and trying to tear off the barely attached button of his jacket . His mother took his hand away several times , but the plump little hand would take hold of the button again . His mother tore the button off and put it in her pocket .
Note - XIX > Page 85 · Location 1783
Subconscious
Highlight (yellow) - XIX > Page 85 · Location 1789
‘ I know nothing but the very best about her , and with regard to myself , I’ve seen only kindness and friendship from her . ’ True , as far as she could remember her impression of the Karenins ’ house in Petersburg , she had not liked it ; there was something false in the whole shape of their family life .
Highlight (yellow) - XIX > Page 85 · Location 1794
She did not want to talk about her grief , and with this grief in her soul she could not talk about irrelevancies
Highlight (yellow) - XIX > Page 85 · Location 1798
Hearing the rustle of a dress and light footsteps already at the door , she turned , and her careworn face involuntarily expressed not joy but surprise .
Note - XIX > Page 85 · Location 1799
Unconscious
Highlight (yellow) - XIX > Page 87 · Location 1837
‘ And do you think he understands all the horror of my position ? ’ Dolly went on . ‘ Not a bit ! He’s happy and content . ’ ‘ Oh , no ! ’ Anna quickly interrupted . ‘ He’s pitiful , he’s overcome with remorse . . . ’ ‘ Is he capable of remorse ? ’ Dolly interrupted , peering intently into her sister - in - law’s face .
Highlight (yellow) - XIX > Page 87 · Location 1846
For me to live with him now would be torture , precisely because I loved him as I did , because I love my past love for him . . . ’
Highlight (yellow) - XIX > Page 88 · Location 1867
I don’t know . . . I don’t know how much love for him there still is in your soul . Only you know whether it’s enough to be able to forgive . If it is , then forgive him ! ’
Highlight (yellow) - XIX > Page 88 · Location 1870
‘ I know more of the world than you do , ’ she said . ‘ I know how people like Stiva look at it . You say he talked with her about you . That never happened . These people may be unfaithful , but their hearth and wife are sacred to them . Somehow for them these women remain despised and don’t interfere with the family . Between them and the family they draw some sort of line that can’t be crossed . I don’t understand it , but it’s so . ’
Highlight (yellow) - XX > Page 89 · Location 1893
Anna obviously admired her beauty and youth , and before Kitty could recover she felt that she was not only under her influence but in love with her , as young girls are capable of being in love with older married ladies .
Highlight (yellow) - XX > Page 89 · Location 1897
Kitty felt that Anna was perfectly simple and kept nothing hidden , but that there was in her some other , higher world of interests , inaccessible to her , complex and poetic .
Highlight (yellow) - XX > Page 90 · Location 1913
‘ No , dear heart , for me there are no longer any balls that are merry , ’ said Anna , and Kitty saw in her eyes that special world that was not open to her . ‘ For me there are those that are less difficult and boring . . . ’
Highlight (yellow) - XX > Page 90 · Location 1930
‘ Oh ! how good to be your age , ’ Anna went on . ‘ I remember and know that blue mist , the same as in the mountains in Switzerland . The mist that envelops everything during the blissful time when childhood is just coming to an end , and the path away from that vast , cheerful and happy circle grows narrower and narrower , and you feel cheerful and eerie entering that suite of rooms , though it seems bright and beautiful . . . Who hasn’t gone through that ? ’
Highlight (yellow) - XXI > Page 92 · Location 1957
By his tone Kitty and Anna both understood at once that a reconciliation had taken place .
Highlight (yellow) - XXI > Page 92 · Location 1963
‘ I know how you’ll do it , ’ Dolly answered , ‘ you’ll tell Matvei to do something impossible , then you’ll leave , and he’ll get it all wrong ’ - and a habitual mocking smile wrinkled Dolly’s lips as she said it . ‘ Complete , complete reconciliation , complete , ’ thought Anna , ‘ thank God ! ’ and rejoicing that she had been the cause of it , she went over to Dolly and kissed her .
Highlight (yellow) - XXI > Page 92 · Location 1968
All evening , as usual , Dolly was slightly mocking towards her husband , and Stepan Arkadyich was content and cheerful , but just enough so as not to suggest that , having been forgiven , he had forgotten his guilt .
Highlight (yellow) - XXI > Page 92 · Location 1969
At half - past nine an especially joyful and pleasant family conversation around the evening tea table at the Oblonskys ’ was disrupted by an apparently very simple event , but this simple event for some reason seemed strange to everyone .
Highlight (yellow) - XXI > Page 93 · Location 1981
Anna , looking down , at once recognized Vronsky , and a strange feeling of pleasure suddenly stirred in her heart , together with a fear of something .
Highlight (yellow) - XXI > Page 93 · Location 1988
Kitty blushed . She thought that she alone understood why he had called by and why he had not come in . ‘ He was at our house , ’ she thought , ‘ didn’t find me , and thought I was here ; but he didn’t come in because he thought it was late , and Anna’s here . ’
Highlight (yellow) - XXI > Page 93 · Location 1991
There was nothing either extraordinary or strange in a man calling at his friend’s house at half - past nine to find out the details of a dinner that was being planned and not coming in ; but they all thought it strange . To Anna especially it seemed strange and not right .
Highlight (yellow) - XXII > Page 94 · Location 1999
A beardless young man , one of those young men of society whom the old prince Shcherbatsky called twits , wearing an extremely low - cut waistcoat , straightening his white tie as he went , bowed to them and , after running past , came back to invite Kitty to a quadrille .
Highlight (yellow) - XXII > Page 94 · Location 2003
Though Kitty’s toilette , coiffure and all the preparations for the ball had cost her a good deal of trouble and planning , she was now entering the ballroom , in her intricate tulle gown over a pink underskirt , as freely and simply as if all these rosettes and laces , and all the details of her toilette , had not cost her and her household a moment’s attention , as if she had been born in this tulle and lace , with this tall coiffure , topped by a rose with two leaves .
Highlight (yellow) - XXII > Page 94 · Location 2006
When the old princess , at the entrance to the ballroom , wanted to straighten the twisted end of her ribbon sash , Kitty drew back slightly . She felt that everything on her must of itself be good and graceful , and there was no need to straighten anything .
Highlight (yellow) - XXII > Page 94 · Location 2012
This velvet ribbon was enchanting , and at home , as she looked at her neck in the mirror , she felt it could almost speak .
Highlight (yellow) - XXII > Page 95 · Location 2047
But now , seeing her in black , she felt that she had never understood all her loveliness . She saw her now in a completely new and , for her , unexpected way . Now she understood that Anna could not have been in lilac , that her loveliness consisted precisely in always standing out from what she wore , that what she wore was never seen on her . And the black dress with luxurious lace was not seen on her ; it was just a frame , and only she was seen - simple , natural , graceful , and at the same time gay and animated .
Highlight (yellow) - XXII > Page 96 · Location 2067
Kitty looked into his face , which was such a short distance from hers , and long afterwards , for several years , that look , so full of love , which she gave him then , and to which he did not respond , cut her heart with tormenting shame .
Highlight (yellow) - XXIII > Page 97 · Location 2073
Nothing important was said during the quadrille , there were snatches of conversation , now about the Korsunskys , husband and wife , whom he described very amusingly as sweet forty - year - old children , now about a future public theatre , 34 and only once did the conversation touch her to the quick , when he asked her whether Levin was there and added that he liked him very much .
Highlight (yellow) - XXIII > Page 97 · Location 2083
She knew that feeling , knew the signs of it , and she saw them in Anna - saw the tremulous , flashing light in her eyes , the smile of happiness and excitement that involuntarily curved her lips , and the precise gracefulness , assurance and lightness of her movements .
Highlight (yellow) - XXIII > Page 97 · Location 2089
Each time he spoke with Anna , her eyes flashed with
Highlight (yellow) - XXIII > Page 97 · Location 2089
She seemed to be struggling with herself to keep these signs of joy from showing , yet they appeared on her face of themselves
Highlight (yellow) - XXIII > Page 97 · Location 2091
Where was his quiet , firm manner and carefree , calm expression ? No , now each time he addressed Anna , he bowed his head slightly , as if wishing to fall down before her , and in his glance there were only obedience and fear . ‘ I do not want to offend you , ’ his glance seemed to say each time , ‘ I want to save myself but do not know how . ’ There was an expression on his face that she had never seen before .
Highlight (yellow) - XXIII > Page 98 · Location 2098
Only the strict school of upbringing she had gone through supported her and made her do what was demanded of her - that is , dance , answer questions , talk , even smile .
Highlight (yellow) - XXIII > Page 98 · Location 2100
Kitty was overcome by a moment of despair and horror . She had refused five partners and now would not dance the mazurka . There was even no hope that she would be asked , precisely because she had had too great a success in society , and it would not have entered anyone’s head that she had not been invited before then . She should have told her mother she was sick and gone home , but she did not have the strength for it . She felt destroyed .
Highlight (yellow) - XXIII > Page 98 · Location 2106
But though she had the look of a butterfly that clings momentarily to a blade of grass and is about to flutter up , unfolding its iridescent wings , a terrible despair pained her heart .
Highlight (yellow) - XXIII > Page 98 · Location 2121
And on Vronsky’s face , always so firm and independent , she saw that expression of lostness and obedience that had so struck her , like the expression of an intelligent dog when it feels guilty .
Highlight (yellow) - XXIII > Page 98 · Location 2123
She was enchanting in her simple black dress , enchanting were her full arms with the bracelets on them , enchanting her firm neck with its string of pearls , enchanting her curly hair in disarray , enchanting the graceful , light movements of her small feet and hands , enchanting that beautiful face in its animation ; but there was something terrible and cruel in her enchantment
Highlight (yellow) - XXIII > Page 99 · Location 2126
Kitty admired her even more than before , and suffered more and more . She felt crushed , and her face showed it . When Vronsky saw her , meeting her during the mazurka , he did not recognize her at first - she was so changed . ‘ A wonderful ball ! ’ he said to her , so as to say something . ‘ Yes , ’ she replied .
Highlight (yellow) - XXIII > Page 99 · Location 2133
‘ Yes , there’s something alien , demonic and enchanting in her , ’ Kitty said to herself .
Highlight (yellow) - XXIV > Page 100 · Location 2145
‘ Yes , there’s something disgusting and repulsive in me , ’ thought Levin , having left the Shcherbatskys and making his way on foot to his brother’s . ‘ And I don’t fit in with other people . It’s pride , they say . No , there’s no pride in me either . If there were any pride in me , I wouldn’t have put myself in such a position . ’ And he pictured Vronsky to himself , happy , kind , intelligent and calm , who certainly had never been in such a terrible position as he had been in that evening . ‘ Yes , she was bound to choose him . It had to be so , and I have nothing and no one to complain about . I myself am to blame . What right did I have to think she would want to join her life with mine ? Who am I ? And what am I ? A worthless man , of no use to anyone or for anything . ’ And he remembered his brother Nikolai and paused joyfully at this remembrance . ‘ Isn’t he right that everything in the world is bad and vile ? And our judgement of brother Nikolai has hardly been fair . Of course , from Prokofy’s point of view , who saw him drunk and in a ragged fur coat , he’s a despicable man ; but I know him otherwise . I know his soul , and I know that we resemble each other . And instead of going to look for him , I went to dinner and then came here . ’
Highlight (yellow) - XXIV > Page 100 · Location 2154
On the long way to his brother‘s , Levin vividly recalled all the events he knew from the life of his brother Nikolai . He remembered how his brother , while at the university and for a year after the university , despite the mockery of his friends , had lived like a monk , strictly observing all the rituals of religion , services , fasts , and avoiding all pleasures , especially women ; and then it was as if something broke loose in him , he began keeping company with the most vile people and gave himself up to the most licentious debauchery .
Highlight (yellow) - XXIV > Page 100 · Location 2166
Levin recalled how , during Nikolai’s period of piety , fasts , monks , church services , when he had sought help from religion as a bridle for his passionate nature , not only had no one supported him , but everyone , including Levin himself , had laughed at him . They had teased him , calling him ‘ Noah ’ and ‘ the monk ’ ; and when he broke loose , no one helped him , but they all turned away with horror and loathing .
Highlight (yellow) - XXIV > Page 101 · Location 2194
‘ Ah , Kostya ! ’ he said suddenly , recognizing his brother , and his eyes lit up with joy . But in the same second he glanced at the young man and made the convulsive movement with his head and neck that Konstantin knew so well , as if his tie were too tight on him ; and a quite different , wild , suffering and cruel expression settled on his emaciated face .
Highlight (yellow) - XXIV > Page 102 · Location 2202
‘ Ah , just like that ? ’ he said . ‘ Well , come in , sit down . Want some supper ? Masha , bring three portions . No , wait . Do you know who this is ? ’ he said to his brother , pointing to the gentleman in the sleeveless jacket . ‘ This is Mr Kritsky , my friend from way back in Kiev , a very remarkable man . He’s being sought by the police , of course , because he’s not a scoundrel . ’
Highlight (yellow) - XXV > Page 103 · Location 2225
‘ You know that capital oppresses the worker - the workers in our country , the muzhiks , bear all the burden of labour , and their position is such that , however much they work , they can never get out of their brutish situation . All the profits earned by their work , with which they might improve their situation , give themselves some leisure and , consequently , education , all surplus earnings are taken from them by the capitalists . And society has developed so that the more they work , the more gain there will be for the merchants and landowners , and they will always remain working brutes . And this order must be changed , ’ he concluded and looked inquiringly at his brother .
Highlight (yellow) - XXV > Page 103 · Location 2236
‘ Because the muzhiks are just as much slaves now as they were before , and that’s why you and Sergei Ivanych don’t like it that we want to bring them out of this slavery , ’ Nikolai Levin said , annoyed by the objection .
Highlight (yellow) - XXV > Page 103 · Location 2239
‘ I know the aristocratic views you and Sergei Ivanych have . I know that he employs all his mental powers to justify the existing evil . ’
Highlight (yellow) - XXV > Page 106 · Location 2300
‘ Don’t call her “ miss ” . She’s afraid of it . No one , except the justice of the peace , when she stood trial for wanting to leave the house of depravity , no one ever called her “ miss ” . My God , what is all this nonsense in the world ! ’ he suddenly cried out . ‘ These new institutions , these justices of the peace , the zemstvo - what is this outrage ! ’
Highlight (yellow) - XXVI > Page 107 · Location 2319
he felt the confusion gradually clearing up and the shame and dissatisfaction with himself going away .
Highlight (yellow) - XXVI > Page 107 · Location 2327
Then , too , his brother’s talk about communism , which he had taken so lightly at the time , now made him ponder . He regarded the reforming of economic conditions as nonsense , but he had always felt the injustice of his abundance as compared with the poverty of the people , and he now decided that , in order to feel himself fully in the right , though he had worked hard before and lived without luxury , he would now work still harder and allow himself still less luxury .
Highlight (yellow) - XXVI > Page 107 · Location 2337
The study was slowly lit up by the candle that was brought . Familiar details emerged : deer’s antlers , shelves of books , the back of the stove with a vent that had long been in need of repair , his father’s sofa , the big desk , an open book on the desk , a broken ashtray , a notebook with his handwriting . When he saw it all , he was overcome by a momentary doubt of the possibility of setting up that new life he had dreamed of on the way . All these traces of his life seemed to seize hold of him and say to him : ‘ No , you won’t escape us and be different , you’ll be the same as you were : with doubts , an eternal dissatisfaction with yourself , vain attempts to improve , and failures , and an eternal expectation of the happiness that has eluded you and is not possible for you . ’
Highlight (yellow) - XXVI > Page 108 · Location 2343
But that was how his things talked , while another voice in his soul said that he must not submit to his past and that it was possible to do anything with oneself .
Highlight (yellow) - XXVII > Page 109 · Location 2367
The house was big , old , and Levin , though he lived alone , heated and occupied all of it . He knew that this was foolish , knew that it was even wrong and contrary to his new plans , but this house was a whole world for Levin . It was the world in which his father and mother had lived and died . They had lived a life which for Levin seemed the ideal of all perfection and which he dreamed of renewing with his wife , with his family .
Highlight (yellow) - XXVII > Page 109 · Location 2371
Levin barely remembered his mother . His notion of her was a sacred memory , and his future wife would have to be , in his imagination , the repetition of that lovely , sacred ideal of a woman which his mother was for him .
Highlight (yellow) - XXVII > Page 109 · Location 2374
His notion of marriage was therefore not like the notion of the majority of his acquaintances , for whom it was one of the many general concerns of life ; for Levin it was the chief concern of life , on which all happiness depended . And now he had to renounce it !
Highlight (yellow) - XXVII > Page 109 · Location 2379
He read the book , thought about what he had read , paused to listen to Agafya Mikhailovna , who chattered tirelessly ; and along with that various pictures of farm work and future family life arose disconnectedly in his imagination . He felt that something in the depths of his soul was being established , adjusted and settled .
Highlight (yellow) - XXVII > Page 109 · Location 2392
But now everything will take a new course . It’s nonsense that life won’t allow it , that the past won’t allow it . I must fight to live a better life , much better . . . ’ He raised his head and pondered .
Highlight (yellow) - XXVII > Page 110 · Location 2395
‘ She all but speaks , ’ said Agafya Mikhailovna . ‘ Just a dog . . . But she understands that her master’s come back and is feeling sad . ’
Highlight (yellow) - XXVIII > Page 112 · Location 2436
‘ Oh , no , no ! I’m not like Stiva , ’ she said , frowning . ‘ I’m telling you this because I don’t allow myself to doubt myself even for a moment . ’ But the moment she uttered these words , she felt that they were wrong ; she not only doubted herself , but felt excitement at the thought of Vronsky , and was leaving sooner than she had wanted only so as not to meet him any more .
Highlight (yellow) - XXIX > Page 114 · Location 2473
Anna Arkadyevna read and understood , but it was unpleasant for her to read , that is , to follow the reflection of other people’s lives . She wanted too much to live herself .
Highlight (yellow) - XXIX > Page 114 · Location 2478
The hero of the novel was already beginning to achieve his English happiness , a baronetcy and an estate , and Anna wished to go with him to this estate , when suddenly she felt that he must be ashamed and that she was ashamed of the same thing . But what was he ashamed of ? ‘ What am I ashamed of ? ’ she asked herself in offended astonishment . She put down the book and leaned back in the seat , clutching the paper - knife tightly in both hands . There was nothing shameful . She went through all her Moscow memories . They were all good , pleasant . She remembered the ball , remembered Vronsky and his enamoured , obedient face , remembered all her relations with him : nothing was shameful . But just there , at that very place in her memories , the feeling of shame became more intense , as if precisely then , when she remembered Vronsky , some inner voice were telling her : ‘ Warm , very warm , hot ! ’ ‘ Well , what then ? ’ she said resolutely to herself , shifting her position in the seat . ‘ What does it mean ? Am I afraid to look at it directly ? Well , what of it ? Can it be that there exist or ever could exist any other relations between me and this boy - officer than those that exist with any acquaintance ? ’ She smiled scornfully and again picked up the book , but now was decidedly unable to understand what she was reading . She passed the paper - knife over the glass , then put its smooth and cold surface to her cheek and nearly laughed aloud from the joy that suddenly came over her for no reason . She felt her nerves tighten more and more , like strings on winding pegs . She felt her eyes open wider and wider , her fingers and toes move nervously ; something inside her stopped her breath , and all images and sounds in that wavering semi - darkness impressed themselves on her with extraordinary vividness . She kept having moments of doubt whether the carriage was moving forwards or backwards , or standing still . Was that Annushka beside her , or some stranger ? ‘ What is that on the armrest - a fur coat or some animal ? And what am I ? Myself or someone else ? ’ It was frightening to surrender herself to this oblivion . But something was drawing her in , and she was able , at will , to surrender to it or hold back from it . She stood up in order to come to her senses , threw the rug aside , and removed the pelerine from her warm dress . For a moment she recovered and realized that the skinny muzhik coming in , wearing a long nankeen coat with a missing button , was the stoker , that he was looking at the thermometer , that wind and snow had burst in with him through the doorway ; but then everything became confused again . . . This muzhik with the long waist began to gnaw at something on the wall ; the old woman began to stretch her legs out the whole length of the carriage and filled it with a black cloud ; then something screeched and banged terribly , as if someone was being torn to pieces ; then a red fire blinded her eyes , and then everything was hidden by a wall . Anna felt as if she was falling through the floor . But all this was not frightening but exhilarating . The voice of a bundled - up and snow - covered man shouted something into her ear . She stood up and came to her senses , realizing that they had arrived at a station and the man was the conductor . She asked Annushka to hand her the pelerine and a shawl , put them on and went to the door .
Note - XXIX > Page 115 · Location 2501
Reading distraction
Highlight (yellow) - XXX > Page 116 · Location 2519
More than once she had told herself during those recent days and again just now that for her Vronsky was one among hundreds of eternally identical young men to be met everywhere , that she would never allow herself even to think of him ; but now , in the first moment of meeting him , she was overcome by a feeling of joyful pride . She had no need to ask why he was there . She knew it as certainly as if he had told her that he was there in order to be where she was .
Highlight (yellow) - XXX > Page 116 · Location 2524
‘ Why am I going ? ’ he repeated , looking straight into her eyes . ‘ You know I am going in order to be where you are , ’ he said , ‘ I cannot do otherwise . ’
Highlight (yellow) - XXX > Page 116 · Location 2527
He had said the very thing that her soul desired but that her reason feared . She made no reply , and he saw a struggle in her face . ‘ Forgive me if what I have said is unpleasant for you , ’ he said submissively .
Highlight (yellow) - XXX > Page 117 · Location 2535
Though she could remember neither his words nor her own , she sensed that this momentary conversation had brought them terribly close , and this made her both frightened and happy . She stood for a few seconds , went into the carriage , and took her seat .
Highlight (yellow) - XXX > Page 117 · Location 2538
But in that strain and those reveries that filled her imagination there was nothing unpleasant or gloomy ; on the contrary , there was something joyful , burning , and exciting . Towards morning Anna dozed off in her seat , and when she woke up it was already white , bright , and the train was pulling into Petersburg . At once thoughts of her home , her husband , her son , and the cares of the coming day and those to follow surrounded her .
Highlight (yellow) - XXX > Page 117 · Location 2545
Some unpleasant feeling gnawed at her heart as she met his unwavering and weary gaze , as if she had expected him to look different . She was especially struck by the feeling of dissatisfaction with herself that she experienced on meeting him .
Highlight (yellow) - XXX > Page 117 · Location 2548
‘ Yes , as you see , your tender husband , tender as in the second year of marriage , is burning with desire to see you , ’ he said in his slow , high voice and in the tone he almost always used with her , a tone in mockery of someone who might actually mean what he said . ‘ Is Seryozha well ? ’ she asked . ‘ Is that all the reward I get for my ardour ? ’ he said . ‘ He’s well , he’s well . . . ’
Highlight (yellow) - XXXI > Page 118 · Location 2555
he now seemed still more proud and self - sufficient . He looked at people as if they were things . A nervous young man across from him , who served on the circuit court , came to hate him for that look . The young man lit a cigarette from his , tried talking to him , and even jostled him , to let him feel that he was not a thing but a human being , but Vronsky went on looking at him as at a lamppost , and the young man grimaced , feeling that he was losing his self - possession under the pressure of this non - recognition of himself as a human being and was unable to fall asleep because of it .
Highlight (yellow) - XXXI > Page 118 · Location 2562
He knew only that he had told her the truth , that he was going where she was , that the whole happiness of life , the sole meaning of life , he now found in seeing and hearing her .
Highlight (yellow) - XXXI > Page 118 · Location 2565
Returning to his carriage , he kept running through all the attitudes in which he had seen her , all her words , and in his imagination floated pictures of the possible future , making his heart stand still .
Highlight (yellow) - XXXI > Page 119 · Location 2578
He told his German footman , who came running from second class , to take his things and go , and he himself went up to her . He saw the first meeting of husband and wife and , with the keen - sightedness of a man in love , noticed signs of the slight constraint with which she talked to her husband . ‘ No , she does not and cannot love him , ’ he decided to himself .
Highlight (yellow) - XXXI > Page 119 · Location 2586
yet for a moment , as she glanced at him , something flashed in her eyes and , although this fire went out at once , he was happy in that moment .
Highlight (yellow) - XXXI > Page 119 · Location 2588
Vronsky’s calm and self - confidence here clashed like steel against stone with the cold self - confidence of Alexei Alexandrovich .
Highlight (yellow) - XXXII > Page 121 · Location 2615
And the son , just like the husband , produced in Anna a feeling akin to disappointment . She had imagined him better than he was in reality . She had to descend into reality to enjoy him as he was . But he was charming even as he was , with his blond curls , blue eyes and full , shapely legs in tight - fitting stockings .
Highlight (yellow) - XXXII > Page 121 · Location 2622
Countess Lydia Ivanovna was a tall , stout woman with an unhealthy yellow complexion and beautiful , pensive dark eyes . Anna loved her , but today she saw her as if for the first time with all her shortcomings .
Highlight (yellow) - XXXII > Page 121 · Location 2635
Pravdin was a well - known Pan - Slavist42 who lived abroad . Countess Lydia Ivanovna proceeded to recount the contents of his letter .
Highlight (yellow) - XXXII > Page 122 · Location 2644
Her agitation and the sense of groundless shame she had experienced during the journey disappeared completely . In the accustomed conditions of her life she again felt herself firm and irreproachable .
Note - XXXII > Page 122 · Location 2645
Parallel with levin
Highlight (yellow) - XXXIII > Page 123 · Location 2657
Every minute of Alexei Alexandrovich’s life was occupied and scheduled . And in order to have time to do what he had to do each day , he held to the strictest punctuality . ‘ Without haste and without rest ’ was his motto . He entered the room , bowed to everyone , and hastily sat down , smiling at his wife .
Highlight (yellow) - XXXIII > Page 123 · Location 2666
Before leaving for Moscow , she , who was generally an expert at dressing not very expensively , had given her dressmaker three dresses to be altered . The dresses needed to be altered so that they could not be recognized , and they were to have been ready three days ago . It turned out that two of the dresses were not ready at all , and the third had not been altered in the way Anna wanted .
Highlight (yellow) - XXXIII > Page 123 · Location 2671
She saw clearly that everything that had seemed so important to her on the train was merely one of the ordinary , insignificant episodes of social life , and there was nothing to be ashamed of before others or herself .
Highlight (yellow) - XXXIII > Page 124 · Location 2686
With the same self - satisfied smile , he told her about an ovation he had received as a result of the passing of this statute .
Highlight (yellow) - XXXIII > Page 124 · Location 2691
‘ Oh , no ! ’ she replied , getting up after him and accompanying him across the drawing room to his study . ‘ What are you reading now ? ’ she asked . ‘ I’m now reading the Duc de Lille , Poésie des enfers , ’ 43 he replied . ‘ A very remarkable book . ’
Highlight (yellow) - XXXIII > Page 124 · Location 2695
She knew that in spite of the responsibilities of service which consumed almost all his time , he considered it his duty to follow everything remarkable that appeared in the intellectual sphere . She also knew that he was indeed interested in books on politics , philosophy , theology , that art was completely foreign to his nature , but that , in spite of that , or rather because of it , Alexei Alexandrovich did not miss anything that caused a stir in that area , and considered it his duty to read everything .
Highlight (yellow) - XXXIII > Page 124 · Location 2699
She knew that in the areas of politics , philosophy and theology , Alexei Alexandrovich doubted or searched ; but in questions of art and poetry , and especially music , of which he lacked all understanding , he had the most definite and firm opinions . He liked to talk about Shakespeare , Raphael , Beethoven , about the significance of the new schools in poetry and music , which with him were all sorted out in a very clear order .
Highlight (yellow) - XXXIV > Page 126 · Location 2720
Baroness Shilton , Petritsky’s lady - friend , her lilac satin dress and rosy fair face shining , and her canary - like Parisian talk filling the whole room , was sitting at a round table making coffee .
Highlight (yellow) - XXXIV > Page 126 · Location 2732
‘ Pass me the coffee , Pierre . ’ She turned to Petritsky , whom she called Pierre after his last name , not concealing her relations with him . ‘ I’ll add some more . ’
Highlight (yellow) - XXXIV > Page 127 · Location 2739
‘ He keeps refusing to grant me a divorce ! Well , what am I to do ? ’ ( ‘ He ’ was her husband . ) ‘ I want to start proceedings . How would you advise me ? Kamerovsky , keep an eye on the coffee , it’s boiling over — you can see I’m busy ! I want proceedings , because I need my fortune . Do you understand this stupidity - that I’m supposedly unfaithful to him , ’ she said with scorn , ‘ and so he wants to have use of my estate ? ’
Highlight (yellow) - XXXIV > Page 127 · Location 2743
In his Petersburg world , all people were divided into two completely opposite sorts . One was the inferior sort : the banal , stupid and , above all , ridiculous people who believed that one husband should live with one wife , whom he has married in church , that a girl should be innocent , a woman modest , a man manly , temperate and firm , that one should raise children , earn one’s bread , pay one’s debts , and other such stupidities . This was an old - fashioned and ridiculous sort of people . But there was another sort of people , the real ones , to which they all belonged , and for whom one had , above all , to be elegant , handsome , magnanimous , bold , gay , to give oneself to every passion without blushing and laugh at everything else .
Highlight (yellow) - XXXIV > Page 127 · Location 2753
‘ Well , good - bye now , or else you’ll never get washed , and I’ll have on my conscience the worst crime of a decent person - uncleanliness . So your advice is a knife at his throat ? ’
Highlight (yellow) - XXXIV > Page 127 · Location 2758
Of money there was none . His father said he would not give him any , nor pay his debts . One tailor wanted to have him locked up , and the other was also threatening to have him locked up without fail .
Highlight (yellow) - XXXIV > Page 127 · Location 2761
he would show her to Vronsky , a wonder , a delight , in the severe Levantine style , the ‘ slave - girl Rebecca genre , 44 you know ’ .
Part Two
Highlight (yellow) - I > Page 130 · Location 2788
With particular pleasure , it seemed , he insisted that maidenly modesty was merely a relic of barbarism and that nothing was more natural than for a not - yet - old man to palpate a naked young girl . He found it natural because he did it every day and never , as it seemed to him , felt or thought anything bad , and therefore he regarded modesty in a girl not only as a relic of barbarism but also as an affront to himself .
Highlight (yellow) - I > Page 130 · Location 2795
The prince frowned and kept coughing as he listened to the doctor . He , as a man who had seen life and was neither stupid nor sick , did not believe in medicine , and in his soul he was angry at this whole comedy , the more so in that he was almost the only one who fully understood the cause of Kitty’s illness .
Highlight (yellow) - I > Page 131 · Location 2821
And the famous doctor presented his plan of treatment by Soden waters , the main aim in the prescription of which evidently being that they could do no harm .
Highlight (yellow) - I > Page 131 · Location 2832
Her whole illness and treatment seemed to her such a stupid , even ridiculous thing ! Her treatment seemed to her as ridiculous as putting together the pieces of a broken vase . Her heart was broken . And what did they want to do , treat her with pills and powders ? But she could not insult her mother , especially since her mother considered herself to blame .
Highlight (yellow) - I > Page 132 · Location 2844
The mother cheered up as she came back to her daughter , and Kitty pretended to cheer up . She often , almost always , had to pretend now .
Highlight (yellow) - II > Page 133 · Location 2858
The first outburst of jealousy , once lived through , could not come again , and even the discovery of unfaithfulness could not affect her as it had the first time . Such a discovery would now only deprive her of her family habits , and she allowed herself to be deceived , despising him and most of all herself for this weakness .
Highlight (yellow) - II > Page 133 · Location 2872
As the youngest , she was her father’s favourite , and it seemed to her that his love for her gave him insight . When her glance now met his kindly blue eyes gazing intently at her , it seemed to her that he saw right through her and understood all the bad that was going on inside her . Blushing , she leaned towards him , expecting a kiss , but he only patted her hair and said : ‘ These stupid chignons ! You can’t even get to your real daughter , but only caress the hair of dead wenches . Well , Dolinka , ’ he turned to his eldest daughter , ‘ what’s your trump up to ? ’
Highlight (yellow) - II > Page 134 · Location 2883
What her father said seemed so simple , yet Kitty became confused and bewildered at these words , like a caught criminal . ‘ Yes , he knows everything , understands everything , and with these words he’s telling me that , though I’m ashamed , I must get over my shame . ’ She could not pluck up her spirits enough to make any reply . She tried to begin , but suddenly burst into tears and rushed from the room .
Highlight (yellow) - II > Page 134 · Location 2891
‘ Ah , I can’t listen ! ’ the prince said gloomily , getting up from his armchair and making as if to leave , but stopping in the doorway . ‘ There are laws , dearest , and since you’re calling me out on it , I’ll tell you who is to blame for it all : you , you and you alone . There are and always have been laws against such young devils ! Yes , ma’am , and if it hadn’t been for what should never have been , I , old as I am , would have challenged him to a duel , that fop . Yes , so treat her now , bring in your charlatans . ’
Highlight (yellow) - III > Page 136 · Location 2931
Dolly knew this way her sister had of grasping something with her hands when she was in a temper ; she knew that Kitty was capable of forgetting herself in such a moment and saying a lot of unnecessary and unpleasant things , and Dolly wanted to calm her down . But it was already too late .
Highlight (yellow) - III > Page 137 · Location 2943
‘ Why bring Levin into it , too ? I don’t understand , why do you need to torment me ? I said and I repeat that I’m proud and would never , never do what you’re doing - go back to a man who has betrayed you , who has fallen in love with another woman . I don’t understand , I don’t understand that ! You may , but I can’t ! ’
Highlight (yellow) - III > Page 137 · Location 2952
As if tears were the necessary lubricant without which the machine of mutual communication could not work successfully , the two sisters , after these tears , started talking , not about what preoccupied them , but about unrelated things , and yet they understood each other .
Highlight (yellow) - III > Page 137 · Location 2956
Dolly , for her part , understood everything she had wanted to know ; she was satisfied that her guesses were right , that Kitty’s grief , her incurable grief , was precisely that Levin had made a proposal and that she had refused him , while Vronsky had deceived her , and that she was ready to love Levin and hate Vronsky . Kitty did not say a word about it ; she spoke only of her state of mind .
Highlight (yellow) - III > Page 137 · Location 2962
‘ The most , most vile and coarse - I can’t tell you . It’s not anguish , or boredom , it’s much worse . As if all that was good in me got hidden , and only what’s most vile was left .
Highlight (yellow) - III > Page 137 · Location 2963
‘ Papa started saying to me just now . . . it seems to me all he thinks is that I’ve got to get married . Mama takes me to a ball : it seems to me she only takes me in order to get me married quickly and be rid of me . I know it’s not true , but I can’t drive these thoughts away . The so - called suitors I can’t even look at . It seems as if they’re taking my measurements . Before it was simply a pleasure for me to go somewhere in a ball gown , I admired myself ; now I feel ashamed , awkward . Well , what do you want ! The doctor . . . Well
Highlight (yellow) - IV > Page 139 · Location 2989
It seemed to her that both she and all the others were pretending , and she felt so bored and awkward in this company that she called on Countess Lydia Ivanovna as seldom as possible .
Highlight (yellow) - IV > Page 139 · Location 2991
The third circle , finally , in which she had connections , was society proper - the society of balls , dinners , splendid gowns , a monde that held on with one hand to the court , so as not to descend to the demi - monde , which the members of this circle thought they despised , but with which they shared not only similar but the same tastes .
Note - IV > Page 139 · Location 2993
World
Highlight (yellow) - IV > Page 139 · Location 2997
At first Anna had avoided this society of Princess Tverskoy’s as much as she could , because it called for expenses beyond her means , and also because at heart she preferred the other ; but after her visit to Moscow it turned the other way round . She avoided her virtuous friends and went into the great world .
Highlight (yellow) - IV > Page 140 · Location 3020
He knew very well that in the eyes of Betsy and all society people he ran no risk of being ridiculous . He knew very well that for those people the role of the unhappy lover of a young girl , or of a free woman generally , might be ridiculous ; but the role of a man who attached himself to a married woman and devoted his life to involving her in adultery at all costs , had something beautiful and grand about it and could never be ridiculous , and therefore , with a proud and gay smile playing under his moustache , he lowered the opera - glasses and looked at his cousin .
Highlight (yellow) - IV > Page 141 · Location 3032
‘ Blessed are the peacemakers , for they shall be saved , ’ 3 said Betsy , remembering hearing something of the sort from someone . ‘ Sit down , then , and tell me about it . ’
Highlight (yellow) - V > Page 143 · Location 3085
The regimental commander had summoned Vronsky precisely because he knew him to be a noble and intelligent man and , above all , a man who cherished the honour of the regiment . They had talked it over and decided that Petritsky and Kedrov would have to go to this titular councillor with Vronsky and apologize . The
Highlight (yellow) - VI > Page 145 · Location 3122
The conversation had begun nicely , but precisely because it was much too nice , it stopped again . They had to resort to that sure , never failing remedy - malicious gossip .
Highlight (yellow) - VI > Page 146 · Location 3135
The princess Betsy’s husband , a fat good - natured man , a passionate collector of etchings , learning that his wife had guests , stopped in the drawing room before going to his club . He approached Princess Miagky inaudibly over the soft carpet .
Highlight (yellow) - VI > Page 146 · Location 3147
‘ Amazing ! ’ someone said . The effect produced by Princess Miagky’s talk was always the same , and the secret of it consisted in her saying simple things that made sense , even if , as now , they were not quite appropriate . In the society in which she lived , such words produced the impression of a most witty joke . Princess Miagky could not understand why it worked that way , but she knew that it did work , and she took advantage of it .
Highlight (yellow) - VI > Page 147 · Location 3159
‘ What of it ? Grimm has a fable — a man without a shadow , a man deprived of a shadow . 10 And it’s his punishment for something . I could never understand where the punishment lay . But it must be unpleasant for a woman to be without a shadow . ’ ‘ Yes , but women with a shadow generally end badly , ’ said Anna’s friend .
Highlight (yellow) - VI > Page 147 · Location 3169
‘ Not in the least . I have no other way out . One of us is stupid . Well , and you know one can never say that about oneself . ’ ‘ No one is pleased with his fortune , but everyone is pleased with his wit , ’ said the diplomat , quoting some French verse .
Highlight (yellow) - VII > Page 149 · Location 3203
‘ And is it true that her younger sister is marrying Topov ? ’ ‘ Yes , they say it’s quite decided . ’ ‘ I’m surprised at the parents . They say it’s a marriage of passion . ’ ‘ Of passion ? What antediluvian thoughts you have ! Who talks about passions these days ? ’ said the ambassador’s wife . ‘ What’s to be done ? This stupid old fashion hasn’t gone out of use , ’ said Vronsky . ‘ So much the worse for those who cling to it . The only happy marriages I know are arranged ones . ’ ‘ Yes , but how often the happiness of an arranged marriage scatters like dust , precisely because of the appearance of that very passion which was not acknowledged , ’ said Vronsky . ‘ But by arranged marriages we mean those in which both have already had their wild times . It’s like scarlet fever , one has to go through it . ’ ‘ Then we should find some artificial inoculation against love , as with smallpox . ’
Highlight (yellow) - VII > Page 150 · Location 3219
‘ I think , ’ said Anna , toying with the glove she had taken off , ‘ I think . . . if there are as many minds as there are men , then there are as many kinds of love as there are hearts . ’ Vronsky was looking at Anna and waiting with a sinking heart for what she would say . He exhaled as if after danger when she spoke these words . Anna suddenly turned to him : ‘ And I have received a letter from Moscow . They write that Kitty Shcherbatsky is very ill . ’
Highlight (yellow) - VII > Page 150 · Location 3241
‘ Remember , I forbade you to utter that word , that vile word , ’ Anna said with a shudder ; but she felt at once that by this one word ‘ forbade ’ she showed that she acknowledged having certain rights over him and was thereby encouraging him to speak of love . ‘ I’ve long wanted to tell you that , ’ she went on , looking resolutely into his eyes , and all aflame with the blush that burned her face , and tonight I came on purpose , knowing that I would meet you . I came to tell you that this must end . I have never blushed before anyone , but you make me feel guilty of something . ’
Highlight (yellow) - VII > Page 151 · Location 3255
She strained all the forces of her mind to say what she ought to say ; but instead she rested her eyes on him , filled with love , and made no answer . ‘ There it is ! ’ he thought with rapture . ‘ When I was already in despair , and when it seemed there would be no end - there it is ! She loves me . She’s confessed
Highlight (yellow) - VII > Page 151 · Location 3268
‘ Your Rambouillet is in full muster , ’ he said , glancing around the whole company , ‘ graces and muses . ’
Highlight (yellow) - VII > Page 152 · Location 3285
The Karenin coachman , a fat old Tartar in a glossy leather coat , had difficulty holding back the chilled grey on the left , who kept rearing up by the entrance .
Note - VII > Page 152 · Location 3286
Plato Phaedrus
Highlight (yellow) - VII > Page 152 · Location 3289
‘ You’ve said nothing ; let’s suppose I also demand nothing , ’ he said , ‘ but you know it’s not friendship I need , for me there is only one possible happiness in life , this word you dislike so . . . yes , love . . . ’ ‘ Love . . . ’ she repeated slowly with her inner voice , and suddenly , just as she freed the lace , added : ‘ That’s why I don’t like this word , because it means too much for me , far more than you can understand , ’ and she looked him in the face : ‘ Good - bye ! ’
Highlight (yellow) - VIII > Page 153 · Location 3297
Alexei Alexandrovich found nothing peculiar or improper in the fact that his wife was sitting at a separate table with Vronsky and having an animated conversation about something ; but he noticed that to the others in the drawing room it seemed something peculiar and improper , and therefore he , too , found it improper . He decided that he ought to say so to his wife .
Highlight (yellow) - VIII > Page 153 · Location 3308
Alexei Alexandrovich was not a jealous man . Jealousy , in his opinion , was insulting to a wife , and a man ought to have trust in his wife . Why he ought to have trust - that is , complete assurance that his young wife would always love him - he never asked himself ; but he felt no distrust , because he had trust and told himself that he had to have it . But now , though his conviction that jealousy was a shameful feeling and that one ought to have trust was not destroyed , he felt that he stood face to face with something illogical and senseless , and he did not know what to do . Alexei Alexandrovich stood face to face with life , confronting the possibility of his wife loving someone else besides him , and it was this that seemed so senseless and incomprehensible to him , because it was life itself . All his life Alexei Alexandrovich had lived and worked in spheres of service that dealt with reflections of life . And each time he had encountered life itself , he had drawn back from it . Now he experienced a feeling similar to what a man would feel who was calmly walking across a bridge over an abyss and suddenly saw that the bridge had been taken down and below him was the bottomless deep . This bottomless deep was life itself , the bridge the artificial life that Alexei Alexandrovich had lived . For the first time questions came to him about the possibility of his wife falling in love with someone , and he was horrified at them .
Note - VIII > Page 153 · Location 3313
Life
Highlight (yellow) - VIII > Page 154 · Location 3330
And answered : nothing , and remembered that jealousy was a feeling humiliating for a wife , but again in the drawing room he was convinced that something had happened . His thoughts , like his body , completed a full circle without encountering anything new . He noticed it , rubbed his forehead , and sat down in her boudoir .
Highlight (yellow) - VIII > Page 154 · Location 3333
Here , looking at her desk with the malachite blotter and an unfinished letter lying on it , his thoughts suddenly changed . He began thinking about her , about what she thought and felt . For the first time he vividly pictured to himself her personal life , her thoughts , her wishes , and the thought that she could and should have her own particular life seemed so frightening to him that he hastened to drive it away . It was that bottomless deep into which it was frightening to look .
Highlight (yellow) - VIII > Page 154 · Location 3341
‘ Questions about her feelings , about what has been or might be going on in her soul , are none of my business ; they are the business of her conscience and belong to religion , ’ he said to himself , feeling relieved at the awareness that he had found the legitimate category to which the arisen circumstance belonged .
Highlight (yellow) - VIII > Page 154 · Location 3348
Thinking over what he would say , he regretted that he had to put his time and mental powers to such inconspicuous domestic use ; but , in spite of that , the form and sequence of the imminent speech took shape in his head clearly and distinctly , like a report . ‘ I must say and speak out the following : first , an explanation of the meaning of public opinion and propriety ; second , a religious explanation of the meaning of marriage ; third , if necessary , an indication of the possible unhappiness for our son ; fourth , an indication of her own unhappiness . ’ And , interlacing his fingers , palms down , Alexei Alexandrovich stretched so that the joints cracked .
Highlight (yellow) - IX > Page 156 · Location 3367
Anna said whatever came to her tongue , and was surprised , listening to herself , at her ability to lie . How simple , how natural her words were , and how it looked as if she simply wanted to sleep ! She felt herself clothed in an impenetrable armour of lies . She felt that some invisible force was helping her and supporting her .
Highlight (yellow) - IX > Page 156 · Location 3372
But for him who knew her , who knew that when he went to bed five minutes late , she noticed it and asked the reason , who knew that she told him at once her every joy , happiness , or grief — for him it meant a great deal to see now that she did not want to notice his state or say a word about herself . He saw that the depth of her soul , formerly always open to him , was now closed to him . Moreover , by her tone he could tell that she was not embarrassed by it , but was as if saying directly to him : yes , it’s closed , and so it ought to be and will be in the future . He now felt the way a man would feel coming home and finding his house locked up . ‘ But perhaps the key will still be found , ’ thought Alexei Alexandrovich .
Highlight (yellow) - IX > Page 157 · Location 3386
‘ But what is all this ? ’ she said with sincere and comical surprise . ‘ What do you want from me ? ’
Highlight (yellow) - IX > Page 157 · Location 3394
‘ I really don’t understand , ’ said Anna , shrugging her shoulders . ‘ He doesn’t care , ’ she thought . ‘ But society noticed and that troubles him . ’
Highlight (yellow) - IX > Page 157 · Location 3401
‘ I have no right to enter into all the details of your feelings , and generally I consider it useless and even harmful , ’ Alexei Alexandrovich began . ‘ Rummaging in our souls , we often dig up something that ought to have lain there unnoticed . Your feelings are a matter for your conscience ; but it is my duty to you , to myself , and to God , to point out your duties to you . Our lives are bound together , and bound not by men but by God . Only a crime can break this bond , and a crime of that sort draws down a heavy punishment . ’
Note - IX > Page 157 · Location 3404
Gaslighting
Highlight (yellow) - IX > Page 157 · Location 3408
For a moment her face fell and the mocking spark in her eye went out ; but the word ‘ love ’ again made her indignant . She thought : ‘ Love ? But can he love ? If he hadn’t heard there was such a thing as love , he would never have used the word . He doesn’t even know what love is . ’
Highlight (yellow) - IX > Page 158 · Location 3415
Alexei Alexandrovich , not noticing it himself , was saying something quite other than what he had prepared .
Highlight (yellow) - IX > Page 158 · Location 3418
When she came into the bedroom , he was already lying down . His lips were sternly compressed , and his eyes were not looking at her . Anna got into her own bed and waited every minute for him to begin talking to her again . She feared that he would , and at the same time she wanted it . But he was silent . For a long time she waited motionless and then forgot about him . She was thinking about another man , she could see him , and felt how at this thought her heart filled with excitement and criminal joy . Suddenly she heard a steady , peaceful nasal whistling . At first , Alexei Alexandrovich seemed startled by this whistling and stopped ; but after two breaths the whistling began again with a new , peaceful steadiness .
Highlight (yellow) - IX > Page 158 · Location 3423
‘ It’s late now , late , late , ’ she whispered with a smile . She lay for a long time motionless , her eyes open , and it seemed to her that she herself could see them shining in the darkness .
Highlight (yellow) - X > Page 159 · Location 3426
From that evening a new life began for Alexei Alexandrovich and his wife . Nothing special happened . Anna went into society as always , visited Princess Betsy especially often , and met Vronsky everywhere . Alexei Alexandrovich saw it but could do nothing . To all his attempts at drawing her into an explanation she opposed the impenetrable wall of some cheerful perplexity
Highlight (yellow) - X > Page 159 · Location 3430
Each time he began thinking about it , he felt that he had to try once more , that by kindness , tenderness and persuasion there was still a hope of saving her , of making her come to her senses , and he tried each day to talk with her . But each time he started talking with her , he felt that the spirit of evil and deceit that possessed her also took possession of him , and he said something to her that was not right at all and not in the tone in which he had wanted to speak . He talked with her involuntarily in his habitual tone , which was a mockery of those who would talk that way seriously . And in that tone it was impossible to say what needed to be said to her .
Highlight (yellow) - XI > Page 160 · Location 3436
That which for almost a year had constituted the one exclusive desire of Vronsky’s life , replacing all former desires ; that which for Anna had been an impossible , horrible , but all the more enchanting dream of happiness - this desire had been satisfied . Pale , his lower jaw trembling , he stood over her and pleaded with her to be calm , himself not knowing why or how .
Highlight (yellow) - XI > Page 160 · Location 3443
She felt herself so criminal and guilty that the only thing left for her was to humble herself and beg forgiveness ; but as she had no one else in her life now except him , it was also to him that she addressed her plea for forgiveness . Looking at him , she physically felt her humiliation and could say nothing more . And he felt what a murderer must feel when he looks at the body he has deprived of life . This body deprived of life was their love , the first period of their love . There was something horrible and loathsome in his recollections of what had been paid for with this terrible price of shame . Shame at her spiritual nakedness weighed on her and communicated itself to him . But , despite all the murderer’s horror before the murdered body , he had to cut this body into pieces and hide it , he had to make use of what the murderer had gained by his murder . And as the murderer falls upon this body with animosity , as if with passion , drags it off and cuts it up , so he covered her face and shoulders with kisses . She held his hand and did not move . Yes , these kisses were what had been bought by this shame . Yes , and this one hand , which will always be mine , is the hand of my accomplice . She raised this hand and kissed it . He knelt down and tried to look at her face ; but she hid it and said nothing . Finally , as if forcing herself , she sat up and pushed him away . Her face was still as beautiful , but the more pitiful for that .
Highlight (yellow) - XI > Page 160 · Location 3458
She felt that at that moment she could not put into words her feeling of shame , joy , and horror before this entry into a new life , and she did not want to speak of it , to trivialize this feeling with imprecise words . But later , too , the next day and the day after that , she not only found no words in which she could express all the complexity of these feelings , but was unable even to find thoughts in which she could reflect with herself on all that was in her soul .
Highlight (yellow) - XI > Page 161 · Location 3465
But in sleep , when she had no power over her thoughts , her situation presented itself to her in all its ugly nakedness . One dream visited her almost every night . She dreamed that they were both her husbands , that they both lavished their caresses on her . Alexei Alexandrovich wept , kissing her hands and saying : ‘ It’s so good now ! ’ And Alexei Vronsky was right there , and he , too , was her husband . And , marvelling that it had once seemed impossible to her , she laughingly explained to them that this was much simpler and that now they were both content and happy . But this dream weighed on her like a nightmare , and she would wake up in horror .
Note - XI > Page 161 · Location 3467
Dream
Highlight (yellow) - XII > Page 162 · Location 3482
However often he said to himself that he was in no way to blame , this memory , on a par with other shameful memories of the same sort , made him start and blush . In his past , as in any man’s past , there were actions he recognized as bad , for which his conscience ought to have tormented him ; yet the memory of the bad actions tormented him far less than these insignificant but shameful memories .
Highlight (yellow) - XII > Page 162 · Location 3489
Meanwhile spring had come , beautiful , harmonious , without spring’s anticipations and deceptions , one of those rare springs that bring joy to plants , animals and people alike .
Highlight (yellow) - XII > Page 163 · Location 3497
Levin had also begun that winter to write a work on farming , the basis of which was that the character of the worker had to be taken as an absolute given in farming , like climate and soil , and that , consequently , all propositions in the science of farming ought to be deduced not from the givens of soil and climate alone , but also from the known , immutable character of the worker .
Highlight (yellow) - XII > Page 163 · Location 3500
only once in a while did he feel an unsatisfied desire to tell the thoughts that wandered through his head to someone besides Agafya Mikhailovna , though with her , too , he often happened to discuss physics , the theory of farming , and especially philosophy . Philosophy was Agafya Mikhailovna’s favourite subject .
Highlight (yellow) - XII > Page 163 · Location 3510
The old grass and the sprouting needles of new grass greened , the buds on the guelder - rose , the currants and the sticky , spiritous birches swelled , and on the willow , all sprinkled with golden catkins , the flitting , newly hatched bee buzzed . Invisible larks poured trills over the velvety green fields and the ice - covered stubble , the peewit wept over the hollows and marshes still filled with brown water ; high up the cranes and geese flew with their spring honking . Cattle , patchy , moulted in all but a few places , lowed in the meadows , bow - legged lambs played around their bleating , shedding mothers , fleet - footed children ran over the drying paths covered with the prints of bare feet , the merry voices of women with their linen chattered by the pond , and from the yards came the knock of the peasants ’ axes , repairing ploughs and harrows . 17 The real spring had come .
Note - XII > Page 163 · Location 3516
Spring
Highlight (yellow) - XIII > Page 164 · Location 3530
What vexed him was the repetition of this eternal slovenliness of farm work , which he had fought against with all his strength for so many years .
Highlight (yellow) - XIII > Page 166 · Location 3570
Nothing so upset Levin as this tone . But it was a tone common to all stewards , as many of them as he had employed . They all had the same attitude towards his proposals , and therefore he now no longer got angry , but became upset and felt himself still more roused to fight this somehow elemental force for which he could find no other name than ‘ as God grants ’ , and which was constantly opposed to him .
Highlight (yellow) - XIII > Page 166 · Location 3576
Levin kept silent . Again this force opposed him . He knew that , hard as they tried , they had never been able to hire more than forty workers , thirty - seven , thirty - eight , at the real price ; they might get forty , but not more . Yet he could not help fighting even so .
Highlight (yellow) - XIII > Page 166 · Location 3594
The further he rode , the happier he felt , and plans for the estate , one better than another , arose in his mind : to plant willows along the meridional lines of all the fields , so that the snow would not stay too long under them ; to divide them into six fertilized fields and three set aside for grass ; to build a cattle - yard at the far end of the field and dig a pond ; to set up movable pens for the cattle so as to manure the fields .
Highlight (yellow) - XIII > Page 167 · Location 3613
Vassily pointed to a mark with his foot , and Levin went , as well as he could , scattering the seeds mixed with soil . It was hard walking , as through a swamp , and having gone one row , Levin became sweaty , stopped and handed the seed basket back .
Highlight (yellow) - XIII > Page 167 · Location 3624
‘ Well , make sure you rub out these lumps , ’ said Levin , going towards his horse , ‘ and keep an eye on Mishka . If it comes up well , you’ll get fifty kopecks per acre . ’
Highlight (yellow) - XIV > Page 169 · Location 3639
He found it frightening and unpleasant in the first moment that the presence of his brother might spoil this happy spring mood of his . Then he became ashamed of this feeling , and at once opened , as it were , his inner embrace and with tender joy now expected and wished it to be his brother . He urged the horse on and , passing the acacia tree , saw the hired troika driving up from the railway station with a gentleman in a fur coat . It was not his brother . ‘ Ah , if only it’s someone pleasant that I can talk with , ’ he thought .
Highlight (yellow) - XIV > Page 169 · Location 3657
‘ Well , how glad I am that I got to you ! Now I’ll understand what these mysteries are that you perform here . No , really , I envy you . What a house , how nice it all is ! Bright , cheerful ! ’ Stepan Arkadyich said , forgetting that it was not always spring and a clear day like that day . ‘ And your nanny’s such a dear ! A pretty maid in a little apron would be preferable , but with your monasticism and strict style - it’s quite all right . ’
Highlight (yellow) - XIV > Page 170 · Location 3677
‘ Yes , but wait : I’m not talking about political economy , I’m talking about scientific farming . It must be like a natural science , observing given phenomena , and the worker with his economic , ethnographic . . . ’
Highlight (yellow) - XIV > Page 171 · Location 3696
‘ How is it you don’t smoke ! A cigar - it’s not so much a pleasure as the crown and hallmark of pleasure . This is the life ! How good ! This is how I’d like to live ! ’
Note - XIV > Page 171 · Location 3697
Smoking
Highlight (yellow) - XIV > Page 171 · Location 3709
‘ There is , brother ! Look , you know there’s this type of Ossianic21 women . . . women you see in your dreams . . . But these women exist in reality . . . and these women are terrible . Woman , you see , it’s such a subject that , however much you study her , there’ll always be something new . ’
Note - XIV > Page 171 · Location 3711
Ossian women
Highlight (yellow) - XIV > Page 171 · Location 3714
Levin listened silently and , despite all his efforts , was simply unable to get inside his friend’s soul and understand his feelings or the charms of studying such women .
Highlight (yellow) - XVII > Page 178 · Location 3859
Kitty was unmarried and ill , ill from love for a man who had scorned her . This insult seemed to fall upon him . Vronsky had scorned her , and she had scorned him , Levin . Consequently , Vronsky had the right to despise Levin and was therefore his enemy . But Levin did not think all that . He vaguely felt that there was something insulting to him in it , and now was not angry at what had upset him but was finding fault with everything he came across .
Highlight (yellow) - XVII > Page 178 · Location 3867
‘ Because I don’t shake hands with my footman , and my footman is a hundred times better . ’ ‘ What a reactionary you are , though ! What about the merging of the classes ? ’ said Oblonsky . ‘ Whoever likes merging is welcome to it . I find it disgusting . ’ ‘ I see , you’re decidedly a reactionary . ’ ‘ Really , I’ve never thought about what I am . I’m Konstantin Levin , nothing more . ’
Highlight (yellow) - XVII > Page 179 · Location 3879
To live with largesse is a nobleman’s business , which only noblemen know how to do . Now muzhiks are buying up the land around us . That doesn’t upset me - the squire does nothing , the muzhik works and pushes out the idle man . It ought to be so . And I’m very glad for the muzhik . But it upsets me to see this impoverishment as a result of - I don’t know what to call it - innocence .
Highlight (yellow) - XVII > Page 179 · Location 3899
‘ Yes , electric light , ’ said Levin . ‘ Yes . Well , and where is Vronsky now ? ’ he said , suddenly putting down the soap .
Highlight (yellow) - XVII > Page 179 · Location 3902
And you know , Kostya , I’ll tell you the truth , ’ he continued , leaning his elbow on the table and resting on his hand his handsome , ruddy face , from which two unctuous , kindly and sleepy eyes shone like stars .
Highlight (yellow) - XVII > Page 180 · Location 3911
‘ Wait , wait , ’ he began , interrupting Oblonsky . ‘ Aristocratism , you say . But allow me to ask , what makes up this aristocratism of Vronsky or whoever else it may be - such aristocratism that I can be scorned ? You consider Vronsky an aristocrat , but I don’t . A man whose father crept out of nothing by wiliness , whose mother , God knows who she didn’t have liaisons with . . . No , excuse me , but I consider myself an aristocrat and people like myself , who can point to three or four honest generations in their families ’ past , who had a high degree of education ( talent and intelligence are another thing ) , and who never lowered themselves before anyone , never depended on anyone , as my father lived , and my grandfather .
Highlight (yellow) - XVIII > Page 181 · Location 3939
and the majority of the young men envied him precisely for what was most difficult in his love , for Karenin’s high position and the resulting conspicuousness of this liaison in society .
Highlight (yellow) - XVIII > Page 181 · Location 3941
The majority of young women , envious of Anna and long since weary of her being called righteous , were glad of what they surmised and only waited for the turnabout of public opinion to be confirmed before they fell upon her with the full weight of their scorn . They were already preparing the lumps of mud they would fling at her when the time came . The majority of older and more highly placed people were displeased by this impending social scandal .
Highlight (yellow) - XVIII > Page 181 · Location 3944
Vronsky’s mother , on learning of his liaison , was pleased at first - both because nothing , to her mind , gave the ultimate finish to a brilliant young man like a liaison in high society , and because Anna , whom she had liked so much , who had talked so much about her son , was after all just like all other beautiful and decent women , to Countess Vronsky’s mind . But recently she had learned that her son had refused a post offered to him and important for his career , only in order to stay in the regiment and be able to see Anna , had learned that highly placed people were displeased with him for that , and had changed her opinion .
Highlight (yellow) - XVIII > Page 181 · Location 3949
Nor did she like it that , judging by all she had learned of this liaison , it was not a brilliant , graceful society liaison , of which she would have approved , but some sort of desperate Wertherian25 passion , as she had been told , which might draw him into foolishness .
Highlight (yellow) - XVIII > Page 181 · Location 3952
The elder brother was also displeased with the younger . He did not care what sort of love it was , great or small , passionate or unpassionate , depraved or not depraved ( he himself , though he had children , kept a dancer , and was therefore indulgent about such things ) ; but he knew that this love displeased those whose good pleasure was necessary , and he therefore disapproved of his brother’s behaviour .
Highlight (yellow) - XIX > Page 184 · Location 3998
Yashvin , a gambler , a carouser , a man not merely without any principles , but with immoral principles - Yashvin was Vronsky’s best friend in the regiment .
Highlight (yellow) - XIX > Page 185 · Location 4014
And the conversation turned to the expectations of the day’s race , which was all Vronsky was able to think about .
Highlight (yellow) - XX > Page 186 · Location 4021
Vronsky stood in the spacious and clean Finnish cottage , which was divided in two . Petritsky shared quarters with him in camp as well . Petritsky was asleep when Vronsky and Yashvin entered the cottage .
Highlight (yellow) - XX > Page 187 · Location 4072
‘ You should get your hair cut , it’s too heavy , especially on the bald spot . ’ Vronsky was indeed beginning to lose his hair prematurely on top . He laughed merrily , showing his solid row of teeth , pulled his peaked cap over his bald spot , went out and got into the carriage .
Highlight (yellow) - XXI > Page 189 · Location 4099
Vronsky not only felt that he had enough ‘ pluck ’ - that is , energy and boldness - but , what was much more important , he was firmly convinced that no one in the world could have more of this ‘ pluck ’ than he had .
Highlight (yellow) - XXI > Page 190 · Location 4111
But she possessed in the highest degree a quality that made one forget all shortcomings ; this quality was blood , that blood which tells , as the English say .
Highlight (yellow) - XXI > Page 190 · Location 4114
She was one of those animals who , it seems , do not talk only because the mechanism of their mouths does not permit it .
Note - XXI > Page 190 · Location 4115
Animal language
Highlight (yellow) - XXI > Page 191 · Location 4143
Why does everybody consider it his duty to take care of me ? And why do they pester me ? Because they see that this is something they can’t understand . If it was an ordinary , banal , society liaison , they’d leave me in peace . They feel that this is something else , that this is not a game , this woman is dearer to me than life .
Highlight (yellow) - XXI > Page 191 · Location 4147
‘ No , they have to teach us how to live . They’ve got no idea what happiness is , they don’t know that without this love there is no happiness or unhappiness for us - there is no life , ’ he thought .
Note - XXI > Page 191 · Location 4148
Love life happiness
Highlight (yellow) - XXI > Page 191 · Location 4149
He was angry with everybody for their interference precisely because in his soul he felt that they , all of them , were right .
Highlight (yellow) - XXI > Page 191 · Location 4154
He vividly remembered all those oft - repeated occasions of the necessity for lying and deceit , which were so contrary to his nature ; he remembered especially vividly the feeling of shame he had noticed in her more than once at this necessity for deceit and lying . And he experienced a strange feeling that had sometimes come over him since his liaison with Anna . This was a feeling of loathing for something - whether for Alexei Alexandrovich , or for himself , or for the whole world , he did not quite know . But he always drove this strange feeling away . And now , rousing himself , he continued his train of thought .
Note - XXI > Page 191 · Location 4158
Dishonesty
Highlight (yellow) - XXI > Page 192 · Location 4160
And for the first time the clear thought occurred to him that it was necessary to stop this lie , and the sooner the better . ‘ To drop everything , both of us , and hide ourselves away somewhere with our love , ’ he said to himself .
Highlight (yellow) - XXII > Page 193 · Location 4176
He was already going up the low steps of the terrace , placing his whole foot on each step to avoid making noise , when he suddenly remembered something that he always forgot and that constituted the most painful side of his relations with her - her son , with his questioning and , as it seemed to him , hostile look .
Highlight (yellow) - XXII > Page 193 · Location 4178
This boy was a more frequent hindrance to their relations than anyone else .
Highlight (yellow) - XXII > Page 193 · Location 4186
With a child’s sensitivity to any show of feelings , he saw clearly that his father , his governess , his nanny - all of them not only disliked Vronsky , but looked at him with disgust and fear , though they never said anything about him , while his mother looked at him as at a best friend .
Highlight (yellow) - XXII > Page 194 · Location 4190
The child’s presence always and inevitably provoked in Vronsky that strange feeling of groundless loathing he had been experiencing lately . It provoked in Vronsky and Anna a feeling like that of a mariner who can see by his compass that the direction in which he is swiftly moving diverges widely from his proper course , but that he is powerless to stop the movement which every moment takes him further and further from the right direction , and that to admit the deviation to himself is the same as admitting disaster .
Note - XXII > Page 194 · Location 4194
Child
Highlight (yellow) - XXII > Page 194 · Location 4208
‘ Forgive me for coming , but I couldn’t let the day pass without seeing you , ’ he went on in French , as he always did , avoiding the impossible coldness of formal Russian and the danger of the informal .
Highlight (yellow) - XXII > Page 194 · Location 4212
She was telling the truth . Whenever , at whatever moment , she might be asked what she was thinking about , she could answer without mistake : about the same thing , about her happiness and her unhappiness .
Highlight (yellow) - XXII > Page 195 · Location 4224
‘ No , I will never forgive him if he doesn’t understand all the significance of it . Better not to tell . Why test him ? ’ she thought , gazing at him in the same way and feeling that her hand holding the leaf was trembling more and more .
Highlight (yellow) - XXII > Page 195 · Location 4226
‘ For God’s sake ! ’ he repeated , taking her hand . ‘ Shall I tell you ? ’ ‘ Yes , yes , yes . . . ’ ‘ I’m pregnant , ’ she said softly and slowly .
Highlight (yellow) - XXII > Page 195 · Location 4236
‘ Yes , ’ he said , resolutely going up to her . ‘ Neither of us has looked on our relation as a game , and now our fate is decided . It’s necessary to end , ’ he said , looking around , ‘ the lie we live in . ’
Highlight (yellow) - XXII > Page 196 · Location 4243
‘ There’s a way out of every situation . A decision has to be made , ’ he said . ‘ Anything’s better than the situation you are living in . I can see how you suffer over everything , over society , and your son , and your husband . ’ ‘ Ah , only not my husband , ’ she said with a simple smile . ‘ I don’t know him , I don’t think about him . He doesn’t exist . ’
Highlight (yellow) - XXIII > Page 197 · Location 4250
Vronsky had already tried several times , though not as resolutely as now , to bring her to a discussion of her situation , and each time had run into that superficiality and lightness of judgement with which she now responded to his challenge . It was as if there were something in it that she could not or would not grasp , as if the moment she began talking about it , she , the real Anna , withdrew somewhere into herself and another woman stepped forward , strange and alien to him , whom he did not love but feared , and who rebuffed him . But today he ventured to say everything .
Highlight (yellow) - XXIII > Page 197 · Location 4259
And a wicked light lit up in her eyes , which a moment before had been tender . ‘ “ Ah , madam , so you love another man and have entered into a criminal liaison with him ? ” ’ ( Impersonating her husband , she stressed the word ‘ criminal ’ , just as Alexei Alexandrovich would have done . ) “ ‘ I warned you about the consequences in their religious , civil and familial aspects . You did not listen to me . Now I cannot lend my name to disgrace . . . ” ’ - ‘ nor my son’s , ’ she was going to say , but she could not joke about her son - ’ “ lend my name to disgrace , ” and more of the same , ’ she added .
Highlight (yellow) - XXIII > Page 197 · Location 4265
He’s not a man , he’s a machine , and a wicked machine when he gets angry , ’ she added , recalling Alexei Alexandrovich in all the details of his figure , manner of speaking and character , holding him guilty for everything bad she could find in him and forgiving him nothing , on account of the terrible fault for which she stood guilty before him .
Highlight (yellow) - XXIII > Page 197 · Location 4274
Again she was going to say ‘ my son ’ , but could not utter the word .
Highlight (yellow) - XXIII > Page 198 · Location 4276
When she thought of her son and his future attitude towards the mother who had abandoned his father , she felt so frightened at what she had done that she did not reason , but , like a woman , tried only to calm herself with false reasonings and words , so that everything would remain as before and she could forget the terrible question of what would happen with her son .
Highlight (yellow) - XXIII > Page 198 · Location 4290
‘ I’m unhappy ? ’ she said , coming close to him and looking at him with a rapturous smile of love . ‘ I’m like a starving man who has been given food . Maybe he’s cold , and his clothes are torn , and he’s ashamed , but he’s not unhappy . I’m unhappy ? No , this is my happiness . . . ’
Note - XXIII > Page 198 · Location 4292
Love happines
Highlight (yellow) - XXIV > Page 200 · Location 4327
Vronsky cast a glance once more over the exquisite , beloved forms of the horse , whose whole body was trembling , and tearing himself with difficulty from this sight , walked out of the shed .
Highlight (yellow) - XXIV > Page 200 · Location 4351
Alexei Vronsky’s frowning face paled and his jutting lower jaw twitched , something that seldom happened to him . Being a man with a very kind heart , he seldom got angry , but when he did , and when his chin twitched , he could be dangerous , as his brother knew . Alexander Vronsky smiled gaily .
Highlight (yellow) - XXIV > Page 201 · Location 4380
Prince Kuzovlev sat pale on his thoroughbred mare from Grabov’s stud , while an Englishman led her by the bridle . Vronsky and all his comrades knew Kuzovlev and his peculiarity of ‘ weak ’ nerves and terrible vanity . They knew that he was afraid of everything , afraid of riding an army horse ; but now , precisely because it was scary , because people broke their necks , and because by each obstacle there was a doctor , an ambulance wagon with a cross sewn on it and a sister of mercy , he had decided to ride .
Highlight (yellow) - XXV > Page 204 · Location 4426
The big barrier stood right in front of the tsar’s pavilion . The emperor , and the entire court , and throngs of people - all were looking at them , at him and at Makhotin , who kept one length ahead of him , as they approached the devil ( as the solid barrier was called ) .
Highlight (yellow) - XXV > Page 204 · Location 4448
There remained one obstacle , the most difficult ; if he got over it ahead of the others , he would come in first . He was riding towards the Irish bank . Together with Frou - Frou he could already see this bank in the distance , and the two together , he and his horse , had a moment’s doubt . He noticed some indecision in the horse’s ears and raised his whip , but felt at once that his doubt was groundless : the horse knew what was needed . She increased her speed and measuredly , exactly as he had supposed , soared up , pushing off from the ground and giving herself to the force of inertia , which carried her far beyond the ditch ; and in the same rhythm , effortlessly , in the same step , Frou - Frou continued the race .
Highlight (yellow) - XXV > Page 205 · Location 4461
She flew over the ditch as if without noticing it ; she flew over it like a bird ; but just then Vronsky felt to his horror that , having failed to keep up with the horse’s movement , he , not knowing how himself , had made a wrong , an unforgivable movement as he lowered himself into the saddle .
Highlight (yellow) - XXV > Page 205 · Location 4466
The awkward movement Vronsky had made had broken her back . But he understood that much later . Now he saw only that Makhotin was quickly drawing away , while he , swaying , stood alone on the muddy , unmoving ground , and before him , gasping heavily , lay Frou - Frou , her head turned to him , looking at him with her lovely eye .
Highlight (yellow) - XXV > Page 205 · Location 4472
‘ A - a - ah ! ’ groaned Vronsky , clutching his head . ‘ A - a - ah , what have I done ! ’ he cried . ‘ The race is lost ! And it’s my own fault - shameful , unforgivable ! And this poor , dear , destroyed horse ! A - a - ah , what have I done ! ’
Highlight (yellow) - XXV > Page 205 · Location 4475
The horse had broken her back and they decided to shoot her .
Highlight (yellow) - XXV > Page 205 · Location 4477
He felt miserable . For the first time in his life he had experienced a heavy misfortune , a misfortune that was irremediable and for which he himself was to blame . Yashvin overtook him with the cap , brought him home , and a half hour later Vronsky came to his senses . But the memory of this race remained in his soul for a long time as the most heavy and painful memory of his life .
Highlight (yellow) - XXVI > Page 207 · Location 4491
He who was so intelligent and subtle in official business , did not understand all the madness of such an attitude towards his wife . He did not understand it , because it was too dreadful for him to recognize his real position , and in his soul he closed , locked and sealed the drawer in which he kept his feelings for his family - that is , his wife and son . He who had been an attentive father had become especially cold towards his son since the end of that winter , and took the same bantering attitude towards him as towards his wife . ‘ Ah ! young man ! ’ was the way he addressed him .
Highlight (yellow) - XXVI > Page 207 · Location 4495
Alexei Alexandrovich thought and said that he had never had so much official business in any other year as he had that year ; but he did not realize that he had invented things for himself to do that year , that this was one way of not opening the drawer where his feelings for his wife and family and his thoughts about them lay , becoming more dreadful the longer they lay there .
Highlight (yellow) - XXVI > Page 207 · Location 4503
This year Countess Lydia Ivanovna refused to live in Peterhof , never once visited Anna Arkadyevna , and hinted to Alexei Alexandrovich at the awkwardness of Anna’s closeness to Betsy and Vronsky . Alexei Alexandrovich sternly interrupted her , expressing the thought that his wife was above suspicion , and after that he began to avoid Countess Lydia Ivanovna . He did not want to see , and did not see , that in society many were already looking askance at his wife ; he did not want to understand , and did not understand , why his wife insisted especially on moving to Tsarskoe , where Betsy lived , which was not far from the camp of Vronsky’s regiment . He did not allow himself to think of it , and did not think of it ; but , nevertheless , in the depths of his soul , without ever saying it to himself and having not only no proofs of it but even no suspicions , he knew without doubt that he was a deceived husband , and it made him deeply unhappy .
Note - XXVI > Page 208 · Location 4509
Psychology
Highlight (yellow) - XXVI > Page 208 · Location 4515
The day of the races was a very busy day for Alexei Alexandrovich ; but , having made a schedule for himself that morning , he decided that immediately after an early dinner he would go to see his wife at their country house and from there to the races , which the whole court would attend and which he , too , had to attend . He would visit his wife , because he had decided to see her once a week for propriety’s sake . Besides , according to the established rule , that day being the fifteenth , he had to give her money for her expenses .
Highlight (yellow) - XXVII > Page 210 · Location 4558
Does he mean to spend the night ? ’ she thought , and all that might come of it seemed to her so terrible and frightening that , without a moment’s thought , she went out to meet them with a gay and radiant face and , feeling in herself the presence of the already familiar spirit of lying and deceit , at once surrendered to it and began talking without knowing herself what she was going to say .
Highlight (yellow) - XXVII > Page 210 · Location 4569
She spoke very simply and naturally , but too much and too quickly . She felt it herself , the more so as , in the curious glance that Mikhail Vassilyevich gave her , she noticed that he seemed to be observing her .
Highlight (yellow) - XXVII > Page 211 · Location 4580
Seryozha came in , preceded by the governess . If Alexei Alexandrovich had allowed himself to observe , he would have noticed the timid , perplexed look with which Seryozha glanced first at his father , then at his mother . But he did not want to see anything , and did not see anything .
Highlight (yellow) - XXVII > Page 211 · Location 4584
, but now , since Alexei Alexandrovich had started calling him young man and since the riddle about whether Vronsky was friend or foe had entered his head , he shrank from his father . As if asking for protection , he looked at his mother . He felt good only with her . Alexei Alexandrovich , talking meanwhile with the governess , held his son by the shoulder , and Seryozha felt so painfully awkward that Anna saw he was about to cry .
Highlight (yellow) - XXVII > Page 211 · Location 4600
‘ Well , good - bye then . You’ll come for tea , that’s splendid ! ’ she said and walked out , radiant and gay . But as soon as she no longer saw him , she felt the place on her hand that his lips had touched and shuddered with revulsion .
Highlight (yellow) - XXVIII > Page 212 · Location 4608
She knew all his ways and they were all disgusting to her . ‘ Nothing but ambition , nothing but the wish to succeed - that’s all there is in his soul , ’ she thought , ‘ and lofty considerations , the love of learning , religion , are all just means to success . ’
Highlight (yellow) - XXVIII > Page 212 · Location 4623
‘ I’m a bad woman , I’m a ruined woman , ’ she thought , ‘ but I don’t like to lie , I can’t bear lying , and lying is food for him ’ ( her husband ) . ‘ He knows everything , he sees everything ; what does he feel , then , if he can talk so calmly ? If he were to kill me , if he were to kill Vronsky , I would respect him . But no , he needs only lies and propriety , ’ Anna said to herself , not thinking of precisely what she wanted from her husband or how she wanted to see him . Nor did she understand that Alexei Alexandrovich’s particular loquacity that day , which so annoyed her , was only the expression of his inner anxiety and uneasiness . As a child who has hurt himself jumps about in order to move his muscles and stifle the pain , so for Alexei Alexandrovich mental movement was necessary in order to stifle those thoughts about his wife , which in her presence and that of Vronsky , and with his name constantly being repeated , clamoured for his attention . And as it is natural for a child to jump , so it was natural for him to speak well and intelligently . He said :
Highlight (yellow) - XXVIII > Page 213 · Location 4636
‘ Let’s suppose , Princess , that it is not superficial , ’ he said , ‘ but internal . But that is not the point , ’ and he again turned to the general , with whom he was speaking seriously . ‘ Don’t forget that racing is for military men , who have chosen that activity , and you must agree that every vocation has its reverse side of the coin . It’s a military man’s duty . The ugly sport of fist fighting or of the Spanish toreadors is a sign of barbarism . But a specialized sport is a sign of development . ’
Highlight (yellow) - XXVIII > Page 213 · Location 4648
‘ There are two sides , ’ Alexei Alexandrovich went on again , sitting down , ‘ the performers and the spectators ; and the love of such spectacles is the surest sign of low development in the spectators , I agree , but . . . ’ ‘ A bet , Princess ! ’ the voice of Stepan Arkadyich came from below , addressing Betsy . ‘ Who are you backing ? ’
Highlight (yellow) - XXVIII > Page 214 · Location 4660
‘ Yes , that lady and the others are also very upset , ’ Alexei Alexandrovich said to himself . He wanted not to look at her , but his glance was involuntarily drawn to her . He peered into that face again , trying not to read what was so clearly written on it , and against his will read on it with horror what he did not want to know .
Highlight (yellow) - XXVIII > Page 214 · Location 4670
The race was unlucky : out of seventeen men more than half fell and were injured . Towards the end of the race everyone was in agitation , which was increased still more by the fact that the emperor was displeased .
Highlight (yellow) - XXIX > Page 215 · Location 4675
But after that a change came over Anna’s face which was positively improper . She was completely at a loss . She started thrashing about like a trapped bird , now wanting to get up and go somewhere , now turning to Betsy .
Highlight (yellow) - XXIX > Page 215 · Location 4686
‘ I once again offer you my arm , if you want to go , ’ said Alexei Alexandrovich , touching her arm . She recoiled from him in revulsion and , without looking at his face , replied : ‘ No , no , let me be , I’ll stay . ’
Highlight (yellow) - XXIX > Page 216 · Location 4700
On the way out of the pavilion , Alexei Alexandrovich , as always , talked with people he met , and Anna also had , as always , to respond and talk ; but she was not herself and walked at her husband’s side as if in a dream .
Highlight (yellow) - XXIX > Page 216 · Location 4703
Despite all he had seen , Alexei Alexandrovich still did not allow himself to think of his wife’s real situation . He saw only the external signs . He saw that she had behaved improperly and considered it his duty to tell her so . Yet it was very hard for him not to say more , but to say just that .
Highlight (yellow) - XXIX > Page 216 · Location 4712
‘ In what way did I behave improperly ? ’ she said loudly , quickly turning her head to him and looking straight into his eyes , now not at all with the former deceptive gaiety , but with a determined look , behind which she barely concealed the fear she felt .
Highlight (yellow) - XXIX > Page 216 · Location 4718
have asked you before to conduct yourself in society so that wicked tongues can say nothing against you . There was a time when I spoke of our inner relations ; now I am not speaking of them . Now I am speaking of our external relations . You conducted yourself improperly , and I do not wish it to be repeated . ’
Highlight (yellow) - XXIX > Page 216 · Location 4726
Now , when the disclosure of everything was hanging over him , he wished for nothing so much as that she would mockingly answer him , just as before , that his suspicions were ridiculous and had no grounds . So dreadful was what he knew , that he was now ready to believe anything . But the expression of her face , frightened and gloomy , did not promise even deceit .
Highlight (yellow) - XXIX > Page 217 · Location 4730
‘ No , you are not mistaken , ’ she said slowly , looking desperately into his cold face . ‘ You are not mistaken . I was and could not help being in despair . I listen to you and think about him . I love him , I am his mistress , I cannot stand you , I’m afraid of you , I hate you . . . Do what you like with me . ’
Highlight (yellow) - XXIX > Page 217 · Location 4734
But his entire face suddenly acquired the solemn immobility of a dead man , and that expression did not change during the whole drive to their country house . As they approached the house , he turned his head to her with the same expression . ‘ So be it ! But I demand that the outward conventions of propriety be observed until ’ - his voice trembled - ‘ until I take measures to secure my honour and inform you of them . ’
Highlight (yellow) - XXIX > Page 217 · Location 4742
‘ My God , what light ! It’s frightening , but I love seeing his face and love this fantastic light . . . My husband ! Ah , yes . . . Well , thank God it’s all over with him . ’
Highlight (yellow) - XXX > Page 218 · Location 4745
As in all places where people gather , so in the small German watering - place to which the Shcherbatskys came there occurred the usual crystallization , as it were , of society , designating for each of its members a definite and invariable place . As definitely and invariably as a particle of water acquires the specific form of a snowflake in freezing , so each new person arriving at the spa was put at once into the place appropriate for him .
Note - XXX > Page 218 · Location 4748
Society
Highlight (yellow) - XXX > Page 218 · Location 4767
The Russian girl looked after Mme Stahl and , besides that , as Kitty noticed , made friends with all the gravely ill , of whom there were many at the spa , and looked after them in the most natural way . This Russian girl , from Kitty’s observation , was not related to Mme Stahl and at the same time was not a hired helper . Mme Stahl called her Varenka , and the others ‘ Mile Varenka ’ . Not only was Kitty interested in observing the relations of this girl with Mme Stahl and other persons unknown to her , but , as often happens , she felt an inexplicable sympathy for this Mile Varenka and sensed , when their eyes met , that she , too , was liked .
Highlight (yellow) - XXX > Page 219 · Location 4772
This Mlle Varenka was not really past her first youth , but was , as it were , a being without youth : she might have been nineteen , she might have been thirty .
Highlight (yellow) - XXX > Page 219 · Location 4775
She was like a beautiful flower which , while still full of petals , is scentless and no longer blooming . Besides that , she also could not be attractive to men because she lacked what Kitty had in over - abundance - the restrained fire of life and an awareness of her attractiveness .
Note - XXX > Page 219 · Location 4777
Beauty
Highlight (yellow) - XXX > Page 219 · Location 4791
But the princess , learning from the Kurlistem that they were Nikolai Levin and Marya Nikolaevna , explained to Kitty what a bad man this Levin was , and all her dreams about these two persons vanished .
Highlight (yellow) - XXXII > Page 223 · Location 4857
The child died at once , and Mme Stahl’s family , knowing her susceptibility and fearing the news might kill her , replaced the baby , taking the daughter of a court cook born the same night and in the same house in Petersburg . This was Varenka . Mme Stahl learned later that Varenka was not her daughter , but continued to bring her up , the more so as Varenka soon afterwards had no family left .
Highlight (yellow) - XXXII > Page 224 · Location 4880
Kitty looked at her friend with pride . She admired her art , and her voice , and her face , but most of all she admired her manner , the fact that Varenka evidently did not think much of her singing and was perfectly indifferent to praise ; she seemed to ask only : must I sing more , or is that enough ?
Highlight (yellow) - XXXII > Page 224 · Location 4882
‘ If it were me , ’ Kitty thought to herself , ‘ how proud I’d be ! How I’d rejoice , looking at this crowd by the windows ! And she is perfectly indifferent . She is moved only by the wish not to say no and to do something nice for maman .
Highlight (yellow) - XXXII > Page 224 · Location 4898
loved him and he loved me ; but his mother didn’t want it , and he married someone else . He lives not far from us now , and I sometimes meet him . You didn’t think that I , too , could have a love story ? ’ she said , and in her beautiful face there barely glimmered that fire which , Kitty felt , had once lit up her whole being .
Highlight (yellow) - XXXII > Page 225 · Location 4911
‘ Then he would have acted badly , and I would not feel sorry about him , ’ Varenka replied , obviously understanding that it was now a matter not of her but of Kitty . ‘ But the insult ? ’ said Kitty . ‘ It’s impossible to forget an insult , impossible , ’ she said , remembering how she had looked at him at the last ball when the music stopped . ‘ Where is the insult ? Did you do anything bad ? ’ ‘ Worse than bad - shameful . ’
Note - XXXII > Page 225 · Location 4915
Shame
Highlight (yellow) - XXXII > Page 225 · Location 4919
‘ So what then ? I don’t understand . The point is whether you love him now or not , ’ said Varenka , calling everything by its name . ‘ I hate him ; I can’t forgive myself . ’ ‘ So what then ? ’ ‘ The shame , the insult . ’
Highlight (yellow) - XXXII > Page 225 · Location 4922
‘ Ah , if everybody was as sensitive as you are ! ’ said Varenka . ‘ There’s no girl who hasn’t gone through that . And it’s all so unimportant . ’ ‘ Then what is important ? ’ asked Kitty , peering into her face with curious amazement . ‘ Ah , many things are important , ’ Varenka said , smiling . ‘ But what ? ’ ‘ Ah , many things are more important , ’ Varenka replied , not knowing what to say . But at that moment the princess’s voice came from the window :
Highlight (yellow) - XXXII > Page 225 · Location 4930
Kitty held her by the hand and with passionate curiosity and entreaty her eyes asked : ‘ What is it , what is this most important thing that gives such tranquillity ? You know , tell me ! ’ But Varenka did not even understand what Kitty’s eyes were asking her . All she remembered was that she still had to stop and see Mme Berthe and be in time for tea with maman at twelve . She went in , collected her music and , having said good - bye to everyone , was about to leave .
Highlight (yellow) - XXXII > Page 226 · Location 4936
‘ No , I always go alone and nothing ever happens to me , ’ she said , taking her hat . And , kissing Kitty once more and never saying what was important , at a brisk pace , with the music under her arm , she vanished into the semi - darkness of the summer night , taking with her the secret of what was important and what gave her that enviable tranquillity and dignity .
Highlight (yellow) - XXXIII > Page 227 · Location 4940
Kitty made the acquaintance of Mme Stahl as well , and this acquaintance , together with her friendship for Varenka , not only had great influence on her , but comforted her in her grief . The comfort lay in the fact that , thanks to this acquaintance , a completely new world was opened to her which had nothing in common with her past : a lofty , beautiful world , from the height of which she could calmly look over that past . It was revealed to her that , besides the instinctive life to which Kitty had given herself till then , there was a spiritual life . This life was revealed by religion , but a religion that had nothing in common with the one Kitty had known from childhood and which found expression in the liturgy and vigils at the Widows ’ Home , 31 where one could meet acquaintances , and in learning Slavonic32 texts by heart with a priest ; it was a lofty , mysterious religion , bound up with a series of beautiful thoughts and feelings which one could not only believe in because one was told to , but could also love .
Note - XXXIII > Page 227 · Location 4947
Religion spirituality
Highlight (yellow) - XXXIII > Page 227 · Location 4950
Yet in her every movement , in every word , in every heavenly glance , as Kitty put it , especially in the whole story of her life , which she knew from Varenka , in everything , Kitty learned ‘ what was important ’ , which till then she had not known .
Highlight (yellow) - XXXIII > Page 227 · Location 4954
She noticed that , when asking about her family , Mme Stahl smiled contemptuously , which was contrary to Christian kindness . She also noticed that when she found a Catholic priest with her , Mme Stahl carefully kept her face in the shadow of a lampshade and smiled peculiarly . However negligible these two observations were , they troubled her , and she doubted Mme Stahl .
Highlight (yellow) - XXXIII > Page 227 · Location 4957
From Varenka she understood that you had only to forget yourself and love others and you would be calm , happy and beautiful .
Note - XXXIII > Page 227 · Location 4958
Ethics
Highlight (yellow) - XXXIII > Page 227 · Location 4960
From Varenka’s stories about what Mme Stahl and the others she mentioned did , Kitty made herself a plan for her future life . Just like Mme Stahl’s niece , Aline , of whom Varenka had told her so much , wherever she lived she would seek out the unfortunate people , help them as much as possible , distribute the Gospel , read the Gospel to the sick , the criminal , the dying . The thought of reading the Gospel to criminals , as Aline did , especially attracted Kitty . But these were all secret thoughts which Kitty did not speak about either to her mother or to Varenka .
Highlight (yellow) - XXXIII > Page 228 · Location 4976
But her daughter said nothing in reply ; she only thought in her heart that one could not speak of excessiveness in matters of Christianity . What excessiveness could there be in following a teaching that tells you to turn the other cheek when you have been struck , and to give away your shirt when your caftan is taken ?
Highlight (yellow) - XXXIII > Page 228 · Location 4990
Kitty replied that there had been nothing between them , and that she decidedly did not understand why Anna Pavlovna seemed displeased with her . Kitty’s reply was perfectly truthful . She did not know the reason for Anna Pavlovna’s change towards her , but she guessed it . Her guess was something she could not tell her mother any more than she could tell it to herself . It was one of those things that one knows but cannot even tell oneself - so dreadful and shameful it would be to be mistaken .
Highlight (yellow) - XXXIII > Page 229 · Location 4999
She remembered her own efforts at first to overcome the revulsion she felt for him , as for all the consumptives , and her attempts to think of something to say to him .
Highlight (yellow) - XXXIII > Page 229 · Location 5010
This doubt poisoned the charm of her new life .
Highlight (yellow) - XXXIV > Page 230 · Location 5015
The prince , on the contrary , found everything abroad vile and European life a burden , kept to his Russian habits and deliberately tried to show himself as less of a European than he really was .
Highlight (yellow) - XXXIV > Page 231 · Location 5049
Kitty saw that he wanted to make fun of Varenka , but that he simply could not do it , because he liked her .
Highlight (yellow) - XXXIV > Page 231 · Location 5052
‘ Did you know her before , papa ? ’ Kitty asked in fear , noticing a flicker of mockery lighting up in the prince’s eyes at the mention of Mme Stahl . ‘ I knew her husband , and her a little , back before she signed up with the Pietists . 34
Highlight (yellow) - XXXIV > Page 231 · Location 5054
‘ What is a Pietist , papa ? ’ asked Kitty , already frightened by the fact that what she valued so highly in Mme Stahl had a name .
Highlight (yellow) - XXXIV > Page 233 · Location 5110
‘ Maybe , ’ he said , pressing her arm with his elbow . ‘ But it’s better to do it so that , if you ask , nobody knows . ’
Highlight (yellow) - XXXIV > Page 233 · Location 5115
There remained only a stubby - legged woman who stayed lying down because of her bad figure and tormented the docile Varenka for not tucking in her rug properly . And by no effort of imagination could she bring back the former Mme Stahl .
Highlight (yellow) - XXXV > Page 234 · Location 5129
The good - natured Marya Evgenyevna rocked with laughter at everything amusing that the prince said , and Varenka - something Kitty had not seen before - melted into weak but infectious laughter , provoked in her by the prince’s witticisms .
Highlight (yellow) - XXXV > Page 234 · Location 5134
Everyone was merry , but Kitty was unable to be merry , and this pained her still more . She had the same feeling as in childhood , when she was punished by being locked in her room and heard her sisters ’ merry laughter .
Highlight (yellow) - XXXV > Page 235 · Location 5144
‘ What’s so interesting ? They’re all pleased as Punch : they’ve beaten everybody . 35 Well , but what’s there for me to be pleased about ? I didn’t beat anybody , I just have to take my boots off myself and put them outside the door myself . In the morning I get up , dress myself at once , go downstairs and drink vile tea . Home is quite another thing ! You wake up without hurrying , get angry at something , grumble a little , come properly to your senses , think things over , don’t have to hurry . ’
Highlight (yellow) - XXXV > Page 236 · Location 5178
‘ It serves me right because it was all pretence , because it was all contrived and not from the heart . What did I have to do with some stranger ? And it turned out that I caused a quarrel and that I did what nobody asked me to do . Because it was all pretence ! pretence ! pretence ! . . . ’ ‘ But what was the purpose of pretending ? ’ Varenka said softly . ‘ Oh , how vile and stupid ! There was no need at all . . . It was all pretence ! . . . ’ she said , opening and closing the parasol . ‘ But for what purpose ? ’ ‘ So as to seem better to people , to myself , to God - to deceive everyone . No , I won’t fall into that any more ! Be bad , but at least don’t be a liar , a deceiver ! ’
Note - XXXV > Page 236 · Location 5184
Deception
Highlight (yellow) - XXXV > Page 236 · Location 5190
‘ It’s all not it . I can only live by my heart , and you live by rules . I loved you simply , but you probably only so as to save me , to teach me ! ’ ‘ You’re unfair , ’ said Varenka . ‘ But I’m not talking about others , I’m talking about myself . ’ ‘ Kitty ! ’ came her mother’s voice . ‘ Come here , show Papa your corals . ’
Highlight (yellow) - XXXV > Page 237 · Location 5203
Peace was made . But with the arrival of her father that whole world in which Kitty had been living changed for her . She did not renounce all that she had learned , but she understood that she had deceived herself in thinking that she could be what she wished to be . It was as if she came to her senses ; she felt all the difficulty of keeping herself , without pretence and boastfulness , on that level to which she had wished to rise ; besides , she felt all the weight of that world of grief , sickness and dying people in which she had been living ; the efforts she had made to force herself to love it seemed tormenting to her , and she wished all the sooner to go to the fresh air , to Russia , to Yergushovo , where , as she learned from a letter , her sister Dolly had already moved with the children .
Part Three
Highlight (blue) - I > Page 239 · Location 5220
For Konstantin Levin the country was the place of life , that is , of joy , suffering , labour ; for Sergei Ivanovich the country was , on the one hand , a rest from work and , on the other , an effective antidote to corruption , which he took with pleasure and an awareness of its effectiveness . For Konstantin Levin the country was good in that it presented a field for labour that was unquestionably useful ; for Sergei Ivanovich the country was especially good because there one could and should do nothing .
Note - I > Page 239 · Location 5224
Country perspective
Highlight (blue) - I > Page 239 · Location 5227
For Konstantin the peasantry was simply the chief partner in the common labour , and , despite all his respect and a sort of blood - love for the muzhiks that he had probably sucked in , as he himself said , with the milk of his peasant nurse , he , as partner with them in the common cause , while sometimes admiring the strength , meekness and fairness of these people , very often , when the common cause demanded other qualities , became furious with them for their carelessness , slovenliness , drunkenness and lying .
Highlight (blue) - I > Page 239 · Location 5232
But it was impossible for him to love or not love the peasantry as something special , because not only did he live with them , not only were all his interests bound up with theirs , but he considered himself part of the peasantry , did not see any special qualities or shortcomings in himself or in them , and could not contrast himself to them .
Highlight (blue) - I > Page 239 · Location 5239
Sergei Ivanovich did the contrary . Just as he loved and praised country life in contrast to the life he did not love , so he loved the peasantry in contrast to the class of people he did not love , and so he knew the peasantry as something in contrast to people in general . In his methodical mind certain forms of peasant life acquired a clear shape , deduced in part from peasant life itself , but mainly from this contrast . He never changed his opinion about the peasantry or his sympathetic attitude towards them .
Highlight (blue) - I > Page 240 · Location 5246
For Sergei Ivanovich his younger brother was a nice fellow with a heart well placed ( as he put it in French ) , but with a mind which , though rather quick , was subject to momentary impressions and therefore filled with contradictions . With the condescension of an older brother , he occasionally explained the meaning of things to him , but could find no pleasure in arguing with him , because he beat him too easily .
Highlight (blue) - I > Page 240 · Location 5251
But , in the depths of his soul , the older he became and the more closely he got to know his brother , the more often it occurred to him that this ability to act for the common good , of which he felt himself completely deprived , was perhaps not a virtue but , on the contrary , a lack of something - not a lack of good , honest and noble desires and tastes , but a lack of life force , of what is known as heart , of that yearning which makes a man choose one out of all the countless paths in life presented to him and desire that one alone .
Note - I > Page 240 · Location 5254
Heart possibility
Highlight (blue) - I > Page 240 · Location 5254
The more he knew his brother , the more he noticed that Sergei Ivanovich and many other workers for the common good had not been brought to this love of the common good by the heart , but had reasoned in their minds that it was good to be concerned with it and were concerned with it only because of that . And Levin was confirmed in this surmise by observing that his brother took questions about the common good and the immortality of the soul no closer to heart than those about a game of chess or the clever construction of a new machine .
Highlight (blue) - I > Page 240 · Location 5260
But though he rested now , that is , did not work on his book , he was so used to intellectual activity that he liked to utter in beautifully concise form the thoughts that occurred to him and liked it when there was someone there to listen to him . His most usual and natural listener was his brother . And therefore , despite the friendly simplicity of their relations , Konstantin felt awkward leaving him alone . Sergei Ivanovich liked to stretch out on the grass in the sun and lie there like that , baking and lazily chatting .
Highlight (blue) - I > Page 240 · Location 5267
and they would not screw the shares to the ploughs , but would take them off and then say that iron ploughs were a worthless invention , nothing like the good old wooden plough , and so on .
Highlight (blue) - II > Page 242 · Location 5278
After the doctor’s departure , Sergei Ivanovich expressed a wish to go to the river with a fishing rod . He liked fishing and seemed to take pride in being able to like such a stupid occupation .
Highlight (blue) - II > Page 242 · Location 5291
Konstantin Levin did not like talking or hearing about the beauty of nature . For him words took away the beauty of what he saw . He agreed with his brother , but involuntarily began thinking of other things .
Note - II > Page 242 · Location 5293
Nature Beaty
Highlight (blue) - II > Page 243 · Location 5300
His brother sat down under the bush , sorting his fishing rods , while Levin led the horse away , tied it up , and went into the enormous grey - green sea of the meadow , unstirred by the wind . The silky grass with its ripening seeds reached his waist in the places flooded in spring .
Highlight (blue) - III > Page 244 · Location 5330
‘ Self - esteem , ’ said Levin , cut to the quick by his brother’s words , ‘ is something I do not understand . If I had been told at the university that others understood integral calculus and I did not - there you have self - esteem . But here one should first be convinced that one needs to have a certain ability in these matters and , chiefly , that they are all very important . ’
Highlight (blue) - III > Page 245 · Location 5352
‘ What are you saying ? Can there be any doubt of the usefulness of education ? If it’s good for you , it’s good for everyone . ’ Konstantin Levin felt himself morally driven into a corner and therefore got excited and involuntarily let out the main reason for his indifference to the common cause . ‘ Maybe all that is good , but why should I worry about setting up medical centres that I’ll never use and schools that I won’t send my children to , that the peasants don’t want to send their children to either , and that I have no firm belief that they ought to send them to ? ’ he said .
Highlight (blue) - III > Page 245 · Location 5363
‘ No , ask anybody you like , ’ Konstantin Levin replied resolutely , ‘ a literate peasant is much worse as a worker . And the roads can’t be repaired , and bridges are no sooner put up than they steal them . ’
Note - III > Page 245 · Location 5365
Literacy
Highlight (blue) - III > Page 246 · Location 5378
‘ How do you mean ? ’ ‘ No , since we’re talking , explain it to me from a philosophical point of view , ’ said Levin . ‘ I don’t understand what philosophy has got to do with it , ’ said Sergei Ivanovich , in such a tone , it seemed to Levin , as if he did not recognize his brother’s right to discuss philosophy . And that vexed Levin .
Note - III > Page 246 · Location 5381
Philosophy
Highlight (blue) - III > Page 246 · Location 5381
‘ It’s got this to do with it ! ’ he began hotly . ‘ I think that the motive force of all our actions is , after all , personal happiness . In our present - day zemstvo institutions I , as a nobleman , see nothing that contributes to my well - being . The roads are no better and cannot be better ; my horses carry me over the bad ones as well . I have no need of doctors and centres , I have no need of any justice of the peace - I’ve never turned to one and never will . Schools I not only do not need but also find harmful , as I told you . For me the zemstvo institutions are simply an obligation to pay six kopecks an acre , go to town , sleep with bedbugs , and listen to all sorts of nonsense and vileness , and personal interest does not move me to do that . ’
Note - III > Page 246 · Location 5386
Modernity institutions
Highlight (blue) - III > Page 246 · Location 5388
‘ No ! ’ Konstantin interrupted , growing more heated . ‘ The emancipation of the serfs was a different matter . There was a personal interest . We wanted to throw off the yoke that oppressed us and all good people . But to be a council member , 2 arguing about how many privy cleaners are needed and how the sewer pipes should be installed in a town I don’t live in ; to be a juror and judge a muzhik who has stolen a ham , and listen for six hours to defence lawyers and prosecutors pouring out all sorts of drivel , and hear the foreman of the jury ask my old Alyoshka - the - fool : “ Mister defendant , do you acknowledge the fact of the stolen ham ? ” “ Wha ? ” ’
Note - III > Page 246 · Location 5393
Emancipation of serfs
Highlight (blue) - III > Page 246 · Location 5396
‘ I only mean to say that I will always defend with all my might those rights that I . . . that touch on my interests . When the gendarmes searched us as students and read our letters , I was ready to defend those rights with all my might , to defend my rights to education , to freedom . I understand military service , which touches the future of my children , my brothers and myself . I’m ready to discuss anything that concerns me . But to decide how to dispose of forty thousand in zemstvo funds , or to judge Alyoshka - the - fool - that I do not understand and cannot do . ’
Highlight (blue) - III > Page 247 · Location 5410
‘ I think , ’ said Konstantin , ‘ that no activity can be solid unless it’s based on personal interest . That is a general truth , a philosophical one , ’ he said , resolutely repeating the word ‘ philosophical ’ , as if wishing to show that he , too , had the right , like anyone else , to speak of philosophy .
Note - III > Page 247 · Location 5413
Self-interest
Highlight (blue) - III > Page 247 · Location 5414
‘ Well , you should leave philosophy alone , ’ he said . ‘ The chief task of philosophy in all ages has consisted precisely in finding the connection that necessarily exists between personal and common interests . But that is not the point , the point is that I must correct your comparison . The birches are not stuck in , they are planted or seeded , and they ought to be carefully tended . Only those nations have a future , only those nations can be called historical , that have a sense of what is important and significant in their institutions , and value them . ’
Note - III > Page 247 · Location 5418
History philosophy
Highlight (blue) - IV > Page 248 · Location 5437
‘ And please send my scythe to Titus to be sharpened and brought along tomorrow - perhaps I’ll do some mowing myself , ’ he said , trying not to be embarrassed .
Highlight (blue) - IV > Page 248 · Location 5450
‘ No , I don’t think so ; but it’s such cheerful and at the same time such hard work , that one has no time to think . ’ ‘ But how are you going to have dinner with them ? It’s a bit awkward to send Lafite5 and roast turkey to you out there . ’
Highlight (blue) - IV > Page 249 · Location 5475
‘ Never mind , he’ll get himself set right , ’ the old man went on . ‘ See , there he goes . . . The swath’s too wide , you’ll get tired . . . He’s the owner , never fear , he’s doing his best ! And look at the hired men ! Our kind would get it in the neck for that . ’
Highlight (blue) - IV > Page 250 · Location 5496
Not understanding what it was or where it came from , in the midst of his work he suddenly felt a pleasant sensation of coolness on his hot , sweaty shoulders . He glanced at the sky while his blade was being whetted . A low , heavy cloud had come over it , and big drops of rain were falling . Some muzhiks went for their caftans and put them on ; others , just like Levin , merely shrugged their shoulders joyfully under the pleasant freshness .
Note - IV > Page 250 · Location 5499
Nature
Highlight (blue) - IV > Page 250 · Location 5499
They finished another swath and another . They went through long swaths , short swaths , with bad grass , with good grass . Levin lost all awareness of time and had no idea whether it was late or early . A change now began to take place in his work which gave him enormous pleasure . In the midst of his work moments came to him when he forgot what he was doing and began to feel light , and in those moments his swath came out as even and good as Titus’s . But as soon as he remembered what he was doing and started trying to do better , he at once felt how hard the work was and the swath came out badly .
Note - IV > Page 250 · Location 5503
Reflection
Highlight (blue) - V > Page 252 · Location 5531
The longer Levin mowed , the more often he felt those moments of oblivion during which it was no longer his arms that swung the scythe , but the scythe itself that lent motion to his whole body , full of life and conscious of itself , and , as if by magic , without a thought of it , the work got rightly and neatly done on its own . These were the most blissful moments .
Note - V > Page 252 · Location 5534
Scythe
Highlight (blue) - V > Page 253 · Location 5565
They had done an extraordinary amount of work for forty - two men . The whole of the big meadow , which in the time of the corvée7 used to be mowed in two days by thirty scythes , was already mowed .
Highlight (blue) - V > Page 254 · Location 5592
Easy as it was to mow the wet and tender grass , it was hard going up and down the steep slopes of the gully . But the old man was not hindered by that . Swinging his scythe in the same way , with the small , firm steps of his feet shod in big bast shoes , he slowly climbed up the steep slope , and , despite the trembling of his whole body and of his trousers hanging lower than his shirt , he did not miss a single blade of grass or a single mushroom on his way and joked with the muzhiks and Levin just as before . Levin came after him and often thought that he would surely fall , going up such a steep slope with a scythe , where it was hard to climb even without a scythe ; but he climbed it and did what was needed . He felt that some external force moved him .
Note - V > Page 255 · Location 5597
Scythe
Highlight (blue) - VI > Page 256 · Location 5605
‘ Heavens , what a sight ! ’ said Sergei Ivanovich , glancing round at his brother with displeasure in the first moment . ‘ The door , shut the door ! ’ he cried out . ‘ You must have let in a good dozen . ’ Sergei Ivanovich could not bear flies . He opened the window in his room only at night and kept the doors carefully shut . ‘ By God , not a one . And if I did , I’ll catch it . You wouldn’t believe what a pleasure it was ! How did your day go ? ’
Highlight (blue) - VI > Page 257 · Location 5628
‘ Excellent ! You wouldn’t believe what a good regimen it is against all sorts of foolishness . I want to enrich medical science with a new term : Arbeitskur . ’ s ‘ Well , it seems you’ve no need for that . ’ ‘ No , but for various nervous patients . ’
Highlight (blue) - VI > Page 257 · Location 5631
‘ Yes , it ought to be tried . And I did want to come to the mowing to have a look at you , but the heat was so unbearable that I got no further than the wood . I sat a little , then walked through the wood to the village , met your nurse there and sounded her out about the muzhiks ’ view of you . As I understand , they don’t approve of it . She said : “ It’s not the master’s work . ” Generally it seems to me that in the peasants ’ understanding there is a very firmly defined requirement for certain , as they put it , “ master‘s ” activities . And they don’t allow gentlemen to go outside the limits defined by their understanding . ’
Highlight (blue) - VII > Page 259 · Location 5673
Hard as Stepan Arkadyich tried to be a solicitous father and husband , he never could remember that he had a wife and children . He had a bachelor’s tastes , and they alone guided him .
Highlight (blue) - VII > Page 260 · Location 5685
The day after their arrival there was torrential rain , and during the night there were leaks in the corridor and the children’s room , so that the beds had to be moved to the living room . There was no cook in the household ; of the nine cows , according to the dairymaid , some were with calf , some had dropped their first calf , some were too old , some were hard - uddered ; there was not enough butter and milk even for the children . There were no eggs . No chicken could be found ; they had to roast and boil old , purple , sinewy roosters . No woman could be found to wash the floors - everyone was in the potato fields . To go for a drive was impossible , because one of the horses was restive and pulled at the shaft . There was nowhere to bathe - the entire river bank was trampled by cattle and open to the road ; it was even impossible to go for a walk , because cattle got into the garden through the broken fence , and there was one terrible bull who bellowed and therefore probably would also charge . There were no proper wardrobes . Such as there were would not close , or else opened whenever someone passed by . No pots or crocks ; no tub for laundry , not even an ironing board in the maids ’ quarters .
Note - VII > Page 260 · Location 5693
Country living
Highlight (blue) - VII > Page 260 · Location 5698
But there was in the Oblonsky house , as in all family houses , one inconspicuous but most important and useful person - Matryona Filimonovna . She calmed her mistress , assured her that everything would shape up ( it was her phrase , and it was from her that Matvei had taken it ) , and , without haste or excitement , went into action herself .
Highlight (blue) - VII > Page 260 · Location 5708
They even constructed a bathing house out of straw mats . Lily started bathing , and Darya Alexandrovna’s expectations of a comfortable , if not calm , country life at least came partly true . With six children Darya Alexandrovna could not be calm . One got sick , another might get sick , a third lacked something , a fourth showed signs of bad character , and so on , and so on . Rarely , rarely would there be short periods of calm . But these troubles and anxieties were for Darya Alexandrovna the only possible happiness . Had it not been for them , she would have remained alone with her thoughts of her husband , who did not love her .
Note - VII > Page 260 · Location 5712
Happiness
Highlight (blue) - VII > Page 261 · Location 5715
Often , looking at them , she made every possible effort to convince herself that she was mistaken , that as a mother she was partial to her children ; all the same , she could not but tell herself that she had lovely children , all six of them , each in a different way , but such as rarely happens - and she was happy in them and proud of them .
Highlight (blue) - VIII > Page 262 · Location 5722
On Sunday during St Peter‘s , Darya Alexandrovna went to the liturgy and had all her children take communion . In her intimate , philosophical conversations with her sister , mother and friends , she very often surprised them with her freethinking in regard to religion . She had her own strange religion of metempsychosis , in which she firmly believed , caring little for the dogmas of the Church . But in the family she strictly fulfilled all the requirements of the Church - not only to set an example , but with all her heart - and the fact that the children had not received communion for more than a year8 troubled her greatly . And so , with Matryona Filimonovna’s full approval and sympathy , she decided to do it now , in the summer .
Highlight (blue) - VIII > Page 262 · Location 5736
Darya Alexandrovna had done her hair and dressed with care and excitement . Once she used to dress for herself , to be beautiful and admired ; then , the older she became , the more unpleasant it was for her to dress ; she saw that she had lost her good looks . But now she again dressed with pleasure and excitement . Now she dressed not for herself , not for her own beauty , but so that , being the mother of these lovely things , she would not spoil the general impression . And taking a last look in the mirror , she remained satisfied with herself . She was pretty . Not as pretty as she had once wanted to be at a ball , but pretty enough for the purpose she now had in mind .
Highlight (blue) - VIII > Page 263 · Location 5750
Grisha wept , saying that Nikolenka had also whistled but was not being punished , and that he was weeping not because of the cake - it made no difference to him - but because he had been unfairly dealt with . This was much too sad , and Darya Alexandrovna decided to talk with the governess and get her to forgive him . But , passing through the drawing room , she saw a scene that filled her heart with such joy that tears came to her eyes , and she herself forgave the culprit . The punished boy was sitting at the corner window in the drawing room ; next to him stood Tanya with a plate . Under the pretext of wishing to feed her dolls , she had asked the governess’s permission to take her portion of cake to the nursery and had brought it to her brother instead . Continuing to weep about the unfairness of the punishment he was suffering , he ate the cake she had brought , saying between sobs : ‘ You eat it , too , we’ll eat it together . . . together . ’ Tanya was affected first by pity for Grisha , then by the consciousness of her virtuous deed , and there were tears in her eyes , too ; but she did not refuse and was eating her share .
Note - VIII > Page 263 · Location 5754
Childrenchildren
Highlight (blue) - VIII > Page 263 · Location 5771
Though it was a chore to look after all the children and stop their pranks , though it was hard to remember and not mix up all those stockings , drawers , shoes from different feet , and to untie , unbutton and retie so many tapes and buttons , Darya Alexandrovna , who had always loved bathing herself , and considered it good for the children , enjoyed nothing so much as this bathing with them all . To touch all those plump little legs , pulling stockings on them , to take in her arms and dip those naked little bodies and hear joyful or frightened shrieks ; to see the breathless faces of those splashing little cherubs , with their wide , frightened and merry eyes , was a great pleasure for her .
Highlight (blue) - VIII > Page 264 · Location 5790
Darya Alexandrovna did not want to part from the women , so interesting was it for her to talk with them , so completely identical were their interests . What pleased Darya Alexandrovna most was that she could see clearly that all these women particularly admired how many children she had and how good they were . The women made Darya Alexandrovna laugh and offended the governess , who was the cause of this - for her incomprehensible - laughter . One of the young women was watching the governess , who got dressed last of all , and as she put on her third petticoat , could not help observing : ‘ See , she wraps and wraps and can’t get done wrapping ! ’ - and they all burst into laughter .
Highlight (blue) - IX > Page 265 · Location 5798
Darya Alexandrovna peered ahead and rejoiced , seeing the familiar figure of Levin in a grey hat and grey coat coming to meet them . She was always glad to see him , but she was especially glad now that he would see her in all her glory . No one could understand her grandeur better than Levin .
Highlight (blue) - IX > Page 265 · Location 5817
The children scarcely knew Levin , did not remember when they had last seen him , but did not show that strange feeling of shyness and aversion towards him that children so often feel for shamming adults , for which they are so often painfully punished . Shamming in anything at all can deceive the most intelligent , perceptive person ; but the most limited child will recognize it and feel aversion , no matter how artfully it is concealed .
Note - IX > Page 265 · Location 5820
Children deception
Highlight (blue) - IX > Page 266 · Location 5826
Here , in the country , with the children and Darya Alexandrovna , who was so sympathetic to him , Levin got into that childishly merry state of mind that often came over him , and which Darya Alexandrovna especially loved in him . He ran with the children , taught them gymnastics , made Miss Hull laugh with his bad English , and told Darya Alexandrovna about his occupations in the country .
Highlight (blue) - IX > Page 266 · Location 5835
And Levin , only to divert the conversation , explained to Darya Alexandrovna the theory of dairy farming , the essence of which was that a cow is merely a machine for processing feed into milk , and so on . He was saying that while passionately wishing to hear the details about Kitty and at the same time fearing it . He was afraid that the peace he had attained with such difficulty might be disturbed .
Highlight (blue) - IX > Page 266 · Location 5840
She had now set up her housekeeping so well through Matryona Filimonovna that she did not want to change anything in it ; nor did she trust Levin’s knowledge of agriculture . The argument that a cow is a machine for producing milk was suspect to her . It seemed to her that such arguments could only hinder things . To her it all seemed much simpler : as Matryona Filimonovna explained , they had only to give Spotty and Whiterump more to eat and drink , and keep the cook from taking the kitchen scraps to the washerwoman’s cow .
Highlight (yellow) - X > Page 267 · Location 5856
‘ You know that I proposed and was refused , ’ said Levin , and all the tenderness he had felt for Kitty a moment before was replaced in his soul by a feeling of anger at the insult .
Highlight (yellow) - X > Page 268 · Location 5874
‘ Yes , I understand everything now , ’ Darya Alexandrovna went on . ‘ You can’t understand it . For you men , who are free and can choose , it’s always clear whom you love . But a young girl in a state of expectation , with that feminine , maidenly modesty , a girl who sees you men from afar , who takes everything on trust - a girl may and does sometimes feel that she doesn’t know who she loves or what to say . ’ ‘ Yes , if her heart doesn’t speak . . . ’ ‘ No , her heart speaks , but consider : you men have your eye on a girl , you visit the house , you make friends , you watch , you wait to see if you’re going to find what you love , and then , once you’re convinced of your love , you propose . . . ’ ‘ Well , it’s not quite like that . ’
Highlight (yellow) - X > Page 268 · Location 5885
‘ Ah , pride , pride ! ’ said Darya Alexandrovna , as if despising him for the meanness of this feeling compared with that other feeling which only women know . ‘ At the time you proposed to Kitty , she was precisely in a position where she could not give an answer . She hesitated . Hesitated between you and Vronsky . Him she saw every day , you she had not seen for a long time . Suppose she had been older - for me , for example , there could have been no hesitation in her place . I always found him disgusting , and so he was in the end . ’
Highlight (yellow) - X > Page 269 · Location 5905
Now everything in Darya Alexandrovna’s house and in her children seemed less nice to him than before . ‘ And why does she speak French with the children ? ’ he thought . ‘ How unnatural and false it is ! And the children can feel it . Teaching French and unteaching sincerity , ’ he thought to himself , not knowing that Darya Alexandrovna had already thought it all over twenty times and , to the detriment of sincerity , had found it necessary to teach her children in this way .
Note - X > Page 269 · Location 5909
Sincerity
Highlight (yellow) - X > Page 269 · Location 5912
While Levin was out of the room , an event had occurred which had suddenly destroyed for Darya Alexandrovna all that day’s happiness and pride in her children . Grisha and Tanya had fought over a ball . Darya Alexandrovna , hearing shouts in the nursery , had run there and found a terrible sight . Tanya was holding Grisha by the hair , while he , his face disfigured by anger , was hitting her with his fists wherever he could reach .
Highlight (yellow) - X > Page 269 · Location 5916
was as if darkness came over her life : she understood that her children , of whom she was so proud , were not only most ordinary , but even bad , poorly brought up children , wicked children , with coarse , beastly inclinations .
Highlight (yellow) - X > Page 269 · Location 5918
She could neither speak nor think of anything else and could not help telling Levin of her unhappiness . Levin saw that she was unhappy and tried to comfort her , saying that this did not prove anything bad , that all children fought ; but , as he said it , Levin thought in his heart : ‘ No , I will not be affected and speak French with my children , but my children will not be like that : one need only not harm , not disfigure children , and they will be lovely . Yes , my children will not be like that . ’
Note - X > Page 270 · Location 5921
Children
Highlight (yellow) - XII > Page 273 · Location 5979
Levin was envious of this healthy merriment ; he would have liked to take part in expressing this joy of life . But he could do nothing and had to lie there and look and listen . When the peasants and their song had vanished from his sight and hearing , a heavy feeling of anguish at his loneliness , his bodily idleness , his hostility to this world , came over him .
Highlight (yellow) - XII > Page 273 · Location 5983
It was all drowned in the sea of cheerful common labour . God had given the day , God had given the strength . Both day and strength had been devoted to labour and in that lay the reward . And whom was this labour for ? What would its fruits be ? These considerations were irrelevant and insignificant .
Note - XII > Page 273 · Location 5985
Labor
Highlight (yellow) - XII > Page 273 · Location 5986
Levin had often admired this life , had often experienced a feeling of envy for the people who lived this life , but that day for the first time , especially under the impression of what he had seen in the relations of Ivan Parmenov and his young wife , the thought came clearly to Levin that it was up to him to change that so burdensome , idle , artificial and individual life he lived into this laborious , pure and common , lovely life .
Highlight (yellow) - XII > Page 273 · Location 5994
Only the night sounds of the never silent frogs in the swamp and the horses snorting in the morning mist rising over the meadow could be heard . Coming to his senses , Levin got down off the haystack , looked at the stars and realized that night was over . ‘ Well , what am I to do then ?
Highlight (yellow) - XII > Page 274 · Location 5997
One was to renounce his old life , his useless knowledge , his utterly needless education . This renunciation gave him pleasure and was easy and simple for him . Other thoughts and notions concerned the life he wished to live now . The simplicity , the purity , the legitimacy of this life he felt clearly , and he was convinced that he would find in it that satisfaction , repose and dignity , the absence of which he felt so painfully .
Highlight (yellow) - XII > Page 274 · Location 6004
‘ I’ll clear it up later . One thing is sure , that this night has decided my fate . All my former dreams about family life are nonsense , not the right thing , ’ he said to himself . ‘ All this is much simpler and better . . .
Highlight (yellow) - XII > Page 274 · Location 6005
‘ How beautiful ! ’ he thought , looking at the strange mother - of - pearl shell of white , fleecy clouds that stopped right over his head in the middle of the sky . ‘ How lovely everything is on this lovely night ! And when did that shell have time to form ? A moment ago I looked at the sky , and there was nothing there - only two white strips . Yes , and in that same imperceptible way my views of life have also changed ! ’
Note - XII > Page 274 · Location 6008
Life cloud
Highlight (yellow) - XII > Page 274 · Location 6015
Inside the coach an old lady dozed in the corner and a young girl , apparently just awakened , sat by the window , holding the ribbons of her white bonnet with both hands . Bright and thoughtful , all filled with a graceful and complex inner life to which Levin was a stranger , she looked through him at the glowing sunrise . At the very instant when this vision was about to vanish , the truthful eyes looked at him . She recognized him , and astonished joy lit up her face . He could not have been mistaken . There were no other eyes in the world like those . There was no other being in the world capable of concentrating for him all the light and meaning of life . It was she . It was Kitty . He realized that she was driving to Yergushovo from the railway station . And all that had troubled Levin during that sleepless night , all the decisions he had taken , all of it suddenly vanished .
Highlight (yellow) - XII > Page 275 · Location 6031
‘ No , ’ he said to himself , ‘ however good that life of simplicity and labour may be , I cannot go back to it . I love her . ’
Highlight (yellow) - XIII > Page 276 · Location 6041
Aware of it and aware that an expression of his feelings at that moment would be unsuitable to the situation , he tried to suppress in himself any manifestation of life , and therefore did not move and did not look at her . From this came that strange expression of deadness on his face , which so struck Anna .
Highlight (yellow) - XIII > Page 276 · Location 6045
His wife’s words , confirming his worst doubts , produced a cruel pain in Alexei Alexandrovich’s heart . This pain was further intensified by a strange feeling of physical pity for her , produced in him by her tears . But , left alone in the carriage , Alexei Alexandrovich , to his own surprise and joy , felt complete deliverance both from this pity and from the doubt and suffering of jealousy that had lately tormented him . He felt like a man who has had a long - aching tooth pulled out . After the terrible pain and the sensation of something huge , bigger than his head , being drawn from his jaw , the patient , still not believing his good fortune , suddenly feels that what had poisoned his life and absorbed all his attention for so long exists no more , and that he can again live , think and be interested in something other than his tooth . This was the feeling Alexei Alexandrovich experienced . The pain had been strange and terrible , but now it was gone ; he felt that he could again live and think about something other than his wife .
Highlight (yellow) - XIII > Page 276 · Location 6053
‘ No honour , no heart , no religion - a depraved woman ! I always knew it , and always saw it , though I tried to deceive myself out of pity for her , ’ he said to himself .
Note - XIII > Page 276 · Location 6054
Pity
Highlight (yellow) - XIII > Page 277 · Location 6066
‘ Granted , some unreasonable ridicule falls on these people , but I never saw anything but misfortune in it , and I always sympathized with them , ’ he said to himself , though it was not true ; he had never sympathized with misfortunes of that sort , but had valued himself the higher , the more frequent were the examples of women being unfaithful to their husbands . ‘ It is a misfortune that may befall anybody . And this misfortune has befallen me . The only thing is how best to endure this situation . ’ And he began going through the details of the modes of action chosen by others who had found themselves in the same position .
Highlight (yellow) - XIII > Page 277 · Location 6071
In his youth Karenin’s thoughts had been especially drawn to duelling , precisely because he was physically a timid man and knew it very well .
Highlight (yellow) - XIII > Page 278 · Location 6090
Having considered and rejected a duel , Alexei Alexandrovich turned to divorce - another way out chosen by some of the husbands he remembered .
Highlight (yellow) - XIII > Page 278 · Location 6109
The feeling of jealousy that had tormented him while he did not know , had gone away the moment his tooth was painfully pulled out by his wife’s words . But that feeling had been replaced by another : the wish not only that she not triumph , but that she be paid back for her crime .
Highlight (yellow) - XIII > Page 278 · Location 6111
And again going over the conditions of a duel , a divorce , a separation and again rejecting them , Alexei Alexandrovich became convinced that there was only one solution : to keep her with him , concealing what had happened from society , and taking all possible measures to stop their affair and above all - something he did not admit to himself - to punish her .
Highlight (yellow) - XIII > Page 279 · Location 6122
It gladdened him to think that , even in so important a matter of life as this , no one would be able to say that he had not acted in accordance with the rules of that religion whose banner he had always held high , amidst the general coolness and indifference .
Note - XIII > Page 279 · Location 6123
Religion hypocracy
Highlight (yellow) - XIII > Page 279 · Location 6127
She should be unhappy , but I am not guilty and therefore cannot be unhappy . ’
Highlight (yellow) - XIV > Page 280 · Location 6143
Otherwise you yourself can imagine what awaits you and your son .
Highlight (yellow) - XIV > Page 280 · Location 6147
He read the letter over and remained pleased with it , especially with having remembered to enclose money ; there was not a cruel word , not a reproach , but no lenience either . Above all , there was a golden bridge for return . Having folded the letter , smoothed it with a massive ivory paper - knife , and put money in the envelope , with the pleasure always aroused in him by the handling of his well - arranged writing accessories , he rang .
Highlight (yellow) - XIV > Page 281 · Location 6166
Alexei Alexandrovich’s particularity as a statesman , that characteristic feature proper to him alone ( every rising official has such a feature ) , which , together with his persistent ambition , reserve , honesty and self - assurance , had made his career , consisted in his scorn for paper bureaucracy , in a reducing of correspondence , in taking as direct a relation to living matters as possible , and in economy .
Note - XIV > Page 281 · Location 6169
Irony writing
Highlight (yellow) - XV > Page 283 · Location 6199
Though Anna had stubbornly and bitterly persisted in contradicting Vronsky when he told her that her situation was impossible and tried to persuade her to reveal everything to her husband , in the depths of her soul she considered her situation false , dishonest , and wished with all her soul to change it .
Highlight (yellow) - XV > Page 283 · Location 6207
When she woke up the next morning , the first thing that came to her was the words she had spoken to her husband , and they seemed so terrible to her now that she could not understand how she could have resolved to utter those strange , coarse words , and could not imagine what would come of it .
Highlight (yellow) - XV > Page 284 · Location 6229
She kept repeating : ‘ My God ! My God ! ’ But neither the ‘ my ’ nor the ‘ God ’ had any meaning for her .
Highlight (yellow) - XV > Page 284 · Location 6243
She remembered the partly sincere , though much exaggerated , role of the mother who lives for her son , which she had taken upon herself in recent years , and felt with joy that , in the circumstances she was in , she had her domain , independent of her relations with her husband and Vronsky . That domain was her son .
Highlight (yellow) - XV > Page 285 · Location 6255
The governess , having greeted her , began to tell her at length and with qualifications about Seryozha’s trespass , but Anna was not listening to her ; she was thinking whether she would take her along or not . ‘ No , I won‘t , ’ she decided . ‘ I’ll go alone with my son . ’
Highlight (yellow) - XV > Page 285 · Location 6270
She stopped and looked at the tops of the aspens swaying in the wind , their washed leaves glistening brightly in the cold sun , and she understood that they would not forgive , that everything and everyone would be merciless to her now , like this sky , like this greenery . And again she felt things beginning to go double in her soul . ‘ I mustn’t , I mustn’t think , ’ she said to herself . ‘ I must get ready to go . Where ? When ? Whom shall I take with me ? Yes , to Moscow , on the evening train . Annushka and Seryozha , and only the most necessary things . But first I must write to them both . ’ She quickly went into the house , to her boudoir , sat down at the desk and wrote to her husband :
Highlight (yellow) - XV > Page 286 · Location 6278
Up to that point she wrote quickly and naturally , but the appeal to his magnanimity , which she did not recognize in him , and the necessity of concluding the letter with something touching , stopped her .
Highlight (yellow) - XVI > Page 287 · Location 6295
‘ Very well , ’ she said , and as soon as the man went out , she tore open the letter with trembling fingers . A wad of unfolded bank notes in a sealed wrapper fell out of it . She freed the letter and began reading from the end . ‘ I have made the preparations for the move , I ascribe importance to the fulfilment of my request , ’ she read . She skipped further back , read everything and once again read through the whole letter from the beginning . When she finished , she felt that she was cold and that a terrible disaster , such as she had never expected , had fallen upon her .
Highlight (yellow) - XVI > Page 287 · Location 6300
She had repented in the morning of what she had told her husband and had wished for only one thing , that those words might be as if unspoken . And here was a letter recognizing the words as unspoken and granting her what she had wished . But now this letter was more terrible for her than anything she could have imagined .
Highlight (yellow) - XVI > Page 287 · Location 6302
‘ He’s right ! He’s right ! ’ she said . ‘ Of course , he’s always right , he’s a Christian , he’s magnanimous ! Yes , the mean , vile man ! And I’m the only one who understands or ever will understand it ; and I can’t explain it . They say he’s a religious , moral , honest , intelligent man ; but they don’t see what I’ve seen . They don’t know how he has been stifling my life for eight years , stifling everything that was alive in me , that he never once even thought that I was a living woman who needed love . They don’t know how he insulted me at every step and remained pleased with himself . Didn’t I try as hard as I could to find a justification for my life ? Didn’t I try to love him , and to love my son when it was no longer possible to love my husband ? But the time has come , I’ve realized that I can no longer deceive myself , that I am alive , that I am not to blame if God has made me so that I must love and live . And what now ? If he killed me , if he killed him , I could bear it all , I could forgive it all , but no , he . . .
Note - XVI > Page 287 · Location 6309
Life
Highlight (yellow) - XVI > Page 287 · Location 6312
‘ That’s a threat that he’ll take my son away , and according to their stupid law he can probably do it .
Highlight (yellow) - XVI > Page 288 · Location 6318
And he knows it all , he knows that I cannot repent that I breathe , that I love ; he knows that , except for lies and deceit , there will be nothing in it ; yet he must go on tormenting me . I know him , I know that he swims and delights in lies like a fish in water . But no , I won’t give him that delight , I’ll tear apart this web of lies he wants to wrap around me , come what may . Anything is better than lies and deceit !
Highlight (yellow) - XVI > Page 288 · Location 6322
And she went to the desk in order to write him another letter . But in the depths of her soul she already sensed that she would be unable to tear anything apart , unable to get out of her former situation , however false and dishonest it was .
Highlight (yellow) - XVI > Page 288 · Location 6327
She felt that the position she enjoyed in society , which had seemed so insignificant to her in the morning , was precious to her , and that she would not be able to exchange it for the shameful position of a woman who has abandoned her husband and son and joined her lover ; that , try as she might , she could not be stronger than she was .
Note - XVI > Page 288 · Location 6329
Society
Highlight (yellow) - XVI > Page 288 · Location 6335
‘ What can I write ? ’ she thought . ‘ What can I decide alone ? What do I know ? What do I want ? What do I love ? ’ Again she felt that things had begun to go double in her soul .
Highlight (yellow) - XVII > Page 290 · Location 6345
The company at the croquet party to which Princess Tverskoy had invited Anna was to consist of two ladies with their admirers . These two ladies were the chief representatives of a select new Petersburg circle which , in imitation of an imitation of something , was called Les sept merveilles du monde.u16
Highlight (yellow) - XVII > Page 291 · Location 6372
‘ The more so as I can’t stay with you long , I must go to see old Vrede . I promised her ages ago , ’ said Anna , for whom lying , foreign to her nature , had not only become simple and natural in society , but even gave her pleasure .
Highlight (yellow) - XVII > Page 291 · Location 6385
‘ Ah ! ’ Anna said indifferently , as if it was of little interest to her , and went on with a smile : ‘ How could your company compromise anyone ? ’ This playing with words , this concealment of the secret , held great charm for Anna , as for all women . It was not the need for concealment , not the purpose of the concealment , but the very process of concealment that fascinated her . ‘ I cannot be more Catholic than the pope , ’ she said . ‘ Stremov and Liza Merkalov are the cream of the cream of society . They are also received everywhere , and I , ’ she especially emphasized the I , ‘ have never been strict and intolerant . I simply have no time . ’
Note - XVII > Page 291 · Location 6389
Concealment
Highlight (yellow) - XVII > Page 292 · Location 6417
‘ The husband ? Liza Merkalov’s husband carries rugs around for her and is always ready to be of service . And what else there is in fact , nobody wants to know . You see , in good society one doesn’t speak or even think of certain details of the toilette . It’s the same here . ’
Highlight (yellow) - XVII > Page 292 · Location 6424
And now she knows that this non - understanding becomes her . Now she may purposely not understand , ’ Betsy spoke with a subtle smile , ‘ but all the same it becomes her . You see , one and the same thing can be looked at tragically and be made into a torment , or can be looked at simply and even gaily . Perhaps you’re inclined to look at things too tragically . ’
Highlight (yellow) - XVIII > Page 294 · Location 6436
On her head , hair of a delicately golden colour , her own and other women‘s , was done up into such an edifice of a coiffure that her head equalled in size her shapely , well - rounded and much - exposed bust .
Highlight (yellow) - XVIII > Page 294 · Location 6441
‘ Can you imagine , we nearly ran over two soldiers , ’ she began telling them at once , winking , smiling , and thrusting her train back in place , having first swept it too far to one side . ‘ I was driving with Vaska . . . Ah , yes , you’re not acquainted . ’ And , giving his family name , she introduced the young man and , blushing , laughed loudly at her mistake , that is , at having called him Vaska to a stranger .
Highlight (yellow) - XVIII > Page 295 · Location 6456
She was indeed an ingenuous , spoiled , but sweet and mild woman .
Highlight (yellow) - XVIII > Page 295 · Location 6458
This brilliance shone from her lovely , indeed unfathomable , eyes . The weary and at the same time passionate gaze of those dark - ringed eyes was striking in its perfect sincerity . Looking into those eyes , everyone thought he knew her thoroughly and , knowing , could not but love her . When she saw Anna , her face suddenly lit up with a joyful smile .
Highlight (yellow) - XVIII > Page 295 · Location 6467
‘ But how do you manage not to be bored ? One looks at you and feels gay . You live , but I’m bored . ’ ‘ Bored ? You’re the gayest company in Petersburg , ’ said Anna . ‘ Maybe those who aren’t in our company are more bored ; but for us , for me certainly , it’s not gay , it’s terribly , terribly boring . ’
Note - XVIII > Page 295 · Location 6470
Ennui
Highlight (yellow) - XVIII > Page 295 · Location 6473
‘ Ah , it was excruciating ! ’ said Liza Merkalov . ‘ We all went to my house after the races . And it was all the same people , all the same ! All one and the same thing . We spent the whole evening lolling on the sofa . What’s gay about that ? No , how do you manage not to be bored ? ’ She again turned to Anna . ‘ One looks at you and sees - here is a woman who can be happy or unhappy , but not bored . Tell me , how do you do it ? ’
Note - XVIII > Page 295 · Location 6475
Ennui
Highlight (yellow) - XVIII > Page 295 · Location 6478
Stremov was a man of about fifty , half grey , still fresh , very ugly , but with an expressive and intelligent face .
Highlight (yellow) - XVIII > Page 295 · Location 6481
‘ Don’t do anything , ’ he repeated with a subtle smile , ‘ that’s the best way . I’ve long been telling you , ’ he turned to Liza Merkalov , ‘ that to keep things from being boring , you mustn’t think they’ll be boring . Just as you mustn’t be afraid you won’t fall asleep if you fear insomnia . And Anna Arkadyevna is telling you the same thing . ’ ‘ I’d be very glad if I had said that , because it’s not only intelligent , but also true , ’ Anna said , smiling . ‘ No , tell me , why is it impossible to fall asleep and impossible not to be bored ? ’ ‘ To fall asleep you must work , and to be gay you also must work . ’
Note - XVIII > Page 296 · Location 6486
Work ennui
Highlight (yellow) - XIX > Page 297 · Location 6510
So it seemed to Vronsky . And he thought , not without inner pride and not groundlessly , that anyone else would long ago have become entangled and been forced to act badly if he had found himself in such difficult circumstances . Yet he felt that to avoid getting entangled he had to do the accounts and clear up his situation there and then .
Highlight (yellow) - XIX > Page 297 · Location 6524
The last category of debts - to shops , hotels , the tailor - were of the sort not worth thinking about . Therefore he needed at least six thousand , and had only one thousand eight hundred for current expenses . For a man with an income of a hundred thousand , as everyone evaluated Vronsky’s fortune , such debts , it would seem , could not be burdensome ; but the thing was that he was far from having a hundred thousand .
Highlight (yellow) - XX > Page 299 · Location 6548
Vronsky’s life was especially fortunate in that he had a code of rules which unquestionably defined everything that ought and ought not to be done . The code embraced a very small circle of conditions , but the rules were unquestionable and , never going outside that circle , Vronsky never hesitated a moment in doing what ought be done . These rules determined unquestionably that a card - sharper must be paid but a tailor need not be , that one should not lie to men but may lie to women , that it is wrong to deceive anyone but one may deceive a husband , that it is wrong to pardon insults but one may give insults , and so on . These rules might not all be very reasonable or very nice , but they were unquestionable , and in fulfilling them Vronsky felt at ease and could hold his head high . Only most recently , in regard to his relations with Anna , had he begun to feel that his code of rules did not fully define all circumstances , and to envisage future difficulties and doubts in which he could no longer find a guiding thread .
Note - XX > Page 299 · Location 6555
Ethics
Highlight (yellow) - XX > Page 299 · Location 6557
She was a respectable woman who had given him her love , and he loved her ; therefore she was a woman worthy of equal and even greater respect than a lawful wife . He would have let his hand be cut off sooner than allow himself a word or a hint that might insult her or fail to show her that respect which a woman may simply count on . His relations with society were also clear . Everyone might know or suspect it , but no one should dare to talk . Otherwise he was prepared to silence the talkers and make them respect the non - existent honour of the woman he loved . His relations with the husband were clearest of all . From the moment of Anna’s love for him , he had considered his own right to her unassailable . The husband was merely a superfluous and interfering person . No doubt his position was pathetic , but what could be done ? One thing the husband had the right to do was ask for satisfaction , weapon in hand , and for that Vronsky had been prepared from the first moment .
Highlight (yellow) - XX > Page 300 · Location 6572
And he fell to thinking . The question of resigning or not resigning led him to another secret interest , known only to himself , all but the chief , though hidden , interest of his whole life .
Highlight (yellow) - XX > Page 300 · Location 6580
He sensed that this independent position of a man who could do anything but wanted nothing was beginning to wear thin , that many were beginning to think he could do nothing but be an honest and good fellow .
Highlight (yellow) - XX > Page 300 · Location 6583
His childhood comrade , of the same circle , the same wealth , and a comrade in the corps , Serpukhovskoy , who had graduated in the same year , had been his rival in class , in gymnastics , in pranks , and in ambitious dreams , had come back from Central Asia the other day , 20 having received two promotions there and a decoration rarely given to such young generals .
Highlight (yellow) - XXI > Page 303 · Location 6666
No , what’s needed is a party of independent people like you and me . ’ ‘ But why ? ’ Vronsky named several people in power . ‘ Why aren’t they independent people ? ’ ‘ Only because they don’t have or weren’t born with an independent fortune , didn’t have a name , weren’t born as near to the sun as we were .
Highlight (yellow) - XXI > Page 303 · Location 6676
Vronsky also realized how strong Serpukhovskoy could be in his unquestionable ability to reflect , to comprehend things , in his intelligence and gift for words , which occurred so rarely in the milieu in which he lived . And , much as it shamed him , he was envious .
Highlight (yellow) - XXI > Page 304 · Location 6683
‘ You say maybe not , ’ Serpukhovskoy went on , as if guessing his thoughts , ‘ and I tell you certainly not . And that’s why I wanted to see you . You acted as you had to . I understand that , but you should not persevere . I’m only asking you for carte blanche . I’m not patronizing you . . . Though why shouldn’t I patronize you ? You’ve patronized me so many times ! I hope our friendship stands above that . Yes , ’ he said , smiling at him tenderly , like a woman . ‘ Give me carte blanche , leave the regiment , and I’ll draw you in imperceptibly . ’
Highlight (yellow) - XXI > Page 304 · Location 6689
‘ You say everything should be as it has been . I understand what that means . But listen . We’re the same age . You may have known a greater number of women than I have , ’ Serpukhovskoy’s smile and gestures told Vronsky that he need not be afraid , that he would touch the sore spot gently and carefully . ‘ But I’m married , and believe me , knowing the one wife you love ( as someone wrote ) , you know all women better than if you’d known thousands of them . ’
Highlight (yellow) - XXI > Page 304 · Location 6695
‘ And here is my opinion for you . Women are the main stumbling block in a man’s activity . It’s hard to love a woman and do anything . For this there exists one means of loving conveniently , without hindrance - that is marriage . How can I tell you , how can I tell you what I’m thinking , ’ said Serpukhovskoy , who liked comparisons , ‘ wait , wait ! Yes , it’s as if you’re carrying a fardeauab and doing something with your hands is only possible if the fardeau is tied to your back - and that is marriage .
Highlight (yellow) - XXII > Page 306 · Location 6716
The vague awareness of the clarity his affairs had been brought to , the vague recollection of the friendship and flattery of Serpukhovskoy , who considered him a necessary man , and , above all , the anticipation of the meeting - all united into one general , joyful feeling of life . This feeling was so strong that he smiled involuntarily . He put his feet down , placed one leg across the knee of the other and , taking it in his hand , felt the resilient calf , hurt the day before in his fall , and , leaning back , took several deep breaths .
Highlight (yellow) - XXII > Page 306 · Location 6720
Before , too , he had often experienced the joyful awareness of his body , but never had he so loved himself , his own body , as now . He enjoyed feeling that slight pain in his strong leg , enjoyed feeling the movement of his chest muscles as he breathed .
Highlight (yellow) - XXII > Page 306 · Location 6724
Everything he saw through the coach window , everything in that cold , clean air , in that pale light of sunset , was as fresh , cheerful and strong as himself : the rooftops glistening in the rays of the sinking sun , the sharp outlines of fences and the corners of buildings , the figures of the rare passers - by and the carriages they met , the motionless green of the trees and grass , the fields with regularly incised rows of potatoes , the slanting shadows cast by the houses , trees , and bushes and the rows of potatoes themselves . Everything was as beautiful as a pretty landscape just finished and coated with varnish .
Note - XXII > Page 306 · Location 6728
Mood
Highlight (yellow) - XXII > Page 306 · Location 6735
Her face was covered with a veil , but with joyful eyes he took in the special motion of her gait , peculiar to her alone , the curve of her shoulders , and the poise of her head , and immediately it was as if an electric current ran through his body . He felt his own self with new force , from the resilient movements of his legs to the movements of his lungs as he breathed , and something tickled his lips .
Note - XXII > Page 307 · Location 6738
Body
Highlight (yellow) - XXII > Page 307 · Location 6742
He understood that something had happened , that this meeting would not be joyful . In her presence he had no will of his own : not knowing the reason for her anxiety , he already felt that this same anxiety had involuntarily communicated itself to him .
Highlight (yellow) - XXII > Page 308 · Location 6774
Having read the letter , he raised his eyes to her , and there was no firmness in his look . She understood at once that he had already thought it over to himself . She knew that whatever he might tell her , he would not say everything he thought . And she understood that her last hope had been disappointed . This was not what she had expected .
Highlight (yellow) - XXII > Page 308 · Location 6779
‘ Why not ? ’ Anna asked , holding back her tears , obviously no longer attaching any significance to what he was going to say . She felt that her fate was decided . Vronsky wanted to say that after the duel , in his opinion inevitable , this could not go on , but he said something else . ‘ It cannot go on . I hope you will leave him now . I hope , ’ he became confused and blushed , ‘ that you will allow me to arrange and think over our life . Tomorrow . . . ’ he began .
Highlight (yellow) - XXII > Page 308 · Location 6789
All she had left was his love , and she wanted to love him . ‘ You understand that from the day I loved you everything was changed for me . For me there is one thing only - your love . If it is mine , I feel myself so high , so firm , that nothing can be humiliating for me . I’m proud of my position , because . . . proud of . . . proud . . . ’ She did not finish saying what she was proud of . Tears of shame and despair stifled her voice . She stopped and burst into sobs .
Highlight (yellow) - XXIII > Page 311 · Location 6839
‘ Alexei Alexandrovich , ’ she said , looking up at him and not lowering her eyes under his gaze , directed at her hair , ‘ I am a criminal woman , I am a bad woman , but I am the same as I said I was then , and I’ve come to tell you that I cannot change anything . ’
Highlight (yellow) - XXIII > Page 311 · Location 6843
‘ I now repeat that I am not obliged to know it . I ignore it . Not all wives are so kind as you are , to hasten to tell their husbands such pleasant news . ’
Highlight (yellow) - XXIII > Page 311 · Location 6845
‘ I ignore it as long as it is not known to society , as long as my name is not disgraced . And therefore I only warn you that our relations must be such as they have always been and that only in the case of your compromising yourself would I have to take measures to protect my honour . ’
Highlight (yellow) - XXIII > Page 311 · Location 6848
When she saw again those calm gestures , heard that piercing , childlike and mocking voice , her loathing for him annihilated the earlier pity , and she was merely frightened , but wished at all costs to understand her situation .
Highlight (yellow) - XXIV > Page 313 · Location 6863
The night Levin spent on the haystack was not wasted on him : the farming he had been engaged in he now came to loathe , and it lost all interest for him . Despite excellent crops , there had never been , or at least it seemed to him that there had never been , so many failures and so much animosity between him and the muzhiks as that year , and the cause of the failures and the animosity was now clear to him . The delight he had experienced in the work itself , the closeness with the muzhiks that had come from it , the envy of them and of their life that he had experienced , the wish to go over to that life , which that night had no longer been a dream for him but an intention , the fulfilment of which he had been thinking over in detail - all this had so changed his view of farming that he could no longer find any of his former interest in it and could not help seeing his own unpleasant attitude towards his workers , which was at the bottom of the whole thing .
Highlight (yellow) - XXIV > Page 313 · Location 6871
But he now saw clearly ( his work on the book about agriculture , in which the fundamental element had to be the worker , had helped him greatly in this ) - he saw clearly now that the farming he was engaged in was merely a cruel and persistent struggle between him and his workers , in which on the one side , his own , there was a constant , intense striving to remake everything after the best - considered fashion , and on the other there was the natural order of things .
Highlight (yellow) - XXIV > Page 313 · Location 6878
He stood for every penny he had ( and could not do otherwise , because as soon as he slackened his energy , he would not have enough money to pay the workers ) , and they stood only for working quietly and pleasantly , that is , as they were accustomed to do .
Highlight (yellow) - XXIV > Page 313 · Location 6880
It was in his interest that each worker should do as much as possible , that he should keep his wits about him at the same time , that he should try not to break the winnowing machine , the horse - rake , the thresher , that he should try to think about whatever he was doing . The worker , however , wanted to work as pleasantly as possible , with rests , and above all - carelessly , obliviously , thoughtlessly . That summer Levin saw it at every step . He sent people to mow clover for hay , choosing the worst acres , overgrown with grass and wormwood , unfit for seed - they went and mowed down his best seeding acres , justifying themselves by shifting it on to the steward and comforting him with the excellence of the hay ; but he knew the reason was that those acres were easier to mow .
Highlight (yellow) - XXIV > Page 314 · Location 6891
All this was done not because anyone wished evil to Levin or his farming ; on the contrary , he knew he was loved and considered a simple master ( which was the highest praise ) ; it was done only because of the wish to work merrily and carelessly , and his interests were not only foreign and incomprehensible to them , but fatally opposed to their own most just interests .
Highlight (yellow) - XXV > Page 316 · Location 6952
He had ploughed for the potatoes with an iron plough , which he called a ‘ plougher ’ , borrowed from the landowner . He sowed wheat . A small detail especially struck Levin , that as he thinned his rye he gave the thinned stalks to the horses . So many times , seeing this excellent feed go to waste , Levin had wanted to gather it ; but it had always proved impossible . Yet with the muzhik it got done , and he could not praise this feed enough .
Highlight (yellow) - XXVI > Page 318 · Location 6971
Sviyazhsky was the marshal of nobility in his district . He was five years older than Levin and long married . His young sister - in - law , a girl Levin found very sympathetic , lived in his house .
Highlight (yellow) - XXVI > Page 318 · Location 6972
And Levin knew that Sviyazhsky and his wife wished very much to marry this girl to him . He knew it indubitably , as these things are always known to young men , so - called suitors , though he would never have dared say it to anyone , and he also knew that even though he wanted to get married , even though by all tokens this quite attractive girl would make a wonderful wife , he was as little capable of marrying her , even if he had not been in love with Kitty Shcherbatsky , as of flying into the sky . And this knowledge poisoned for him the pleasure he hoped to have in visiting Sviyazhsky .
Highlight (yellow) - XXVI > Page 318 · Location 6980
Sviyazhsky was one of those people , always astonishing to Levin , whose reasoning , very consistent though never independent , goes by itself , and whose life , extremely well defined and firm in its orientation , goes by itself , quite independent of and almost always contrary to their reasoning . Sviyazhsky was an extremely liberal man .
Highlight (yellow) - XXVI > Page 318 · Location 6987
He considered the Russian muzhik as occupying a transitional step of development between ape and man , and yet at zemstvo elections he was most willing to shake hands with muzhiks and listen to their opinions . He believed in neither God nor devil , but was very concerned about questions of improving the life of the clergy and the shrinking number of parishes , taking particular trouble over keeping up the church in his village .
Highlight (yellow) - XXVI > Page 318 · Location 6991
In the woman question he was on the side of the extreme advocates of complete freedom for women , and especially of their right to work , but he lived with his wife in such a way that everyone admired the harmony of their childless family life ; and he arranged his wife’s existence so that she did not and could not do anything but concern herself , together with her husband , with how better and more gaily to pass the time .
Highlight (yellow) - XXVI > Page 319 · Location 6998
Still less could Levin say that he was trash , because Sviyazhsky was unquestionably an honest , kind , intelligent man , who cheerfully , energetically , ceaselessly did things highly appreciated by all around him and most certainly never consciously did or could do anything bad .
Highlight (yellow) - XXVI > Page 319 · Location 7010
‘ This may not have been important under serfdom , or may not be important in England . In both cases the conditions themselves are defined ; but with us now , when all this has been overturned and is just beginning to settle , the question of how these conditions ought to be settled is the only important question in Russia , ’ thought Levin .
Highlight (yellow) - XXVI > Page 320 · Location 7032
‘ Do you teach in it yourself ? ’ asked Levin , trying to look past the neckline , but feeling that wherever he looked in that direction , he would see nothing else . ‘ Yes , I have taught and still do , but we have a wonderful young woman for a teacher . And we’ve introduced gymnastics . ’
Highlight (yellow) - XXVII > Page 322 · Location 7074
And much of what the landowner went on to say , proving why Russia had been ruined by the emancipation , seemed to him very true , new and irrefutable . The landowner was obviously voicing his own thought , which happens rarely , and this thought had not been arrived at by a desire to somehow occupy an idle mind , but had grown out of the conditions of his own life , had been hatched out in his country solitude and considered on all sides .
Highlight (yellow) - XXVII > Page 322 · Location 7077
‘ The point , kindly note , is that all progress is achieved by authority alone , ’ he said , apparently wishing to show that he was no stranger to education . ‘ Take the reforms of Peter , Catherine , Alexander . 25 Take European history . The more so with progress in agricultural methods .
Note - XXVII > Page 322 · Location 7079
Progress authority reactionary
Highlight (yellow) - XXVII > Page 322 · Location 7082
Now , sirs , with the abolition of serfdom , our authority has been taken away , and our farming , where it was brought to a high level , is bound to sink to the most savage , primitive condition . That’s how I understand
Highlight (yellow) - XXVII > Page 322 · Location 7086
‘ There it is - the work force , the chief element in farming , ’ thought Levin . ‘ With paid workers . ’ ‘ Workers don’t want to do good work or to do good work with tools . Our worker knows one thing only - how to get drunk as a pig , and while drunk to break everything you give him . He’ll overwater the horses , snap good harness , dismount a wheel with a tyre and sell it for drink , put a pintle into the thresher so as to break it . He loathes the sight of things that aren’t to his liking . That causes the whole level of the farming to sink . Plots are abandoned , overgrown with wormwood or given up to muzhiks , and where millions of bushels used to be produced , now it’s a few hundred thousand - the common wealth is diminished . If the same thing was done , only with calculation
Highlight (yellow) - XXVII > Page 322 · Location 7097
‘ I don’t find it so , ’ Sviyazhsky retorted , seriously now . ‘ I only see that we don’t know how to go about farming and that , on the contrary , the level of farming we carried on under serfdom was in fact not too high but too low . We have neither machines , nor good working stock , nor real management , nor do we know how to count . Ask any farm owner - he won’t know what’s profitable for him and what isn’t . ’
Highlight (yellow) - XXVII > Page 323 · Location 7121
‘ Ah , the true rent ! ’ Levin exclaimed with horror . ‘ Maybe true rent exists in Europe , where the land has been improved by the labour put into it ; but with us the land all becomes worse from the labour put into it - that is , from being ploughed - and so there’s no true rent . ’
Note - XXVII > Page 323 · Location 7123
Economics
Highlight (yellow) - XXVII > Page 323 · Location 7129
Deprived of his interlocutor , Levin went on talking with the landowner , trying to prove to him that all the difficulty came from our not knowing the properties and habits of our worker ; but the landowner , like all people who think originally and solitarily , was slow to understand another man’s thought and especially partial to his own . He insisted that the Russian muzhik was a swine and liked swinishness , and that to move him out of swinishness , authority was needed , and there was none , a stick was needed , and we suddenly became so liberal that we replaced the thousand - year - old stick with some sort of lawyers and lock - ups , in which worthless , stinking muzhiks are fed good soup and allotted so many cubic feet of air .
Highlight (yellow) - XXVII > Page 324 · Location 7136
‘ That will never be done with the Russian peasantry without a stick ! There’s no authority , ’ the landowner replied .
Highlight (yellow) - XXVII > Page 324 · Location 7137
‘ How can new forms be found ? ’ said Sviyazhsky , who , having eaten his curds and lit a cigarette , again came over to the arguers . ‘ All possible relations to the workforce have been defined and studied , ’ he said . ‘ That leftover of barbarism - the primitive community with its mutual guarantees - is falling apart of itself , serfdom is abolished , there remains only free labour , and its forms are defined and ready , and we must accept them . The hired worker , the day - labourer , the farmhand - you won’t get away from that . ’
Note - XXVII > Page 324 · Location 7141
Economics
Highlight (yellow) - XXVII > Page 324 · Location 7149
‘ This question now occupies the best minds in Europe . The Schulze - Delitsch tendency . . . Also all the vast literature on the workers question , on the most liberal Lassalle tendency . . . The Mulhouse system is already a fact , you surely know that . ’ 27 ‘ I have an idea , but a very vague one . ’ ‘ No , you only say so ; you surely know it all as well as I do . Of course , I’m no social professor , but it once interested me , and if it interests you , you really should look into it . ’
Note - XXVII > Page 324 · Location 7154
Socialism
Highlight (yellow) - XXVII > Page 324 · Location 7155
The landowners got up , and Sviyazhsky , again stopping Levin in his unpleasant habit of prying beyond the reception rooms of his mind , went to see his guests off .
Highlight (yellow) - XXVIII > Page 325 · Location 7163
Sviyazhsky’s study was a huge room lined with bookcases and had two tables in it - one a massive desk that stood in the middle of the room , and the other a round one on which the latest issues of newspapers and magazines in different languages were laid out in a star - like pattern around a lamp . By the desk was a stand with boxes of all sorts of files marked with gilt labels .
Highlight (yellow) - XXVIII > Page 325 · Location 7175
‘ Yes , but I was very interested in the angry landowner , ’ Levin said with a sigh . ‘ He’s intelligent and said many right things . ’ ‘ Ah , go on ! An inveterate secret serf - owner , as they all are ! ’ said Sviyazhsky .
Highlight (yellow) - XXVIII > Page 325 · Location 7179
‘ What interests me so much is this , ’ said Levin . ‘ He’s right that our cause , that is , rational farming , doesn’t work , that only usurious farming works , as with that silent one , or else the simplest kind . Who is to blame for that ? ’
Highlight (yellow) - XXVIII > Page 326 · Location 7183
‘ But all the same I don’t know what you’re surprised at . The peasantry stand at such a low level of both material and moral development that they apparently must oppose everything foreign to them . In Europe rational farming works because the peasantry are educated ; which means that with us the peasantry have to be educated - that’s all . ’
Note - XXVIII > Page 326 · Location 7185
Peasantry education
Highlight (yellow) - XXVIII > Page 326 · Location 7193
‘ That’s something I’ve never understood , ’ Levin objected hotly . ‘ How will schools help the peasantry to improve their material well - being ? You say that schools , education , will give them new needs . So much the worse , because they won’t be able to satisfy them . And how the knowledge of addition , subtraction and the catechism will help them to improve their material condition , I never could understand . The evening before last I met a woman with an infant at her breast and asked her where she had been . She said : “ To the wise woman , because a shriek - hag has got into the child , so I took him to be treated . ” I asked how the wise woman treats the shriek - hag . “ She puts the baby on a roost with the chickens and mumbles something . ”
Note - XXVIII > Page 326 · Location 7196
Peasants edducation
Highlight (yellow) - XXVIII > Page 326 · Location 7206
Schools won’t help , what will help is an economic system in which the peasantry will be wealthier , there will be more leisure - and then there will also be schools . ’
Highlight (yellow) - XXVIII > Page 327 · Location 7211
Levin saw that he was not going to find a connection between this man’s life and his thoughts . Evidently it made absolutely no difference to him where his reasoning led him ; he needed only the process of reasoning itself . And it was unpleasant for him when the process of reasoning led him to a dead end . That alone he disliked and avoided , turning the conversation to something pleasantly cheerful .
Highlight (yellow) - XXVIII > Page 327 · Location 7220
Left alone in the room given him , lying on a spring mattress that unexpectedly tossed his arms and legs up with every movement , Levin did not fall asleep for a long time . Not one conversation with Sviyazhsky , though he had said many intelligent things , had interested Levin ; but the landowner’s arguments called for discussion . Levin involuntarily recalled all his words and in his imagination corrected his own replies .
Highlight (yellow) - XXVIII > Page 327 · Location 7228
Let’s try to look at the work force not as an ideal work force but as the Russian muzhik with his instincts , and organize our farming accordingly . Picture to yourself , ” I should have said to him , “ that you do your farming like that old man , that you’ve found a way of getting the workers interested in the success of the work and found some midpoint in the improvements that they can recognize - and , without exhausting the soil , you’ll bring in two or three times more than before . Divide it in two , give half to the workers ; the difference you come out with will be greater and the workers will also come out with more . But to do that you have to lower the level of the farming and interest the workers in its success . How to do that is a matter of details , but there’s no doubt that it’s possible . ” ’
Note - XXVIII > Page 327 · Location 7233
Agriculture
Highlight (yellow) - XXIX > Page 328 · Location 7244
As far as Levin’s proposal was concerned - that he participate as a shareholder , along with the workers , in the whole farming enterprise - to this the steward responded only with great dejection and no definite opinion , and immediately began talking about the necessity of transporting the remaining sheaves of rye the next day and seeing to the cross - ploughing , so that Levin felt that now was not the time for it .
Highlight (yellow) - XXIX > Page 328 · Location 7256
Besides that ( Levin felt that the bilious landowner was right ) , the peasants put down as the first and immutable condition of any agreement whatsoever that they not be forced to employ new methods of farming or to make use of new tools . They agreed that the iron plough worked better , that the scarifier produced good results , but they found a thousand reasons why it was impossible for them to use either , and though he was convinced that he had to lower the level of farming , he was sorry to renounce improvements whose advantages were so obvious to him . But , despite all these difficulties , he had his way and by autumn things got going , or at least it seemed so to him .
Highlight (yellow) - XXIX > Page 329 · Location 7274
Besides that , these muzhiks , under various pretexts , kept postponing the building of a cattle - yard and threshing barn on this land , as had been agreed , and dragged it on till winter .
Highlight (yellow) - XXIX > Page 329 · Location 7283
These matters , along with the rest of the farming , which had been left in his hands , along with the study - work on his book , so occupied Levin’s summer that he hardly ever went hunting . He learned at the end of August , from the man who brought back the side - saddle , that the Oblonskys had returned to Moscow . He felt that by not answering Darya Alexandrovna’s letter , by his impoliteness , which he could not recall without a flush of shame , he had burned his boats and could never visit them again . He had done the same with the Sviyazhskys by leaving without saying goodbye . But he would never visit them again either . It made no difference to him now .
Highlight (yellow) - XXIX > Page 330 · Location 7293
He saw the same in the socialist books : these were either beautiful but inapplicable fantasies , such as he had been enthusiastic about while still a student , or corrections , mendings of the state of affairs in which Europe stood and with which Russian agriculture had nothing in common . Political economy said that the laws according to which European wealth had developed and was developing were universal and unquestionable . Socialist teaching said that development according to these laws led to ruin . And neither the one nor the other gave , not only an answer , but even the slightest hint of what he , Levin , and all Russian peasants and landowners were to do with their millions of hands and acres so that they would be most productive for the common good . Once he got down to this matter , he conscientiously read through everything related to his subject and planned to go abroad in the autumn to study the matter on site , so that the same thing would not happen to him with this question as had happened so often with various other questions .
Note - XXIX > Page 330 · Location 7298
Socialism
Highlight (yellow) - XXIX > Page 330 · Location 7303
He now saw clearly that Kauffmann and Miccelli had nothing to tell him . He knew what he wanted . He saw that Russia had excellent land , excellent workers , and that in some cases , as with the muzhik half - way there , workers and land produced much , but in the majority of cases , when capital was employed European - style , they produced little , and that this came only from the fact that the workers wanted to work and to work well in the one way natural to them , and that their resistance was not accidental but constant and rooted in the spirit of the peasantry . He thought that the Russian peasantry , called upon to inhabit and cultivate vast unoccupied spaces , consciously kept to the methods necessary for it until all the lands were occupied , and that these methods were not at all as bad as was usually thought . And he wanted to prove it theoretically in his book and in practice on his estate .
Note - XXIX > Page 330 · Location 7306
Peasant
Highlight (yellow) - XXX > Page 331 · Location 7312
Now , to explain the whole thing theoretically and to finish his book , which , according to Levin’s dreams , was not only to bring about a revolution in political economy but was to abolish that science altogether and initiate a new science - of the relation of the peasantry to the land - the only thing necessary was to go abroad and study on site everything that had been done there in that direction and to find convincing proofs that everything done there was not what was needed .
Note - XXX > Page 331 · Location 7315
Political economy economics
Highlight (yellow) - XXX > Page 331 · Location 7327
‘ I need only persist in going towards my goal and I’ll achieve what I want , ’ thought Levin , ‘ and so work and effort have their wherefore . This is not my personal affair , it is a question here of the common good . Agriculture as a whole , above all the position of the entire peasantry , must change completely . Instead of poverty - universal wealth , prosperity ; instead of hostility - concord and the joining of interests . In short , a revolution , a bloodless but great revolution , first in the small circle of our own region , then the province , Russia , the whole world . Because a correct thought cannot fail to bear fruit . Yes , that is a goal worth working for .
Note - XXX > Page 331 · Location 7332
Agriculture economics
Highlight (yellow) - XXX > Page 332 · Location 7336
The steward , who had gone to the merchant , came and brought part of the money for the wheat . The arrangement with the innkeeper was made , and the steward had found out on the way that wheat had been left standing in the fields everywhere , so that his own hundred and sixty stacks were nothing in comparison with what others had lost .
Highlight (yellow) - XXX > Page 332 · Location 7356
‘ It’s a known fact , a man had best think of his own soul , ’ she said with a sigh . ‘ There’s Parfen Denisych , illiterate as they come , but God grant everybody such a death , ’ she said of a recently deceased house servant . ‘ Took communion , got anointed . ’ 33
Highlight (yellow) - XXXI > Page 335 · Location 7410
He wanted to weep over his beloved dying brother , and he had to listen and keep up a conversation about how he was going to live .
Note - XXXI > Page 335 · Location 7411
Death
Highlight (yellow) - XXXI > Page 335 · Location 7416
Death , the inevitable end of everything , presented itself to him for the first time with irresistible force . And this death , which here , in his beloved brother , moaning in his sleep and calling by habit , without distinction , now on God , now on the devil , was not at all as far off as it had seemed to him before . It was in him , too - he felt it . If not now , then tomorrow , if not tomorrow , then in thirty years - did it make any difference ? And what this inevitable death was , he not only did not know , he not only had never thought of it , but he could not and dared not think of it . ‘ I work , I want to do something , and I’ve forgotten that everything will end , that there is - death . ’ He was sitting on his bed in the dark , crouching , hugging his knees and thinking , holding his breath from the strain of it . But the more he strained to think , the clearer it became to him that it was undoubtedly so , that he had actually forgotten , overlooked in his life one small circumstance - that death would come and everything would end , that it was not worth starting anything and that nothing could possibly be done about it . Yes , it was terrible , but it was so .
Note - XXXI > Page 335 · Location 7420
Death
Highlight (yellow) - XXXI > Page 336 · Location 7428
And he suddenly remembered how as children they had gone to bed at the same time and had only waited for Fyodor Bogdanych to leave before they started throwing pillows at each other and laughing , laughing irrepressibly , so that even the fear of Fyodor Bogdanych could not stop this overflowing and effervescent consciousness of life’s happiness . ‘ And now this crooked and empty chest . . . and I , not knowing what will become of me or why . . . ’
Highlight (yellow) - XXXI > Page 336 · Location 7434
Levin felt it , went behind the partition , put out the candle , but did not sleep for a long time . He had just partly clarified the question of how to live , when he was presented with a new , insoluble problem - death .
Note - XXXI > Page 336 · Location 7436
Death life
Note - XXXII > Page 337 · Location 7448
Falseness
Highlight (yellow) - XXXII > Page 337 · Location 7448
On the third day , Nikolai provoked his brother to tell him his plans again and began not only to condemn them , but deliberately to confuse them with communism .
Note - XXXII > Page 337 · Location 7449
Communism
Highlight (yellow) - XXXII > Page 337 · Location 7460
‘ But I have been , and I find that it’s premature but reasonable , and that it has a future , like Christianity in the first centuries . ’ ‘ I only suppose that the work force must be considered from the point of view of natural science - that is , study it , recognize its properties , and . . . ’
Highlight (yellow) - XXXII > Page 338 · Location 7466
true that he wanted to balance between communism and the established forms and that this was hardly possible .
Highlight (yellow) - XXXII > Page 338 · Location 7469
‘ You don’t want to set up anything , you simply want to be original , as you have all your life , to show that you don’t simply exploit the muzhiks but do it with an idea . ’

"""
if __name__ == '__main__':
    notes = GetNotes(sample_text)
    notes.set_for_kindle()
    note_iterator = notes.return_iterator()
    x = note_iterator()

    while True:
        print (next(x))
        input()
    


