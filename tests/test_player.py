
from examples.play_model import main
# from examples.tkplay import tkmain


def test_main():
    main(render=True, n_steps=20, n_trials=2, sGL="PIL")

