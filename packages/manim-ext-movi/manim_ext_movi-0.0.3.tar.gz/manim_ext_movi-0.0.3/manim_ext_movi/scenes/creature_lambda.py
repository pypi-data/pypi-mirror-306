from manim import *

from manim_ext_movi.creatures import CreatureLambda


#%%
class CreatureLambdaTest(Scene):
    def construct(self):
        lam = CreatureLambda().scale(0.5)
        dot = Dot().move_to(LEFT + UP)
        self.remove(lam.eyes)
        self.add(lam, dot)
        
        self.play(LaggedStart(
            DrawBorderThenFill(lam.eyes)
        ))
        self.play(lam.animate.become(lam.copy().look_at(dot)))
        self.wait()
        


#%%
if __name__ == '__main__':
    with tempconfig(dict(
        quality='medium_quality',
        preview=True
    )):
        scene = CreatureLambdaTest()
        scene.render()