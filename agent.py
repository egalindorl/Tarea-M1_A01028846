from mesa import Agent

class Roomba(Agent):
    def __init__(self, unique_id, model):

        super().__init__(unique_id, model)

        self.direccion = 4
        self.value = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,

            include_center=True
        )
        self.direccion = (self.random.randint(0,8))

        freeSpaces = []
        for pos in possible_steps:
            var = True

            if self.model.grid.get_cell_list_contents(pos):

                for agent in self.model.grid.get_cell_list_contents(pos):
                    if isinstance(agent, ObstacleAgent):
                        var = False 

            freeSpaces.append(var)
        
        if freeSpaces[self.direccion]:

            self.model.grid.move_agent(self, possible_steps[self.direccion])
            self.value += 1

        for a in self.model.grid.get_cell_list_contents(self.pos):
            
            if(isinstance(a, Dirt)):
                self.model.grid.remove_agent(a)


    
    def step(self):
        pass
    def advance(self):
        self.move()

class ObstacleAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Dirt(Agent):
   
    def __init__(self, pos, model, assignedValue):
        super().__init__(pos,model)
        self.pos = pos
        self.condition = assignedValue

    def step(self):
        if self.pos:
            for a in self.model.grid.get_cell_list_contents(self.pos):
                if(isinstance(a, Roomba)):
                    self.condition = "clean"