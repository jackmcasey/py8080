import pygame

import cpu


class Emulator:
    """
    Contains 8080 CPU and uses Pygame to display the VRAM

    Controls:
      1. Press 'c' key to insert coin
      2. Press '1' key to choose player 1
      3. Press arrow keys to move
      4. Press 'Space' to shoot

    """

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, path, width=256, height=224):
        self._cpu = cpu.CPU(path)
        self._cpu.init_instruction_table()
        self._path = path
        self._width = width
        self._height = height
        self._display_size = height, width
        self._px_array = None
        self._fps = 60

    def refresh(self):
        """
        Update the pixel array

        :return:
        """
        for i in range(self._height):
            index = 0x2400 + (i << 5)

            for j in range(32):
                vram = self._cpu._memory[index]
                index += 1

                for k in range(8):
                    if (vram & 0x01) == 1:
                        self._px_array[i][255-j*8-k] = self.WHITE
                    else:
                        self._px_array[i][255-j*8-k] = self.BLACK

                    vram >>= 1

    def run(self):
        self._cpu.reset()

        pygame.init()
        surface = pygame.display.set_mode(self._display_size)
        pygame.display.set_caption(self._path)

        black = 0, 0, 0
        surface.fill(black)
        self._px_array = pygame.PixelArray(surface)

        pygame.display.update()
        fps_clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self._cpu.io.in_port1 |= 0x01
                    if event.key == pygame.K_1:
                        self._cpu.io.in_port1 |= 0x04
                    if event.key == pygame.K_SPACE:
                        self._cpu.io.in_port1 |= 0x10
                    if event.key == pygame.K_LEFT:
                        self._cpu.io.in_port1 |= 0x20
                    if event.key == pygame.K_RIGHT:
                        self._cpu.io.in_port1 |= 0x40

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_c:
                        self._cpu.io.in_port1 &= 255 - 0x01
                    if event.key == pygame.K_1:
                        self._cpu.io.in_port1 &= 255 - 0x04
                    if event.key == pygame.K_SPACE:
                        self._cpu.io.in_port1 &= 255 - 0x10
                    if event.key == pygame.K_LEFT:
                        self._cpu.io.in_port1 &= 255 - 0x20
                    if event.key == pygame.K_RIGHT:
                        self._cpu.io.in_port1 &= 255 - 0x40

            self._cpu.run()
            self.refresh()
            fps_clock.tick(self._fps)
            pygame.display.update()