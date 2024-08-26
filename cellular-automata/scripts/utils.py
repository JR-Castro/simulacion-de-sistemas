from os import listdir
from os.path import join, isfile

STATIC_3D_PATH = '../src/main/resources/static/3d'
STATIC_2D_PATH = '../src/main/resources/static/2d'

DYNAMIC_3D_PATH = '../src/main/resources/dynamic/3d'
DYNAMIC_2D_PATH = '../src/main/resources/dynamic/2d'

OUTPUT_3D_PATH = '../output/3d'
OUTPUT_2D_PATH = '../output/2d'

RUN_SIMULATION_CMD = 'java -jar ../target/cellular-automata-1.0-SNAPSHOT-jar-with-dependencies.jar'

RUN_ITERATIONS = 10
PERCENTAGES = [(i+1) * 0.1 for i in range(10)]

STATIC_FILES_3D = [f for f in listdir(STATIC_3D_PATH) if isfile(join(STATIC_3D_PATH, f))]
STATIC_FILES_2D = [f for f in listdir(STATIC_2D_PATH) if isfile(join(STATIC_2D_PATH, f))]
