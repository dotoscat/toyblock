Full example
============

For the sake of simplicity, this example is not runnable. It just demostrates
how to use toyblock.

.. code-block:: python
    
    from time import time
    import toyblock

    #Our components for an entity 'bullet'
    class Body:
        def __init__(self):
            self.x = 0.0
            self.y = 0.0
            self.vel_x = 0.0
            self.vel_y = 0.0

        def update(dt):
            # update

    class Collision:
        def __init__(self, radius):
            self.x = 0.0
            self.y = 0.0
            self.radius = radius
        def collides_with(another):
            # return true or false
        def update(x, y):
            # update

    class Graphic:
        def __init__(self, sprite, animation):
            self.sprite = sprite
            self.animation = animation

        def update_position(x, y):
            self.sprite.set_position(x, y)

    @toyblock.system
    def physics(system, entity, dt):
        body = entity[Body]
        body.update(dt)

    @toyblock.system
    def collision(system, entity, hero):
        body = entity[Body]
        collision = entity[Collision]
        hero_collision = hero[Collision]
        if collision.collides_with(hero_collision):
            entity.free()

    @toyblock.system
    def draw(system, entity, canvas):
        body = entity[Body]
        graphic = entity[Graphic]
        graphic.update_position(body.x, body.y)
        canvas.draw(graphic)

    bullet_args = (None, (8, ), (bullet_sprite, bullet_animation))

    bullets = Pool(100, (Body, Collision, Graphic), args=bullet_args, systems=(physics, collision, draw))
    @bullet.init
    def bullet_init(entity):
        entity[Graphic].animation.step = 0

    # .... More setup

    while playing:
        # Spawn bullets and move hero
        physics(time())
        collision(hero)
        draw(canvas)
