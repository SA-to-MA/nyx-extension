(define (problem car_prob)
  (:domain car)
(:objects
	(:private
		car1 - car
		car2 - car
	)
)

  (:init
    (running car1)
    (transmission_fine car1)
    (= (running_time car1) 0)
    (= (up_limit) 1)
    (= (down_limit) -1)
    (= (d car1) 0)
    (= (a car1) 0)
    (= (v car1) 0)
    (running car2)
    (transmission_fine car2)
    (= (running_time car2) 0)
    (= (d car2) 0)
    (= (a car2) 0)
    (= (v car2) 0)
  )

  ;; Goal state for both cars
  (:goal
    (and
      (goal_reached car1)
      (goal_reached car2)
      (not (engineBlown car1))
      (not (engineBlown car2))
      (<= (running_time car1) 50)
      (<= (running_time car2) 50)
      (transmission_fine car1)
      (transmission_fine car2)
    )
  )

  ;; Minimize total time (this applies to both cars)
  (:metric minimize (total-time))
)
