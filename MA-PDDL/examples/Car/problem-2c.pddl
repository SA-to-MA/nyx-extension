(define (problem ma-car-problem)
  (:domain ma-car)

  (:private
    car1 car2 - car
  )

  (:init
    (running car1)
    (running car2)
    (not (engineBlown car1))
    (not (engineBlown car2))
    (not (goal_reached car1))
    (not (goal_reached car2))
    (>= (up_limit car1) 10)
    (>= (up_limit car2) 10)
    (<= (down_limit car1) 0)
    (<= (down_limit car2) 0)
    (= (v car1) 0)
    (= (v car2) 0)
    (= (a car1) 0)
    (= (a car2) 0)
    (= (d car1) 0)
    (= (d car2) 0)
    (= (running_time car1) 0)
    (= (running_time car2) 0)
  )

  (:goal
    (and
      (goal_reached car1)
      (goal_reached car2)
    )
  )
)
