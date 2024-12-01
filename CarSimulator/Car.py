class Car:
    def __init__(self, running, engine, trans, d, v, a, up, down):
        # Predicates
        self.running = running
        self.engine_blown = engine
        self.transmission_fine = trans
        self.goal_reached = False
        # Functions
        self.d = d  # distance
        self.v = v  # Velocity
        self.a = a  # Acceleration
        self.up_limit = up  # Upper acceleration limit
        self.down_limit = down  # Lower acceleration limit
        self.running_time = 0  # Running time in seconds

    # Processes
    def moving(self, time_elapsed=1):
        if self.running:
            self.v += self.a * time_elapsed
            self.d += self.v * time_elapsed
            self.running_time += time_elapsed

    def wind_resistance(self, time_elapsed=1):
        if self.running and self.v >= 50:
            self.v -= time_elapsed * 0.1 * ((self.v - 50) ** 2)
            self.v = max(0, self.v)  # Velocity cannot be negative

    # Actions
    def accelerate(self):
        if self.running and self.a < self.up_limit:
            self.a += 1

    def decelerate(self):
        if self.running and self.a > self.down_limit:
            self.a -= 1

    def stop(self):
        if not self.engine_blown and self.v == 0 and self.d >= 30:
            self.goal_reached = True

    # Events
    def engine_explode(self):
        if self.running and self.a >= 1 and self.v >= 100:
            self.running = False
            self.engine_blown = True
            self.a = 0

    # State display
    def __str__(self):
        return (f"Running: {self.running}, Engine Blown: {self.engine_blown}, "
                f"Distance: {self.d:.2f}, Velocity: {self.v:.2f}, "
                f"Acceleration: {self.a}, Running Time: {self.running_time:.2f}, "
                f"Goal Reached: {self.goal_reached}")
