(define (domain car)
(:requirements :typing :fluents :time :negative-preconditions)
(:types agent - object)
(:predicates
    (running ?a - agent)
    (engineBlown ?a - agent)
    (transmission_fine ?a - agent)
    (goal_reached ?a - agent)
)
(:functions
    (d ?a - agent)
    (v ?a - agent)
    (a ?a - agent)
    (up_limit ?a - agent)
    (down_limit ?a - agent)
    (running_time ?a - agent)
)

(:process moving
    :parameters (?a - agent)
    :precondition (and (running ?a))
    :effect (and
        (increase (v ?a) (* #t (a ?a)))
        (increase (d ?a) (* #t (v ?a)))
        (increase (running_time ?a) (* #t 1))
    )
)

(:process windResistance
    :parameters (?a - agent)
    :precondition (and (running ?a) (>= (v ?a) 50))
    :effect (decrease (v ?a) (* #t (* 0.1 (* (- (v ?a) 50) (- (v ?a) 50)))))
)

(:action accelerate
    :parameters (?a - agent)
    :precondition (and (running ?a) (< (a ?a) (up_limit ?a)))
    :effect (and (increase (a ?a) 1))
)

(:action decelerate
    :parameters (?a - agent)
    :precondition (and (running ?a) (> (a ?a) (down_limit ?a)))
    :effect (and (decrease (a ?a) 1))
)

(:event engineExplode
    :parameters (?a - agent)
    :precondition (and (running ?a) (>= (a ?a) 1) (>= (v ?a) 100))
    :effect (and (not (running ?a)) (engineBlown ?a) (assign (a ?a) 0))
)

(:action stop
    :parameters (?a - agent)
    :precondition (and (= (v ?a) 0) (>= (d ?a) 30) (not (engineBlown ?a)))
    :effect (goal_reached ?a)
)
)