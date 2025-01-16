(define (domain car)
  (:requirements :typing :fluents :time :negative-preconditions)

  ;; Define types
  (:types
    car - object     ;; Car is an object type
  )

  ;; Define predicates with object types
  (:predicates
    (running ?car - car)            ;; Car is running
    (engineBlown ?car - car)        ;; Car engine is blown
    (transmission_fine ?car - car)  ;; Car's transmission is fine
    (goal_reached ?car - car)       ;; Car has reached its goal
  )

  ;; Define functions with object types
  (:functions
    (d ?car - car)          ; Distance for the car
    (v ?car - car)          ; Speed of the car
    (a ?car - car)          ; Acceleration of the car
    (up_limit)              ; Upper limit for acceleration (no object needed)
    (down_limit)            ; Lower limit for acceleration (no object needed)
    (running_time ?car - car) ; Running time of the car
  )

  ;; Process to simulate the car moving
  (:process moving
    :parameters (?car - car)
    :precondition (and (running ?car))
    :effect (and
      (increase (v ?car) (* #t (a ?car)))
      (increase (d ?car) (* #t (v ?car)))
      (increase (running_time ?car) (* #t 1))
    )
  )

  ;; Process for wind resistance that activates when speed is over 50
  (:process windResistance
    :parameters (?car - car)
    :precondition (and (running ?car) (>= (v ?car) 50))
    :effect (decrease (v ?car) (* #t (* 0.1 (* (- (v ?car) 50) (- (v ?car) 50))))))

  ;; Action to accelerate the car
  (:action accelerate
    :parameters (?car - car)
    :precondition (and (running ?car) (< (a ?car) (up_limit)))
    :effect (and (increase (a ?car) 1))
  )

  ;; Action to decelerate the car
  (:action decelerate
    :parameters (?car - car)
    :precondition (and (running ?car) (> (a ?car) (down_limit)))
    :effect (and (decrease (a ?car) 1))
  )

  ;; Event when the engine explodes due to over-speed or high acceleration
  (:event engineExplode
    :parameters (?car - car)
    :precondition (and (running ?car) (>= (a ?car) 1) (>= (v ?car) 100))
    :effect (and (not (running ?car)) (engineBlown ?car) (assign (a ?car) 0))
  )

  ;; Action to stop the car if conditions are met
  (:action stop
    :parameters (?car - car)
    :precondition (and (= (v ?car) 0) (>= (d ?car) 30) (not (engineBlown ?car)))
    :effect (goal_reached ?car)
  )
)
