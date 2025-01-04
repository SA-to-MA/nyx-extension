(define (domain car)
(:requirements :typing :fluents :time :negative-preconditions )
(:types car - object )
(:predicates (running ?car - car )(engineblown ?car - car )(transmission_fine ?car - car )(goal_reached ?car - car )(dif_car ?ob1 - car ?ob2 - car ))
(:functions (d ?car - car )(v ?car - car )(a ?car - car )(up_limit )(down_limit )(running_time ?car - car ))
(:process moving :parameters (?car - car ):precondition (and (running ?car )):effect (and (increase (v ?car )(* #t (a ?car )))(increase (d ?car )(* #t (v ?car )))(increase (running_time ?car )(* #t 1 ))))
(:process windresistance :parameters (?car - car ):precondition (and (running ?car )(>= (v ?car )50 )):effect (decrease (v ?car )(* #t (* 0.1 (* (- (v ?car )50 )(- (v ?car )50 ))))))
(:event engineexplode :parameters (?car - car ):precondition (and (running ?car )(>= (a ?car )1 )(>= (v ?car )100 )):effect (and (not (running ?car ))(engineblown ?car )(assign (a ?car )0 )))
(:action decelerate&stop
:parameters (?car1 - car ?car2 - car)
:precondition (and
(running ?car1 )
(> (a ?car1 )(down_limit ))
(= (v ?car2 )0 )
(>= (d ?car2 )30 )
(not (engineblown ?car2 ))
(goal_reached ?car2 )
(dif_car ?car1 ?car2 )
)
:effect (and
(decrease (a ?car1 )1 )
)
)
(:action no-op_car&no-op_car
:parameters (?a1 - car ?a2 - car)
:precondition (and
(dif_car ?a1 ?a2 )
)
:effect (and
)
)
(:action accelerate&accelerate
:parameters (?car1 - car ?car2 - car)
:precondition (and
(running ?car1 )
(< (a ?car1 )(up_limit ))
(running ?car2 )
(< (a ?car2 )(up_limit ))
(dif_car ?car1 ?car2 )
)
:effect (and
(increase (a ?car1 )1 )
(increase (a ?car2 )1 )
)
)
(:action accelerate&decelerate
:parameters (?car1 - car ?car2 - car)
:precondition (and
(running ?car1 )
(< (a ?car1 )(up_limit ))
(running ?car2 )
(> (a ?car2 )(down_limit ))
(dif_car ?car1 ?car2 )
)
:effect (and
(increase (a ?car1 )1 )
(decrease (a ?car2 )1 )
)
)
(:action stop&stop
:parameters (?car1 - car ?car2 - car)
:precondition (and
(= (v ?car1 )0 )
(>= (d ?car1 )30 )
(not (engineblown ?car1 ))
(goal_reached ?car1 )
(= (v ?car2 )0 )
(>= (d ?car2 )30 )
(not (engineblown ?car2 ))
(goal_reached ?car2 )
(dif_car ?car1 ?car2 )
)
:effect (and
)
)
(:action no-op_car&stop
:parameters (?a1 - car ?car2 - car)
:precondition (and
(= (v ?car2 )0 )
(>= (d ?car2 )30 )
(not (engineblown ?car2 ))
(goal_reached ?car2 )
(dif_car ?a1 ?car2 )
)
:effect (and
)
)
(:action accelerate&no-op_car
:parameters (?car1 - car ?a2 - car)
:precondition (and
(running ?car1 )
(< (a ?car1 )(up_limit ))
(dif_car ?car1 ?a2 )
)
:effect (and
(increase (a ?car1 )1 )
)
)
(:action decelerate&decelerate
:parameters (?car1 - car ?car2 - car)
:precondition (and
(running ?car1 )
(> (a ?car1 )(down_limit ))
(running ?car2 )
(> (a ?car2 )(down_limit ))
(dif_car ?car1 ?car2 )
)
:effect (and
(decrease (a ?car1 )1 )
(decrease (a ?car2 )1 )
)
)
(:action accelerate&stop
:parameters (?car1 - car ?car2 - car)
:precondition (and
(running ?car1 )
(< (a ?car1 )(up_limit ))
(= (v ?car2 )0 )
(>= (d ?car2 )30 )
(not (engineblown ?car2 ))
(goal_reached ?car2 )
(dif_car ?car1 ?car2 )
)
:effect (and
(increase (a ?car1 )1 )
)
)
(:action decelerate&no-op_car
:parameters (?car1 - car ?a2 - car)
:precondition (and
(running ?car1 )
(> (a ?car1 )(down_limit ))
(dif_car ?car1 ?a2 )
)
:effect (and
(decrease (a ?car1 )1 )
)
)
)
