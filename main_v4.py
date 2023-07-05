import sys


import pygame

import gameV2
import make_positions_list
from name_coord_list import NameList


def run_game():

    pygame.init()
    screen = pygame.display.set_mode((1200, 900))
    pygame.display.set_caption("Pedamma - version 0.5")

    rows = 10
    cols = 10
    square_size = 70
    color = (0,139,139)

    #naam lijst\
    name_list = NameList()
    name_list = name_list.get_list()
    #print(name_list)

    # Maak de beginpositie van het bord
    start_pos = gameV2.Game()
    start_list = start_pos.position_list
    #print(start_list)
        
    # list from white's perspective
    start_coord = make_positions_list.PosList(10, 10, 0, 0, 70).make_list()
    print(start_coord)

    draw_squares_white = []
    draw_coordinates_white = []

    draw_squares_black = []
    draw_coordinates_black = []

    # Woordenboek waarin alle speelvelden komen, een woordenboek waarin alle witte schijven komen 
    # en tot slot een woordenboek waarin alle zwarte schijven komen
    rects_dict = {}
    white_dict = {}
    black_dict = {}


    # Nu maken we woordenboeken die bijhoudt hoeveel keer er door de gebruiker op een steen geklikt is:
    # eentje die het voor de witte stukken bijhoudt en eentje die het voor de zwarte stenen bijhoudt.
    white_count = {}
    black_count = {}

    # We maken twee variabelen aan die bijhouden hoeveel oneven getallen er in white_count respectievelijk black_count staan
    # Deze waarden moeten uiteraard aan het begin van het spel gelijk zijn aan 0.
    odd_white = 0
    odd_black = 0

    # We maken een lijst waarin de zet van de witspeler respectievelijk zwartspeler wordt opgeslagen:
    #       - wanneer de gebruiker op een schijf klikt, dan krijgt deze een rode rand. Tegelijk wordt het coordinaat van deze cirkel opgeslagen.
    #       - wanneer de gebruiker nu op een leeg vakje klikt, dan wordt het coordinaat van dit lege vakje opgeslagen (in white_move[0]).
    #       - we kunnen vervolgens deze informatie gebruiken om de cirkel op de oude plek te verwijderen (incl. de rode rand) en de cirkel op de nieuwe plek te tekenen (in white_move[1]). 
    white_move = [0,0]
    black_move = [0,0]

    # We gaan de zet, zoals in de lijsten white_move resp. black_move, transformeren naar de string 'v1 - v2'. 
    # Waarbij v1, v2 de nummers van de vakjes zijn waarvandaan de schijf komt en waar deze naartoe gaat.
    # Hiervoor maken we eerst twee nieuwe lijsten aan, waarbij de coordinaten van de middelpunten van de schijf en het lege vak worden vervangen met de nummers van de vakjes. 

    number_white_move = [0, 0]
    coord_white_move = [0, 0]
    string_white_move = ''
    number_black_move = [0, 0]
    coord_black_move = [0, 0]

    # Variabele voor de beurt
    # Als wit aan zet is, heeft turn de waarde 0. Aangezien wit als eerste aan de beurt is, krijgt turn als startwaarde '0' mee 
    # Aangezien wit als eerste aan zet is, maken we direct een lijst met reglementaire zetten
    turn = 0
    # start_pos.legal_moves_list("white")
    print(start_pos.legal_moves_white)

    # We willen nu de schijven tekenen. Ter voorbereiding hierop doen we het volgende:
    # - uit start_list, maken we een lijst met coordinaten (rijnummer, kolomnummer) van de vakjes waarin de schijven moeten worden getekend
    #       (hierbij maken we een lijst voor de witte schijven (draw_squares_white) en een aparte lijst voor de zwarte schijven (draw_squares_black))
    # - uit start_coord halen we bij de coordinaten (rijnummer, kolomnummer), de x,y-coordinaten van het middelpunt van deze vakjes 
    #       (hierbij ook een aparte lijst voor de witte schijven (draw_coordinates_white) en een aparte lijst voor de zwarte schijven (draw_coordinates_black()))  
    # - de schijven worden getekend in regels 120 tot en met 130
    for vakje, schijf in start_list.items():
            if schijf == ['white', 'stone']:
                draw_squares_white.append(vakje)
            if schijf == ['black', 'stone']:
                draw_squares_black.append(vakje)
        
    for i in range(len(draw_squares_white)):
        for vakje, coord in start_coord.items():
            if draw_squares_white[i] == vakje:
                draw_coordinates_white.append(coord)

    for i in range(len(draw_squares_black)):
        for vakje, coord in start_coord.items():
            if draw_squares_black[i] == vakje:
                draw_coordinates_black.append(coord)

    for i in range(len(draw_squares_white)):
        draw_coordinates_white[i] = tuple(draw_coordinates_white[i])
        
    
    for i in range(len(draw_squares_black)):
        draw_coordinates_black[i] = tuple(draw_coordinates_black[i])
        
    # print(draw_coordinates_white)
    # print(draw_coordinates_black)

    # Tekenen van het ruitjespatroon van het dambord
    # De vakjes waarover de schijven bewegen, worden opgeslagen in het woordenboek rects_dict met als key (rijnummer, kolomnummer) en als value het vakje.
    for row in range(rows):
        for col in range(row%2, rows, 2):
            pygame.draw.rect(screen, (205, 197, 191), (row*square_size, col*square_size, square_size, square_size))
            pygame.draw.rect(screen, (0,0,0), (row*square_size, col*square_size, square_size, square_size),1)
        for col in range((row+1)%2, rows, 2):
            rects_dict[(row, col)]= pygame.draw.rect(screen, color, (row*square_size, col*square_size, square_size, square_size))
            pygame.draw.rect(screen, (0,0,0), (row*square_size, col*square_size, square_size, square_size),1)

    # print(rects_dict)

    # Tekenen van de schijven voor beide spelers:
    piece_color_white = (255, 255, 255) 
    piece_color_black = (0,0,0)     
        
    for i in range(len(draw_coordinates_white)):
        white_dict[draw_coordinates_white[i]] = pygame.draw.circle(screen, piece_color_white, draw_coordinates_white[i], 33) 
        white_count[draw_coordinates_white[i]] = 0       
        

    for i in range(len(draw_coordinates_black)):
        black_dict[draw_coordinates_black[i]] = pygame.draw.circle(screen, piece_color_black, draw_coordinates_black[i], 33)
        black_count[draw_coordinates_black[i]] = 0       
        
    # print(white_dict.keys())
    # print(white_count.keys())
    # print(black_dict.keys())
    # print('Lijst voor wit: ' + str(white_count))
    # print('Lijst voor zwart: ' + str(black_count))

    while True:
               
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()              

                # Geval 1:
                # Wit is aan zet en er is op een witte schijf geklikt.
                if turn == 0:                                       
                 
                    for coord, schijf_wit in white_dict.items():
                        # Als er voor het eerst op een witte schijf wordt geklikt (en er is bij de vorige muisklik niet op een zwarte schijf geklikt), 
                        # dan komt er een rode rand omheen. Het middelpunt van de schijf waarop werd geklikt, wordt toegevoegd aan de lijst white_move
                        if schijf_wit.collidepoint(mouse_pos) and white_count[coord] % 2 == 0 and odd_white == 0 and odd_black == 0 :

                            white_move[0] = coord 
                            # print(white_move)
                                                                                               
                            white_count[coord] += 1                                                                                                                                      
                            middelpunt = schijf_wit.center
                            straal = 0.5*schijf_wit.height                                              

                            pygame.draw.circle(screen, (255,0,0), middelpunt, straal,3)
                                               
                            # Er is nu een schijf met een rode rand, dus in white_count staat nu 1 oneven getal
                            odd_white = 1
                        # Als er voor de tweede keer achter elkaar op een witte schijf wordt geklikt (en er is bij de laatste muisklik niet op een zwarte schijf geklikt), 
                        # dan is het de bedoeling dat de rode rand om de witte schijf weggaat. De coordinaten van deze schijf worden verwijderd uit de lijst white_move.                                                       

                        elif schijf_wit.collidepoint(mouse_pos) and white_count[coord] % 2 == 1 and odd_white == 1 and odd_black == 0:                                                            
                            
                            #  
                            # print(white_move)
                        
                            middelpunt = schijf_wit.center
                            straal = 0.5*schijf_wit.height                                          

                            pygame.draw.circle(screen, (255,255,255), middelpunt, straal, 3) 
                           
                            white_count[coord] += 1

                            odd_white = 0  

                    # Als er een schijf is met een rode rand en de gebruiker klikt op een leeg vakje, dan wordt de schijf verplaatst naar dit lege vakje.
                    # Hiervoor zijn er twee condities nodig:
                    #   1. odd_white = 1 (geeft aan dat er een witte schijf is met een rode rand eromheen)
                    #   2. white_move[0] bestaat, d.w.z er is een schijf aangeklikt die verplaatst moet worden 
                    # Vervolgens wordt er op een ander vakje geklikt: we checken eerst dat de schjif niet wordt verplaatst naar het vakje waar deze stond

                    if odd_white == 1 and white_move[0]:
                        #print(white_move)
                        for vakje in rects_dict.values():
                            if vakje.collidepoint(mouse_pos):
                                 centrum_nieuw = vakje.center
                        if centrum_nieuw == white_move[0]:
                            pass
                        else: 
                            print(white_move)
                            white_move[1] = centrum_nieuw
                            # print(white_move)

                            # We zetten nu de ingevoerde zet om in string waarin de zet zo genoteerd wordt zoals dit op een notatieformulier gebeurt.
                            for mid_punt in name_list:
                                for i in range(len(white_move)):
                                    if mid_punt == white_move[i]:
                                        number_white_move[i] = name_list[mid_punt]                           

                            # print(number_white_move)
                            string_white_move = str(number_white_move[0]) + "-" + str(number_white_move[1])
                            print('White move: ' + string_white_move)

                            

                            # Controle of de zet die door de gebruiker is ingevoerd een reglementaire zet is.
                            if string_white_move in start_pos.legal_moves_white:
                                print("True")

                                # print(white_move)
                                
                                # We zetten de ingevoerde zet nu om waarbij zowel het oorspronkelijke veld als het doelveld de vorm (rijnr, kolomnr) hebben
                                for vakje, coord in start_coord.items():
                                    if white_move[0] == tuple(coord):
                                        coord_white_move[0] = vakje
                                    if white_move[1] == tuple(coord):
                                        coord_white_move[1] = vakje
                                # print(coord_white_move)

                                # We wijzigen de start_list: bij het oorspronkelijke veld wordt de value 'white', 'stone' aangepast naar [] en bij het doelveld staat
                                # nu 'white', 'stone' ipv []   
                                for coord in start_list.keys():
                                    if coord == coord_white_move[0]:
                                        start_list[coord] = []
                                    if coord == coord_white_move[1]:
                                        start_list[coord] = ["white", "stone"]
                                # print(start_list)

                                # Nu positie opnieuw tekenen op basis van de aangepaste start_list 
                                # Eerst maken we lijsten en woordenboeken leeg zodat de nieuwe positie erin kan zonder dat de oude positie onthouden en getekend wordt
                                draw_squares_white = []
                                draw_coordinates_white = []
                                white_dict = {}
                                white_count = {}
                                
                                for vakje, schijf in start_list.items():
                                    if schijf == ['white', 'stone']:
                                        draw_squares_white.append(vakje)
                                    if schijf == ['black', 'stone']:
                                        draw_squares_black.append(vakje)
        
                                for i in range(len(draw_squares_white)):
                                    for vakje, coord in start_coord.items():
                                        if draw_squares_white[i] == vakje:
                                            draw_coordinates_white.append(coord)

                                for i in range(len(draw_squares_white)):
                                    draw_coordinates_white[i] = tuple(draw_coordinates_white[i])

                                # Zorgt ervoor dat de oude schijf niet meer wordt getekend
                                pygame.draw.circle(screen, color, white_move[0], 33)	

                                # De schijven worden opnieuw getekend
                                for i in range(len(draw_coordinates_white)):
                                    white_dict[draw_coordinates_white[i]] = pygame.draw.circle(screen, piece_color_white, draw_coordinates_white[i], 33) 
                                    white_count[draw_coordinates_white[i]] = 0   

                                # De witte zet is nu getekend en uitgevoerd. De beurt gaat naar zwart  
                                odd_white = 0
                                white_move = [0,0]
                                number_white_move = [0, 0]
                                string_white_move = ''      
                                start_pos.legal_moves_black = []
                                start_pos.legal_moves_list("black")
                                print(start_pos.legal_moves_black)
                                turn = 1
                                print(start_list)
                            else: 
                                print("Dit is een onreglementaire zet. Selecteer a.u.b. een ander veld")                            
                                                               
                # Geval 2: zwart is aan zet:   
                # # Er is op een zwarte schijf geklikt
                if turn == 1:                              
                    for coord, schijf_zwart in black_dict.items():
                        if schijf_zwart.collidepoint(mouse_pos) and black_count[coord] % 2 == 0 and odd_white == 0 and odd_black == 0:
                            black_move[0] = coord 
                            # print(black_move)                           

                                             
                            black_count[coord] += 1                                        
                                                                       
                            middelpunt = schijf_zwart.center
                            straal = 0.5*schijf_zwart.height                                             

                            pygame.draw.circle(screen, (255,0,0), middelpunt, straal,3)     

                            odd_black = 1

                        elif schijf_zwart.collidepoint(mouse_pos) and black_count[coord] % 2 == 1 and odd_white == 0 and odd_black == 1:                         
                            black_count[coord] += 1    

                            middelpunt = schijf_zwart.center
                            straal = 0.5*schijf_zwart.height                  

                            pygame.draw.circle(screen, (0,0,0), middelpunt, straal, 3)   

                            odd_black = 0 

                    if odd_black == 1 and black_move[0]:
                        # print('odd_black == 1 and black_move[0]')
                        for vakje in rects_dict.values():
                            if vakje.collidepoint(mouse_pos):
                                centrum_nieuw = vakje.center
                        if centrum_nieuw == black_move[0]:
                            pass
                        else:   
                            black_move[1] = centrum_nieuw
                            # print(black_move)

                            # We zetten nu de ingevoerde zet om in string waarin de zet zo genoteerd wordt zoals dit op een notatieformulier gebeurt.
                            for mid_punt in name_list:
                                for i in range(len(black_move)):
                                    if mid_punt == black_move[i]:
                                        number_black_move[i] = name_list[mid_punt]                           

                            # print(number_white_move)
                            string_black_move = str(number_black_move[0]) + "-" + str(number_black_move[1])
                            print('Black move: ' + string_black_move)

                            # Controle of de zet die door de gebruiker is ingevoerd een reglementaire zet is. 
                            # Als deze controle positief is, dan wordt de zet doorgevoerd in de position_list
                            if string_black_move in start_pos.legal_moves_black:
                                print("True")
                                for vakje, coord in start_coord.items():
                                    if black_move[0] == tuple(coord):
                                        coord_black_move[0] = vakje
                                    if black_move[1] == tuple(coord):
                                        coord_black_move[1] = vakje
                                print(coord_black_move)
                            
                            # We wijzigen de start_list: bij het oorspronkelijke veld wordt de value 'black', 'stone' aangepast naar [] en bij het doelveld staat
                            # nu 'black', 'stone' ipv []   
                                for coord in start_list.keys():
                                    if coord == coord_black_move[0]:
                                        start_list[coord] = []
                                    if coord == coord_black_move[1]:
                                        start_list[coord] = ["black", "stone"]
                                #print(start_list)

                            # Nu positie opnieuw tekenen op basis van de aangepaste start_list 
                            # Eerst maken we lijsten en woordenboeken leeg zodat de nieuwe positie erin kan zonder dat de oude positie onthouden en getekend wordt
                                draw_squares_black = []
                                draw_coordinates_black = []
                                black_dict = {}
                                black_count = {}

                                for vakje, schijf in start_list.items():
                                    if schijf == ['black', 'stone']:
                                        draw_squares_black.append(vakje)
                                    if schijf == ['black', 'stone']:
                                        draw_squares_black.append(vakje)
        
                                for i in range(len(draw_squares_black)):
                                    for vakje, coord in start_coord.items():
                                        if draw_squares_black[i] == vakje:
                                            draw_coordinates_black.append(coord)

                                for i in range(len(draw_squares_black)):
                                    draw_coordinates_black[i] = tuple(draw_coordinates_black[i])

                                # Zorgt ervoor dat de oude schijf niet meer zichtbaar is
                                pygame.draw.circle(screen, color, black_move[0], 33)	

                                # De zwarte schijven worden opnieuw getekend
                                for i in range(len(draw_coordinates_black)):
                                    black_dict[draw_coordinates_black[i]] = pygame.draw.circle(screen, piece_color_black, draw_coordinates_black[i], 33) 
                                    black_count[draw_coordinates_black[i]] = 0

                                # Wit is nu aan zet
                                odd_black = 0
                                black_move = [0, 0]
                                number_black_move = [0, 0]
                                string_black_move = ''
                                
                                start_pos.legal_moves_white = []
                                start_pos.legal_moves_list("white")
                                print(start_pos.legal_moves_white) 
                                turn = 0
                                print(start_list)
                           
                            else: 
                                print("Dit is een onreglementaire zet. Selecteer a.u.b. een ander veld")
                                string_black_move = ''
                                

                                                                                                                                                                                                               
                                                                 
                        #screen.fill(color)
                        #           
            pygame.display.flip()
          
run_game()

        





