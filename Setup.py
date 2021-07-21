import cx_Freeze

executables = [cx_Freeze.Executable("Ball Blast.py")]

cx_Freeze.setup(
    name="Ball Blast",
    options={"build_exe":{"packages":["pygame"],"include_files":["Ball Blast.py","bullet.png"]}},
    description = "Ball Blast",
    executables = executables
    )


