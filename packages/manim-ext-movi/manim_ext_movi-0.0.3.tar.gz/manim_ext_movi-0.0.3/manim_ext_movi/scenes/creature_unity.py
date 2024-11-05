from manim import *

from manim_ext_movi.creatures import CreatureUnity


#%%
class CreatureUnityTest(Scene):
    def construct(self):
        unity = CreatureUnity().scale(0.5)
        dot = Dot().move_to(LEFT + UP)
        self.remove(unity.eyeL_grp, unity.eyeR_grp)
        self.add(unity, dot)
        
        self.play(LaggedStart(
            DrawBorderThenFill(unity.eyeL_grp),
            DrawBorderThenFill(unity.eyeR_grp)
            ))
        self.play(unity.look_at(dot))
        self.wait()
        
        unity_copy = unity.copy()
        self.play(unity.smile())
        self.play(unity.look_at(dot))
        self.wait()
        unity.generate_target()
        unity.target.stretch(2,0)
        unity.target.stretch(0.5,1)
        self.play(MoveToTarget(unity))
        
        unity.generate_target()
        unity.target.stretch(2,0)
        unity.target.stretch(0.5,1)
        self.play(MoveToTarget(unity))
        
        unity.generate_target()
        unity.target.stretch(2,0)
        unity.target.stretch(0.5,1)
        self.play(MoveToTarget(unity))
        self.wait()
        

        self.play(Transform(unity, unity_copy))
        self.wait()


#%%
if __name__ == '__main__':
    with tempconfig(dict(
        quality='medium_quality',
        preview=True
    )):
        scene = CreatureUnityTest()
        scene.render()