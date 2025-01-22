(define (problem multi-car-problem)
  (:domain car)
  (:requirements :typing :fluents :time)
  (:objects
    (:private
        car1 - agent
        car2 - agent
    )
  )
  (:init
    (running car1)
    (transmission_fine car1)
    (= (d car1) 0)
    (= (v car1) 0)
    (= (a car1) 0)
    (= (up_limit car1) 10)
    (= (down_limit car1) 1)
    (running car2)
    (transmission_fine car2)
    (= (d car2) 0)
    (= (v car2) 0)
    (= (a car2) 0)
    (= (up_limit car2) 12)
    (= (down_limit car2) 2)
  )
  (:goal
    (and
      (goal_reached car1)
      (goal_reached car2)
    )
  )
)
