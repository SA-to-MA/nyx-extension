(define (domain sailing)
(:requirements :typing )
(:types boat person - object )
(:predicates (saved ?t - person )(dif_boat ?ob1 - boat ?ob2 - boat )(dif_person ?ob1 - person ?ob2 - person ))
(:functions (x ?b - boat )(y ?b - boat )(d ?t - person ))
(:action go-south-east
:parameters (?b1 - boat)
:precondition (and
)
:effect (and
(decrease (x ?b1 )2 )
(decrease (y ?b1 )2 )
)
)
(:action go-north-west
:parameters (?b1 - boat)
:precondition (and
)
:effect (and
(decrease (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
)
)
(:action go-north-east
:parameters (?b1 - boat)
:precondition (and
)
:effect (and
(increase (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
)
)
(:action go-east
:parameters (?b1 - boat)
:precondition (and
)
:effect (and
(increase (x ?b1 )3 )
)
)
(:action save-person
:parameters (?b1 - boat ?t1 - person)
:precondition (and
(>= (+ (x ?b1 )(y ?b1 ))(d ?t1 ))
(>= (- (y ?b1 )(x ?b1 ))(d ?t1 ))
(<= (+ (x ?b1 )(y ?b1 ))(+ (d ?t1 )25 ))
(<= (- (y ?b1 )(x ?b1 ))(+ (d ?t1 )25 ))
)
:effect (and
(saved ?t1 )
)
)
(:action go-south
:parameters (?b1 - boat)
:precondition (and
)
:effect (and
(decrease (y ?b1 )2 )
)
)
(:action go-west
:parameters (?b1 - boat)
:precondition (and
)
:effect (and
(decrease (x ?b1 )3 )
)
)
(:action go-south-west
:parameters (?b1 - boat)
:precondition (and
)
:effect (and
(increase (x ?b1 )2 )
(decrease (y ?b1 )2 )
)
)
)
