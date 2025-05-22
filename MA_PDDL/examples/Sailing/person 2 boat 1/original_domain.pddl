(define (domain sailing)
  (:requirements :typing)

  (:types
    boat person - object
  )

  (:predicates
    (saved ?t - person)

  )

  (:functions
    (x ?b - boat)
    (y ?b - boat)
    (d ?t - person)
  )

  (:action go-north-east
    :parameters (?b - boat)
    :precondition ()
    :effect (and
      (increase (x ?b) 1.5)
      (increase (y ?b) 1.5)
    )
  )

  (:action go-north-west
    :parameters (?b - boat)
    :precondition ()
    :effect (and
      (decrease (x ?b) 1.5)
      (increase (y ?b) 1.5)
    )
  )

  (:action go-east
    :parameters (?b - boat)
    :precondition ()
    :effect (increase (x ?b) 3)
  )

  (:action go-west
    :parameters (?b - boat)
    :precondition ()
    :effect (decrease (x ?b) 3)
  )

  (:action go-south-west
    :parameters (?b - boat)
    :precondition ()
    :effect (and
      (increase (x ?b) 2)
      (decrease (y ?b) 2)
    )
  )

  (:action go-south-east
    :parameters (?b - boat)
    :precondition ()
    :effect (and
      (decrease (x ?b) 2)
      (decrease (y ?b) 2)
    )
  )

  (:action go-south
    :parameters (?b - boat)
    :precondition ()
    :effect (decrease (y ?b) 2)
  )

  (:action save-person
    :parameters (?b - boat ?t - person)
    :precondition (and
      (>= (+ (x ?b) (y ?b)) (d ?t))
      (>= (- (y ?b) (x ?b)) (d ?t))
      (<= (+ (x ?b) (y ?b)) (+ (d ?t) 25))
      (<= (- (y ?b) (x ?b)) (+ (d ?t) 25))
    )
    :effect (saved ?t)
  )
)
