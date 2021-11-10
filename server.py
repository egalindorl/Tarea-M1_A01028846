from model import RoombaModel, Roomba, ObstacleAgent, Dirt
from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

COLORS = {"Dirty": "#00AA00", "Clean": "#880000"}

def roombaPortrayal(agent):
    if agent is None:
        return

    if (isinstance(agent, Dirt)):
        portrayal = {
            "Shape": "rect",
            "w": 0.7,
            "h": 0.7,
            "Color": "green",
            "Layer": 0,
            "Filled": "true"
        }

    if (isinstance(agent, Roomba)):
        portrayal = {
            "Shape": "circle",
            "Color": "blue",
            "Layer": 1,
            "Filled": "true",
            "r": 0.5
        }

    if (isinstance(agent, ObstacleAgent)):
        portrayal = {
            "Shape": "circle",
            "Color": "grey",
            "Layer": 2,
            "Filled": "true",
            "r": 0.2
        }


    return portrayal

model_parameters = {
    "porcentaje":UserSettableParameter("slider", "Dirt Percentage", 0.6, 0.01, 1.0, 0.1), 
    "n_sliders": UserSettableParameter("number", "Number of sliders", 4, 1, 10, 1),
    "ancho": 10,
    "alto": 10,
    "tiempo": UserSettableParameter("number", "Seconds",60,1,360,5)}

grid = CanvasGrid(roombaPortrayal, 10, 10, 500, 500)

tree_chart = ChartModule(
    [{"Label": "Clean Tiles (in percentage)","Color": "green"}]

)

pie_chart = ChartModule(
    [{"Label": "Movimientos" ,"Color": "orange"}]

)

server = ModularServer(RoombaModel,
                       [grid, pie_chart, tree_chart],
                       "Roomba Cleaning",model_parameters)

server.port = 7979
server.launch()
    



