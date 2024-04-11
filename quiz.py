import pygame
import pygame.gfxdraw
import time
import random

from label import *


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1500, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Quizjáték")




buttons = pygame.sprite.Group()
class Button(pygame.sprite.Sprite):
    usedA = []
    usedB = []

    def __init__(self, position, text, size,
        colors="white on blue",
        hover_colors="red on green",
        style="button1",
        borderc=(255,255,255),
        command=lambda: print("No command activated for this button")):


        super().__init__()
        global num

        self.text = text
        self.command = command

        self.colors = colors
        self.original_colors = colors
        self.fg, self.bg = self.colors.split(" on ")

        if hover_colors == "red on green":
            self.hover_colors = f"{self.bg} on {self.fg}"
        else:
            self.hover_colors = hover_colors

        self.style = style
        self.borderc = borderc

        self.font = pygame.font.SysFont("Arial", size)
        self.render(self.text)
        self.x, self.y, self.w , self.h = self.text_render.get_rect()
        self.x, self.y = position
        self.rect = pygame.Rect(self.x, self.y, 500, self.h)
        self.position = position
        self.pressed = 1

        buttons.add(self)

    def render(self, text):

        self.text_render = self.font.render(text, 1, self.fg)

        self.image = self.text_render

    def update(self):
        self.fg, self.bg = self.colors.split(" on ")
        if self.style == "button1":
            self.draw_button1()
        elif self.style == "button2":
            self.draw_button2()
        if self.command != None:
            self.hover()
            self.click()

    def draw_button1(self):


        lcolor = (150, 150, 150)
        lcolor2 = (50, 50, 50)
        pygame.draw.line(screen, lcolor, self.position,
            (self.x + self.w , self.y), 5)
        pygame.draw.line(screen, lcolor, (self.x, self.y - 2),
            (self.x, self.y + self.h), 5)

        pygame.draw.line(screen, lcolor2, (self.x, self.y + self.h),
            (self.x + self.w , self.y + self.h), 5)
        pygame.draw.line(screen, lcolor2, (self.x + self.w , self.y + self.h),
            [self.x + self.w , self.y], 5)

        pygame.draw.rect(screen, self.bg, self.rect)  

    def draw_button2(self):


        pygame.draw.rect(screen, self.bg, (self.x - 50, self.y, 500 , self.h))
        pygame.gfxdraw.rectangle(screen, (self.x - 50, self.y, 500 , self.h), self.borderc)

    def check_collision(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):

            self.colors = self.hover_colors

        else:
            self.colors = self.original_colors



    def hover(self):


        self.check_collision()

    def click(self):

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                print("The answer is:'" + self.text + "'")
                self.command()
                self.pressed = 0

            if pygame.mouse.get_pressed() == (0,0,0):
                self.pressed = 1





def on_click():
    print("Click on one answer")

def on_right():
    check_score("right")

def on_false():

    check_score()

def check_score(answered="wrong"):

    global qnum, points, onepoints, twopoints

    if qnum < 10:
        print(qnum, len(questions))
        if answered == "right":
            time.sleep(.1)
            onepoints += 1
            points += 1

        qnum += 1
        score.change_text("1. játékos pontjai: " + str(onepoints))

        
        question = random.randint(0, len(questions))
        while question in Button.usedA:
            question = random.randint(0, len(questions))
        Button.usedA.append(question)
        print(Button.usedA)
       
        title.change_text(questions[question-1][0], color="cyan")

        num_question.change_text(str(qnum) + ". kérdés")
        show_question(question)
        


    elif qnum == 10:
        print(qnum, len(questions))
        if answered == "right":
            time.sleep(.1)
            onepoints +=1
            twopoints -= 1
        qnum += 1
        points = 0
    time.sleep(.5)

    if qnum > 10 and qnum < 21:
        print(qnum, len(questions))
        if answered == "right":
            time.sleep(.1)
            points += 1
            twopoints += 1

        qnum += 1
        score.change_text("2. játékos pontjai: " + str(twopoints))

        question = random.randint(0, len(questions))
        while question in Button.usedB:
            question = random.randint(0, len(questions))
        Button.usedB.append(question)
        print(Button.usedB)

        title.change_text(questions[question-1][0], color="cyan")

        num_question.change_text(str(qnum-1) + ". kérdés")
        show_question(question)

    elif qnum == 21:
        print(qnum, len(questions))
        if answered == "right":
            kill()
            time.sleep(.1)
            points +=1
            twopoints += 1
        twopoints = points
        score.change_text("Az első játékos " + str(onepoints) + " pontot ért el, a második játékos " + str(twopoints) + " pontot ért el.")
        if onepoints > twopoints:
            title.change_text("Az első játékos nyert", color="cyan")
        elif onepoints < twopoints:
            title.change_text("A második játékos nyert", color="cyan")
        else:
            title.change_text("Döntetlen", color="cyan")
        kill()
    time.sleep(.5)




questions = [
    ["Mi Magyarország fővárosa?", ["Budapest", "Róma", "Tokió", "Madrid"]],
  ["Melyik évben kezdődött az első világháború?", ["1914", "1905", "1923", "1939"]],
  ["Ki festette a Mona Lisát?", ["Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso", "Claude Monet"]],
  ["Melyik bolygó a Naprendszerünk legnagyobb bolygója?", ["Jupiter", "Mars", "Merkúr", "Szaturnusz"]],
  ["Ki írta a „Rómeó és Júlia” című drámát?", ["William Shakespeare", "Charles Dickens", "Jane Austen", "Fyodor Dostoyevsky"]],
  ["Melyik város az Egyesült Királyság fővárosa?", ["London", "Párizs", "Berlin", "Madrid"]],
  ["Melyik állat a legnagyobb a Földön?", ["Kék bálna", "Elefánt", "Tigris", "Zsiráf"]],
  ["Melyik évben köszöntötték be az első ember a Holdon?", ["1969", "1959", "1979", "1989"]],
  ["Melyik a világ legnagyobb óceánja?", ["Csendes-óceán", "Atlanti-óceán", "Indiai-óceán", "Északi-sarki-óceán"]],
  ["Melyik városban található a Louvre múzeum?", ["Párizs", "London", "Róma", "Madrid"]],
  ["Ki volt az Egyesült Államok első elnöke?", ["George Washington", "Thomas Jefferson", "Abraham Lincoln", "John Adams"]],
  ["Melyik szín keverése adja a lila színt?", ["Kék és piros", "Kék és zöld", "Sárga és piros", "Zöld és sárga"]],
  ["Melyik évben kezdődött az első olimpiai játékok a modern korban?", ["1896", "1886", "1906", "1916"]],
  ["Ki volt az első ember, aki megmászta a Mount Everestet?", ["Sir Edmund Hillary", "Reinhold Messner", "Tenzing Norgay", "Junko Tabei"]],
  ["Melyik az egyik hét csoda közül?", ["Kolosszeum", "Louvre", "Eiffel-torony", "Westminster apátság"]],
  ["Melyik ország a legnagyobb felszínű Afrikában?", ["Algéria", "Egyiptom", "Dél-Afrika", "Nigéria"]],
  ["Ki volt a „Harry Potter” könyvek szerzője?", ["J.K. Rowling", "J.R.R. Tolkien", "Roald Dahl", "C.S. Lewis"]],
  ["Melyik a világ legmagasabb hegycsúcsa?", ["Mount Everest", "Mount Kilimanjaro", "Aconcagua", "K2"]],
  ["Melyik évben volt az amerikai polgárháború?", ["1861", "1776", "1812", "1914"]],
  ["Melyik a legnagyobb sziget a világon?", ["Grönland", "Ausztrália", "Madagaszkár", "Új-Zéland"]],
  ["Melyik évben alakult az ENSZ (Egyesült Nemzetek Szervezete)?", ["1945", "1919", "1939", "1955"]],
  ["Ki írta a „Háború és béke” című regényt?", ["Leo Tolstoy", "Fyodor Dostoyevsky", "Victor Hugo", "Ernest Hemingway"]],
  ["Melyik a legnagyobb szárazföldi ragadozó?", ["Elefánt", "Tigris", "Grizzly medve", "Jegesmedve"]],
  ["Melyik város az Egyesült Államok fővárosa?", ["Washington, D.C.", "New York", "Los Angeles", "Chicago"]],
  ["Ki festette a „Csillagos éjszakát” című festményt?", ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet"]],
  ["Melyik az egyik legnagyobb kutyafajta?", ["Német juhász", "Beagle", "Mopsz", "Dán dog"]],
  ["Melyik évben kezdődött az első világháború?", ["1914", "1905", "1923", "1939"]],
  ["Melyik a legnagyobb kontinens?", ["Ázsia", "Afrika", "Ausztrália", "Észak-Amerika"]],
  ["Ki írta a „Macskák” című musicalt?", ["Andrew Lloyd Webber", "Stephen Sondheim", "Richard Rodgers", "Leonard Bernstein"]],
  ["Melyik a legnagyobb édesvízi tó a Földön?", ["Kaszpi-tenger", "Huron-tó", "Michigan-tó", "Titicaca-tó"]],
  ["Ki volt az első nő, aki megkapta a Nobel-békedíjat?", ["Jane Addams", "Marie Curie", "Mother Teresa", "Malala Yousafzai"]],
  ["Melyik a legnagyobb repülőterek közül?", ["Heathrow Airport, London", "Hartsfield-Jackson Airport, Atlanta", "Beijing Capital Airport, Peking", "Dubai International Airport"]],
  ["Ki volt Amerika függetlenségi nyilatkozatának fő szerzője?", ["Thomas Jefferson", "George Washington", "Benjamin Franklin", "John Adams"]],
  ["Melyik állat a legnagyobb szárazföldi emlős?", ["Elefánt", "Tigris", "Zsiráf", "Orrszarvú"]],
]




def show_question(qnum):



    kill()

    

    pos = [100, 150, 200, 250]

    random.shuffle(pos)

    Button((10, 100), "1. ", 36, "aqua on blue",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=None)
    Button((10, 150), "2. ", 36, "aqua on blue",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=None)
    Button((10, 200), "3. ", 36, "aqua on blue",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=None)
    Button((10, 250), "4. ", 36, "aqua on blue",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=None)



    Button((50, pos[0]), questions[qnum-1][1][0], 36, "aqua on blue",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=on_right)
    Button((50, pos[1]), questions[qnum-1][1][1], 36, "aqua on blue",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=on_false)
    Button((50, pos[2]), questions[qnum-1][1][2], 36, "aqua on blue",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=on_false)
    Button((50, pos[3]), questions[qnum-1][1][3], 36, "aqua on blue",
        hover_colors="blue on orange", style="button2", borderc=(255,255,0),
        command=on_false)


def kill():
    for _ in buttons:
        _.kill()

qnum = 1
points = 0
onepoints = 0
twopoints = 0

num_question = Label(screen, str(qnum), 0, 0)
score = Label(screen, "1. játékos pontjai: ", 50, 300)
title = Label(screen, questions[qnum-1][0], 10, 10, 55, color="cyan")

def start_again():
    pass

def loop():
    global game_on

    show_question(qnum)

    while True:
        screen.fill(0)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        buttons.update() 
        buttons.draw(screen)
        show_labels()
        clock.tick(60)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    pygame.init()
    game_on = 1
    loop()