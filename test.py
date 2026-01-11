import tcod

con = tcod.console.Console(10, 2)

BLUE, YELLOW, BLACK = (0, 0, 255), (255, 255, 0), (0, 0, 0)

con.rgb[0, 0] = ord("@"), YELLOW, BLACK

print(f"{con.rgb[0, 0]=}")
con.rgb[0, 0]=(64, [255, 255,   0], [0, 0, 0])

con.rgb["bg"] = BLUE

print(f"{con.rgb[:, 0]=}")