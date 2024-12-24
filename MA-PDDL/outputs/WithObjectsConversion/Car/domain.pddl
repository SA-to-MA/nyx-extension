(define (domain car)
(:requirements :typing :fluents :time :negative-preconditions )
(:types car - object )
(:predicates (running ?car )(engineblown ?car )(transmission_fine ?car )(goal_reached ?car ))
(:functions (d ?car )(v ?car )(a ?car )(up_limit )(down_limit )(running_time ?car ))
(:process moving :parameters (?car ):precondition (and (running ?car )):effect (and (increase (v ?car )(* #t (a ?car )))(increase (d ?car )(* #t (v ?car )))(increase (running_time ?car )(* #t 1 ))))
(:process windresistance :parameters (?car ):precondition (and (running ?car )(>= (v ?car )50 )):effect (decrease (v ?car )(* #t (* 0.1 (* (- (v ?car )50 )(- (v ?car )50 ))))))
(:event engineexplode :parameters (?car ):precondition (and (running ?car )(>= (a ?car )1 )(>= (v ?car )100 )):effect (and (not (running ?car ))(engineblown ?car )(assign (a ?car )0 )))
(:action 
:parameters ()
:precondition (and
)
:effect (and
)
)
)
