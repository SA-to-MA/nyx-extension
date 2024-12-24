(define (domain car)
  (:requirements :typing :fluents :time :negative-preconditions)
  (:types
	 car - object
 )
  (:predicates
    (running ?car)            ;; Car is running
    (engineBlown ?car)        ;; Car engine is blown
    (transmission_fine ?car)  ;; Car's transmission is fine
    (goal_reached ?car)       ;; Car has reached its goal
  )
  (:functions
    (d ?car)          ; distance for the car
    (v ?car)          ; speed of the car
    (a ?car)          ; acceleration of the car
    (up_limit)        ; upper limit for acceleration
    (down_limit)      ; lower limit for acceleration
    (running_time ?car) ; running time of the car
  )

  ;; Process to simulate the car moving
  (:process moving
    :parameters (?car)
    :precondition (and (running ?car))
    :effect (and
      (increase (v ?car) (* #t (a ?car)))
      (increase (d ?car) (* #t (v ?car)))
      (increase (running_time ?car) (* #t 1))
    )
  )

  ;; Process for wind resistance that activates when speed is over 50
  (:process windResistance
    :parameters (?car)
    :precondition (and (running ?car) (>= (v ?car) 50))
    :effect (decrease (v ?car) (* #t (* 0.1 (* (- (v ?car) 50) (- (v ?car) 50)))))
  )

  ;; Action to accelerate the car
  (:action accelerate
    :parameters (?car)
    :precondition (and (running ?car) (< (a ?car) (up_limit)))
    :effect (and (increase (a ?car) 1))
  )

  ;; Action to decelerate the car
  (:action decelerate
    :parameters (?car)
    :precondition (and (running ?car) (> (a ?car) (down_limit)))
    :effect (and (decrease (a ?car) 1))
  )

  ;; Event when the engine explodes due to over-speed or high acceleration
  (:event engineExplode
    :parameters (?car)
    :precondition (and (running ?car) (>= (a ?car) 1) (>= (v ?car) 100))
    :effect (and (not (running ?car)) (engineBlown ?car) (assign (a ?car) 0))
  )

  ;; Action to stop the car if conditions are met
  (:action stop
    :parameters (?car)
    :precondition (and (= (v ?car) 0) (>= (d ?car) 30) (not (engineBlown ?car)))
    :effect (goal_reached ?car)
  )
)
