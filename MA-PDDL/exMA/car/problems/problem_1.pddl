(define (problem ma-car-problem)
  (:domain ma-car)

  (:objects
    car1 car2 - car
  )

  (:init
    (running car1)    ; Car1 is running
    (running car2)    ; Car2 is running
    (not (engineBlown car1))  ; Car1's engine is not blown
    (not (engineBlown car2))  ; Car2's engine is not blown
    (not (goal_reached car1)) ; Car1 has not reached the goal yet
    (not (goal_reached car2)) ; Car2 has not reached the goal yet
    (>= (up_limit car1) 10)   ; Car1's acceleration limit
    (>= (up_limit car2) 10)   ; Car2's acceleration limit
    (<= (down_limit car1) 0)  ; Car1's deceleration limit
    (<= (down_limit car2) 0)  ; Car2's deceleration limit
    (= (v car1) 0)  ; Car1 starts with speed 0
    (= (v car2) 0)  ; Car2 starts with speed 0
    (= (a car1) 0)  ; Car1 starts with acceleration 0
    (= (a car2) 0)  ; Car2 starts with acceleration 0
    (= (d car1) 0)  ; Car1 starts at distance 0
    (= (d car2) 0)  ; Car2 starts at distance 0
    (= (running_time car1) 0)  ; Car1's running time is 0
    (= (running_time car2) 0)  ; Car2's running time is 0
  )

  (:goal
    (and
      (goal_reached car1)  ; Car1 has reached its goal
      (goal_reached car2)  ; Car2 has reached its goal
    )
  )
)
