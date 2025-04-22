import os
import random
import sys
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def load_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """移動方向ごとのこうかとん画像を辞書で返す"""
    original_img = pg.image.load("fig/3.png")
"""
    kk_imgs = {
        (0, 0): pg.transform.rotozoom(original_img, 0, 0.9),
        (+5, 0): pg.transform.rotozoom(original_img, -90, 0.9),
        (+5, -5): pg.transform.rotozoom(original_img, -45, 0.9),
        (0, -5): pg.transform.rotozoom(original_img, 270, 0.9),
        (-5, -5): pg.transform.rotozoom(original_img, 45, 0.9),
        (-5, 0): pg.transform.rotozoom(original_img, 0, 0.9),
        (-5, +5): pg.transform.rotozoom(original_img, 45, 0.9),
        (0, +5): pg.transform.rotozoom(original_img, -270, 0.9),
        (+5, +5): pg.transform.rotozoom(original_img, -135, 0.9),
    }
    
    return kk_imgs
"""
def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """移動量の合計値タプルに対応する向きの画像Surfaceを返す"""
    return kk_imgs.get(sum_mv, kk_imgs[(0, 0)])

def main():
    global kk_imgs
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    # こうかとん画像辞書の読み込み
    kk_imgs = load_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    last_mv = (0, 0)  # 最後の移動方向

    # 爆弾画像と加速度のリスト作成
    bb_accs = [a for a in range(1, 11)]
    bb_imgs = []
    for r in range(1, 11):
        img = pg.Surface((20*r, 20*r))
        pg.draw.circle(img, (255, 0, 0), (10*r, 10*r), 10*r)
        img.set_colorkey((0, 0, 0))
        bb_imgs.append(img)

    # 爆弾初期化
    bb_rct = bb_imgs[0].get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return

        # キー入力処理
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        # こうかとん移動
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        # 向き更新
        mv = tuple(sum_mv)
        if mv != (0, 0):
            last_mv = mv
        kk_img = get_kk_img(last_mv)
        screen.blit(kk_img, kk_rct)

        # 爆弾更新（加速＆拡大）
        index = min(tmr // 500, 9)
        bb_img = bb_imgs[index]
        avx = vx * bb_accs[index]
        avy = vy * bb_accs[index]
        old_center = bb_rct.center
        bb_rct = bb_img.get_rect(center=old_center)

        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def game_over(screen: pg.Surface) -> None:
    blackout = pg.Surface((WIDTH, HEIGHT))
    blackout.set_alpha(150)
    blackout.fill((0, 0, 0))
    screen.blit(blackout, (0, 0))
    sad_img = pg.image.load("fig/8.png")
    sad_img = pg.transform.rotozoom(sad_img, 0, 0.9)
    sad_rct1 = sad_img.get_rect(center=(WIDTH//2 + 180, HEIGHT//2))
    sad_rct2 = sad_img.get_rect(center=(WIDTH//2 - 180, HEIGHT//2))
    screen.blit(sad_img, sad_rct1)
    screen.blit(sad_img, sad_rct2)
    font = pg.font.SysFont(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)
    pg.display.update()
    time.sleep(5)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
