(define (domain car)
(:requirements :typing :fluents :time :negative-preconditions )
(:types agent - object )
(:predicates (running ?a - agent )(engineblown ?a - agent )(transmission_fine ?a - agent )(goal_reached ?a - agent )(dif_agent ?ob1 - agent ?ob2 - agent ))
(:functions (d ?a - agent )(v ?a - agent )(a ?a - agent )(up_limit ?a - agent )(down_limit ?a - agent )(running_time ?a - agent ))
(:process moving :parameters (?a - agent ):precondition (and (running ?a )):effect (and (increase (v ?a )(* #t (a ?a )))(increase (d ?a )(* #t (v ?a )))(increase (running_time ?a )(* #t 1 ))))
(:process windresistance :parameters (?a - agent ):precondition (and (running ?a )(>= (v ?a )50 )):effect (decrease (v ?a )(* #t (* 0.1 (* (- (v ?a )50 )(- (v ?a )50 ))))))
(:event engineexplode :parameters (?a - agent ):precondition (and (running ?a )(>= (a ?a )1 )(>= (v ?a )100 )):effect (and (not (running ?a ))(engineblown ?a )(assign (a ?a )0 )))
(:action accelerate&accelerate
:parameters (?a1 - agent ?a2 - agent)
:precondition (and
(running ?a1 )
(< (a ?a1 )(up_limit ?a1 ))
(running ?a2 )
(< (a ?a2 )(up_limit ?a2 ))
(dif_agent ?a1 ?a2 )
)
:effect (and
(increase (a ?a1 )1 )
(increase (a ?a2 )1 )
)
)
(:action decelerate&stop
:parameters (?a1 - agent ?a2 - agent)
:precondition (and
(running ?a1 )
(> (a ?a1 )(down_limit ?a1 ))
(= (v ?a2 )0 )
(>= (d ?a2 )30 )
(not (engineblown ?a2 ))
(dif_agent ?a1 ?a2 )
)
:effect (and
(decrease (a ?a1 )1 )
(goal_reached ?a2 )
)
)
(:action no-op_agent&no-op_agent
:parameters (?a1 - agent ?a2 - agent)
:precondition (and
(dif_agent ?a1 ?a2 )
)
:effect (and
)
)
(:action accelerate&stop
:parameters (?a1 - agent ?a2 - agent)
:precondition (and
(running ?a1 )
(< (a ?a1 )(up_limit ?a1 ))
(= (v ?a2 )0 )
(>= (d ?a2 )30 )
(not (engineblown ?a2 ))
(dif_agent ?a1 ?a2 )
)
:effect (and
(increase (a ?a1 )1 )
(goal_reached ?a2 )
)
)
(:action decelerate&decelerate
:parameters (?a1 - agent ?a2 - agent)
:precondition (and
(running ?a1 )
(> (a ?a1 )(down_limit ?a1 ))
(running ?a2 )
(> (a ?a2 )(down_limit ?a2 ))
(dif_agent ?a1 ?a2 )
)
:effect (and
(decrease (a ?a1 )1 )
(decrease (a ?a2 )1 )
)
)
(:action decelerate&no-op_agent
:parameters (?a1 - agent ?a2 - agent)
:precondition (and
(running ?a1 )
(> (a ?a1 )(down_limit ?a1 ))
(dif_agent ?a1 ?a2 )
)
:effect (and
(decrease (a ?a1 )1 )
)
)
(:action no-op_agent&stop
:parameters (?a1 - agent ?a2 - agent)
:precondition (and
(= (v ?a2 )0 )
(>= (d ?a2 )30 )
(not (engineblown ?a2 ))
(dif_agent ?a1 ?a2 )
)
:effect (and
(goal_reached ?a2 )
)
)
(:action accelerate&decelerate
:parameters (?a1 - agent ?a2 - agent)
:precondition (and
(running ?a1 )
(< (a ?a1 )(up_limit ?a1 ))
(running ?a2 )
(> (a ?a2 )(down_limit ?a2 ))
(dif_agent ?a1 ?a2 )
)
:effect (and
(increase (a ?a1 )1 )
(decrease (a ?a2 )1 )
)
)
(:action stop&stop
:parameters (?a1 - agent ?a2 - agent)
:precondition (and
(= (v ?a1 )0 )
(>= (d ?a1 )30 )
(not (engineblown ?a1 ))
(= (v ?a2 )0 )
(>= (d ?a2 )30 )
(not (engineblown ?a2 ))
(dif_agent ?a1 ?a2 )
)
:effect (and
(goal_reached ?a1 )
(goal_reached ?a2 )
)
)
(:action accelerate&no-op_agent
:parameters (?a1 - agent ?a2 - agent)
:precondition (and
(running ?a1 )
(< (a ?a1 )(up_limit ?a1 ))
(dif_agent ?a1 ?a2 )
)
:effect (and
(increase (a ?a1 )1 )
)
)
)
