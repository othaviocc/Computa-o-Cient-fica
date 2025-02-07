from dataclasses import dataclass as component
import pyxel as px
import esper
import math

# ------------------------ COMPONENTS -----------------------

@component
class Circle:
    x: float
    y: float
    r: int = 10
    m: float = 1.0

@component
class Velocity:
    vx: float = 0.0
    vy: float = 0.0

@component
class Color:
    c: int = 6

@component
class Gravity:
    g: float = 9.8

@component
class Wind:
    wx: float = 0.0

@component
class Life:
    hp: int = 100

@component
class Wall:
    normal: tuple = (0, 1)  # Vetor normal da parede

# ------------------------ PROCESSORS -----------------------

class MovementProcessor(esper.Processor):
    def process(self):
        for entity, (circle, velocity) in self.world.get_components(Circle, Velocity):
            gravity = self.world.component_for_entity(entity, Gravity, None)
            wind = self.world.component_for_entity(entity, Wind, None)
            if gravity:
                velocity.vy += gravity.g * dt
            if wind:
                velocity.vx += wind.wx * dt
            circle.x += velocity.vx * dt
            circle.y += velocity.vy * dt

class AppearanceProcessor(esper.Processor):
    def process(self):
        for entity, (circle, color) in self.world.get_components(Circle, Color):
            px.circ(circle.x, circle.y, circle.r, color.c)
            # Desenho adicional (retângulo ao redor)
            px.rect(circle.x - circle.r, circle.y - circle.r, circle.x + circle.r, circle.y + circle.r, color.c)

class WallProcessor(esper.Processor):
    def process(self):
        for entity, (circle, velocity) in self.world.get_components(Circle, Velocity):
            if circle.x < circle.r:  # Parede esquerda
                circle.x = circle.r
                velocity.vx *= -wall_restitution
            elif circle.x > px.width - circle.r:  # Parede direita
                circle.x = px.width - circle.r
                velocity.vx *= -wall_restitution
            if circle.y < circle.r:  # Teto
                circle.y = circle.r
                velocity.vy *= -wall_restitution
            elif circle.y > px.height - circle.r:  # Chão
                circle.y = px.height - circle.r
                velocity.vy *= -wall_restitution

        # Paredes inclinadas
        for wall_entity, wall in self.world.get_component(Wall):
            for entity, (circle, velocity) in self.world.get_components(Circle, Velocity):
                # Aqui você pode implementar a lógica de colisão com paredes inclinadas usando vetores normais
                pass

class CollisionProcessor(esper.Processor):
    def process(self):
        entities = list(self.world.get_components(Circle, Velocity))
        for i, (e1, (c1, v1)) in enumerate(entities):
            for j, (e2, (c2, v2)) in enumerate(entities):
                if i >= j:  # Evitar duplicar verificações
                    continue
                dx = c2.x - c1.x
                dy = c2.y - c1.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance < c1.r + c2.r:  # Colisão detectada
                    # Resolve colisão usando física elástica
                    normal = (dx / distance, dy / distance)
                    rel_velocity = (v1.vx - v2.vx, v1.vy - v2.vy)
                    velocity_along_normal = rel_velocity[0] * normal[0] + rel_velocity[1] * normal[1]
                    if velocity_along_normal > 0:
                        continue
                    impulse = 2 * velocity_along_normal / (c1.m + c2.m)
                    v1.vx -= impulse * normal[0] * c2.m
                    v1.vy -= impulse * normal[1] * c2.m
                    v2.vx += impulse * normal[0] * c1.m
                    v2.vy += impulse * normal[1] * c1.m

class LifeProcessor(esper.Processor):
    def process(self):
        for entity, life in self.world.get_component(Life):
            if life.hp <= 0:
                self.world.delete_entity(entity)

        # Adicione lógica para reduzir vida ao detectar colisões
        for i, (e1, (c1, _)) in enumerate(self.world.get_components(Circle, Life)):
            for j, (e2, (c2, _)) in enumerate(self.world.get_components(Circle, Life)):
                if i >= j:
                    continue
                dx = c2.x - c1.x
                dy = c2.y - c1.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance < c1.r + c2.r:  # Colisão detectada
                    life1 = self.world.component_for_entity(e1, Life)
                    life2 = self.world.component_for_entity(e2, Life)
                    if life1:
                        life1.hp -= 10
                    if life2:
                        life2.hp -= 10

# ------------------------ FUNÇÕES PRINCIPAIS -----------------------

def update():
    pass
def draw():
    px.cls(0)
    esper.process()

# ------------------------ MAIN -----------------------

dt = 0.2
wall_restitution = 1.0

# Inicialização do Pyxel
px.init(100, 100)


# Processadores
esper.add_processor(MovementProcessor())
esper.add_processor(AppearanceProcessor())
esper.add_processor(WallProcessor())
esper.add_processor(CollisionProcessor())
esper.add_processor(LifeProcessor())

# Entidades
esper.create_entity(Circle(x=50, y=50, r=5, m=1), Velocity(vx=10, vy=8), Color(), Gravity(g=5), Life(hp=100))
esper.create_entity(Circle(x=90, y=90, r=10, m=1), Velocity(vx=-6, vy=4), Color(c=10), Wind(wx=1), Life(hp=100))

px.run(update, draw)
