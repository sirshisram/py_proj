from star_sys_main import Sys, Star_Body, Planet_Body

system = Sys(400, proj_2d=True)

star = Star_Body(system)

planets = (Planet_Body(# 1
                       system,
                       mass=45,
                       position=(80, 12, -12),
                       velocity=(20, 30, 25),
                       ),
           Planet_Body(# 2
                       system,
                       mass=40,
                       position=(100, 130, 150),
                       velocity=(25, 3, 2),
                       ),
            Planet_Body(# 3
                       system,
                       mass=40,
                       position=(120, -90, -100),
                       velocity=(-25, -3, -2),
                       ))
for i in range(10000):
    system.calc_interxn()
    system.update_all()
    system.render_all()
    
    
    