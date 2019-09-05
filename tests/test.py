from myutils import utils, scheduler

conf = utils.readFile("test_setup.yaml")
def myprint():
    print(conf)
utils.loop(action=myprint)