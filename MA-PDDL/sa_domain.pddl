(define (domain car-ma)
(:requirements :typing :fluents :time :negative-preconditions :multi-agent)
(:types agent)

(:predicates
(running ?agent - agent)
(engineBlown ?agent - agent)
(transmission_fine ?agent - agent)
(goal_reached ?agent - agent)
)

(:functions
(d ?agent - agent)
(v ?agent - agent)
(a ?agent - agent)
(up_limit ?agent - agent)
(down_limit ?agent - agent)
(running_time ?agent - agent)
)

(:process moving
:parameters (?agent - agent)
:precondition (and (running ?agent))
:effect (and
(increase (v ?agent) (* #t (a ?agent)))
(increase (d ?agent) (* #t (v ?agent)))
(increase (running_time ?agent) (* #t 1))
)
)

(:process windResistance
:parameters (?agent - agent)
:precondition (and (running ?agent) (>= (v ?agent) 50))
:effect (decrease (v ?agent) (* #t (* 0.1 (* (- (v ?agent) 50) (- (v ?agent) 50)))))
)

(:action accelerate
:parameters ()
:precondition (and (running ?agent) (< (a ?agent) (up_limit ?agent)))
:effect (and (increase (a ?agent) 1))
)

(:action decelerate
:parameters ()
:precondition (and (running ?agent) (> (a ?agent) (down_limit ?agent)))
:effect (and (decrease (a ?agent) 1))
)

(:event engineExplode
:parameters (?agent - agent)
:precondition (and (running ?agent) (>= (a ?agent) 1) (>= (v ?agent) 100))
:effect (and (not (running ?agent)) (engineBlown ?agent) (assign (a ?agent) 0))
)

(:action stop
:parameters ()
:precondition (and (= (v ?agent) 0) (>= (d ?agent) 30) (not (engineBlown ?agent)))
:effect (goal_reached ?agent)
)
)