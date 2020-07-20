import pyglet
from pyglet.window import key
from pyglet.gl import glEnable,glBlendFunc,GL_BLEND,GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
window = pyglet.window.Window(caption='shooting' ,width=600,height=600)
window.set_location(window.screen.width//2-window.width//2, window.screen.height//2-window.height//2)
window.set_icon(pyglet.image.load('textures/icon.ico'))

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

KeyHandler = key.KeyStateHandler()
window.push_handlers(KeyHandler)

ObjectBatch = pyglet.graphics.Batch()


Player = pyglet.sprite.Sprite(pyglet.image.load('textures/player/Player_direction0.png') ,x=300,y=300 ,batch=ObjectBatch)
PlayerDirection = 'up'
Bullet = pyglet.sprite.Sprite(pyglet.image.load('textures/bullet/bullet1.png') ,x=300,y=300 ,batch=ObjectBatch)
BulletDirection = 'up'
Bullet.visible = False
SpacePressed = False
shoot = False
def update(dt):
    global SpacePressed, PlayerDirection, BulletDirection, shoot
    if KeyHandler[key.W]:
        PlayerDirection = 'up'
        Player.y += 1
    if KeyHandler[key.S]:
        PlayerDirection = 'down'
        Player.y -= 1
    if KeyHandler[key.A]:
        PlayerDirection = 'left'
        Player.x -= 1
    if KeyHandler[key.D]:
        PlayerDirection = 'right'
        Player.x += 1
    if SpacePressed == False and KeyHandler[key.SPACE] and Bullet.visible == False and shoot == True:
        SpacePressed = True
        BulletDirection = PlayerDirection
        Bullet.visible = True
        shoot = False
    if SpacePressed == True and not KeyHandler[key.SPACE]: SpacePressed = False

    # Player flip
    if PlayerDirection == 'up': Player.image = pyglet.image.load('textures/player/Player_direction0.png')
    if PlayerDirection == 'down': Player.image = pyglet.image.load('textures/player/Player_direction2.png')
    if PlayerDirection == 'left': Player.image = pyglet.image.load('textures/player/Player_direction1.png')
    if PlayerDirection == 'right': Player.image = pyglet.image.load('textures/player/Player_direction3.png')

    # Pos of bullet
    if not Bullet.visible and PlayerDirection == 'up':
        Bullet.y = Player.y + 32
        Bullet.x = Player.x + 16
        shoot = True
    if not Bullet.visible and PlayerDirection == 'down':
        Bullet.y = Player.y
        Bullet.x = Player.x + 16
        shoot = True
    if not Bullet.visible and PlayerDirection == 'left':
        Bullet.x = Player.x - 5
        Bullet.y = Player.y + 16
        shoot = True
    if not Bullet.visible and PlayerDirection == 'right':
        Bullet.x = Player.x + 32
        Bullet.y = Player.y + 16
        shoot = True

    # Bullet direction
    if BulletDirection == 'up' or BulletDirection == 'down':
        Bullet.image = pyglet.image.load('textures/bullet/bullet1.png')
    if BulletDirection == 'left' or BulletDirection == 'right':
        Bullet.image = pyglet.image.load('textures/bullet/bullet0.png')

    # Bullet movment
    if BulletDirection == 'up' and Bullet.visible == True: Bullet.y +=4
    if BulletDirection == 'down' and Bullet.visible == True: Bullet.y -= 4
    if BulletDirection == 'left' and Bullet.visible == True: Bullet.x -= 4
    if BulletDirection == 'right' and Bullet.visible == True: Bullet.x += 4

    # Bullet reset
    if Bullet.x >= 590 and BulletDirection == 'right':Bullet.visible = False
    if Bullet.x <= 5 and BulletDirection == 'left': Bullet.visible = False
    if Bullet.y >= 590 and BulletDirection == 'up': Bullet.visible = False
    if Bullet.y <= 5 and BulletDirection == 'down': Bullet.visible = False
@window.event()
def on_draw():
    window.clear()
    ObjectBatch.draw()

pyglet.clock.schedule_interval(update, 1/120)
pyglet.app.run()