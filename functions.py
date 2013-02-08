#    Functions


def get_playlist():
    file_name = "/home/parent/test/piclist.txt"
    return (file_name)


def read_config():
    return True


def get_picture(file):
    pic_file = file.readline()
    pic_file = pic_file.strip()
    if pic_file == '':
        return False
    else:
        image = pygame.Surface((window.get_rect().width,\
         window.get_rect().height))
        image = pygame.image.load(pic_file)
        image = image.convert()
        return image


def crossfade(image1, image2):
    # fade out image1 and fade in image2
    for alpha in [0, 255]:
        image1.set_alpha(255 - alpha)
        image2.set_alpha(alpha)
        window.blit(image1, (0, 0))
        window.blit(image2, (0, 0))
        pygame.display.flip()


def title_loop():
    # title screen main loop
    image = pygame.image.load("/home/parent/Pictures/test")
    image = image.convert()
    done = False
    alpha = 250
    alpha_vel = 1

    # fade alpha in-out while waiting
    while not done:
        # get key input
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True

        # draw
        if alpha >= 255 or alpha <= 0:
            alpha_vel *= -1
        alpha += alpha_vel
        image.set_alpha(alpha)

        window.blit(background, (0, 0))
        window.blit(image, (0, 0))
        pygame.display.flip()

        # pygame.time.delay(20)
