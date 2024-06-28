import pygame, random, time, sys

telaX = 720
telaY = 480
preto = pygame.Color(0, 0, 0)
branco = pygame.Color(255, 255, 255)
vermelho = pygame.Color(255, 0, 0)
verde = pygame.Color(0, 255, 0)
azul = pygame.Color(0, 0, 255)

check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


telaJogo = pygame.display.set_mode((telaX, telaY))

fps = pygame.time.Clock()

posicaoCobra = [100, 50]
corpoCobra = [[100, 50], [100-10, 50], [100-(2*10), 50]]

posicaoFood = [random.randrange(1, (telaX//10)) * 10, random.randrange(1, (telaY//10)) * 10]
spawnFood = True

direction = 'RIGHT'
mudar = direction

placar = 0

def fimJogo():
    fonte = pygame.font.SysFont('times new roman', 90)
    fimJogoSurface =  fonte.render('VOCÊ MORREU', True, vermelho)
    fimJogoRect = fimJogoSurface.get_rect()
    telaJogo.fill(preto)
    telaJogo.blit(fimJogoSurface, fimJogoRect)
    mostrarPlacar(0, vermelho, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit

def mostrarPlacar(escolha, cor, fonte, tamanho):
    placarFonte = pygame.font.SysFont(fonte, tamanho)
    placarSurface = placarFonte.render('Placar : ' + str(placar), True, cor)
    placarRect = placarSurface.get_rect()
    if escolha == 1:
        placarRect.midtop = (telaX/10, 15)
    else:
        placarRect.midtop = (telaX/2, telaY/1.25)
    telaJogo.blit(placarSurface, placarRect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                mudar = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                mudar = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                mudar = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                mudar = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    if mudar == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if mudar == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if mudar == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if mudar == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        posicaoCobra[1] -= 10
    if direction == 'DOWN':
        posicaoCobra[1] += 10
    if direction == 'LEFT':
        posicaoCobra[0] -= 10
    if direction == 'RIGHT':
        posicaoCobra[0] += 10

    corpoCobra.insert(0, list(posicaoCobra))
    if posicaoCobra[0] == posicaoFood[0] and posicaoCobra[1] == posicaoFood[1]:
        placar += 1
        spawnFood = False
    else:
        corpoCobra.pop()

    if not spawnFood:
        posicaoFood = [random.randrange(1, (telaX//10)) * 10, random.randrange(1, (telaY//10)) * 10]
    spawnFood = True

    telaJogo.fill(preto)
    for pos in corpoCobra:
        pygame.draw.rect(telaJogo, verde, pygame.Rect(pos[0], pos[1], 10, 10))
        
    pygame.draw.rect(telaJogo, branco, pygame.Rect(posicaoFood[0], posicaoFood[1], 10, 10))

    if posicaoCobra[0] < 0 or posicaoCobra[0] > telaX-10:
        fimJogo()
    if posicaoCobra[1] < 0 or posicaoCobra[1] > telaY-10:
        fimJogo()

    for block in corpoCobra[1:]:
        if posicaoCobra[0] == block[0] and posicaoCobra[1] == block[1]:
            fimJogo()

    mostrarPlacar(1, branco, 'consolas', 20)
    pygame.display.update()
    fps.tick(25)