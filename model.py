from mesa.time import SimultaneousActivation
from mesa.space import Grid
from mesa import Model
from mesa.datacollection import DataCollector
from agent import Roomba, ObstacleAgent, Dirt
import time

#Numero celdas sucias


class RoombaModel(Model):
    def __init__(self, n_sliders, alto, ancho, porcentaje, tiempo):

        #totalCeldas = ancho*alto
        #nSucias = ((totalCeldas) * porcentaje)/100
        #nLimpias = int(totalCeldas - nSucias)

        global start_time
        start_time = time.time_ns() 
        start_time = start_time + (tiempo*1000000000)
        print(tiempo)
        self.num_agents = n_sliders
        self.schedule = SimultaneousActivation(self)
        self.grid = Grid(alto, ancho, torus=False)
        self.time = tiempo
        # self.cleanCells = (alto*ancho)-porcentaje(alto*ancho)

        global movimientosCount 
        movimientosCount = 0

        self.datacollector = DataCollector(
            {
                #"Clean Tiles (in percentage)": lambda m: ((nLimpias)*100)/totalCeldas,
                #"Clean Tiles (in percentage)": lambda m: ((int(ancho*alto - ((ancho*alto) * porcentaje)/100))*100)/ancho*alto,

                "Movimientos": lambda m: self.count_moves(m),
                "Clean Tiles (in percentage)": lambda m: self.count_type(m),
            }
        )

        numObs = (ancho * 2) + (alto * 2 - 4)
        listaPosLimite = [(col, ren) for col in [0, ancho-1]
                          for ren in range(alto)]

        for col in range(1, ancho-1):
            for ren in [0, alto-1]:
                listaPosLimite.append((col, ren))

        for i in range(numObs):
            a = ObstacleAgent(i+1000, self)
            self.schedule.add(a)
            self.grid.place_agent(a, listaPosLimite[i])

        for i in range(self.num_agents):
            a = Roomba(i+2000, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))

        for (contents, x, y) in self.grid.coord_iter():
            if (self.grid.is_cell_empty((x, y)) and self.random.random() < porcentaje):
                new_dirt = Dirt((x, y), self, 'Dirt')
                self.grid.place_agent(new_dirt, (x, y))
                self.schedule.add(new_dirt)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        #if self.count_type(self, 'Dirty') == 0:
        #    self.running = False
        current_time = time.time_ns()
        print(current_time - start_time)
        if current_time >= start_time:
            self.running = False
        
    @staticmethod
    def count_type(model):
        count  = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Dirt):
                if agent.condition == 'Dirt':
                    count += 1
        return ((64 - count)*100) / 64

    @staticmethod
    def count_moves(model):
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Roomba):
                    count += agent.value
        return count