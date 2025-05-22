(define (domain sailing)
(:requirements :typing )
(:types boat person - object )
(:predicates (saved ?t - person )(dif_boat ?ob1 - boat ?ob2 - boat )(dif_person ?ob1 - person ?ob2 - person ))
(:functions (x ?b - boat )(y ?b - boat )(d ?t - person ))
(:action go-north-west
:parameters (?b1 - boat)
:precondition (and
)
:effect (and
(decrease (x ?b1 )1.5 )
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
(:action go-north-east
:parameters (?b1 - boat)
:precondition (and
)
:effect (and
(increase (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
)
)
(:action go-south-east
:parameters (?b1 - boat)
:precondition (and
)
:effect (and
(decrease (x ?b1 )2 )
(decrease (y ?b1 )2 )
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
(:action go-north-east&save-person
:parameters (?b1 - boat ?b2 - boat ?t2 - person)
:precondition (and
(>= (+ (x ?b2 )(y ?b2 ))(d ?t2 ))
(>= (- (y ?b2 )(x ?b2 ))(d ?t2 ))
(<= (+ (x ?b2 )(y ?b2 ))(+ (d ?t2 )25 ))
(<= (- (y ?b2 )(x ?b2 ))(+ (d ?t2 )25 ))
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
(saved ?t2 )
)
)
(:action go-west&go-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (x ?b1 )3 )
(decrease (x ?b2 )3 )
)
)
(:action go-south-west&go-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )2 )
(decrease (y ?b1 )2 )
(decrease (x ?b2 )3 )
)
)
(:action go-east&go-south-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )3 )
(increase (x ?b2 )2 )
(decrease (y ?b2 )2 )
)
)
(:action go-south-east&go-south-east
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (x ?b1 )2 )
(decrease (y ?b1 )2 )
(decrease (x ?b2 )2 )
(decrease (y ?b2 )2 )
)
)
(:action go-south-east&go-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (x ?b1 )2 )
(decrease (y ?b1 )2 )
(decrease (x ?b2 )3 )
)
)
(:action go-west&save-person
:parameters (?b1 - boat ?b2 - boat ?t2 - person)
:precondition (and
(>= (+ (x ?b2 )(y ?b2 ))(d ?t2 ))
(>= (- (y ?b2 )(x ?b2 ))(d ?t2 ))
(<= (+ (x ?b2 )(y ?b2 ))(+ (d ?t2 )25 ))
(<= (- (y ?b2 )(x ?b2 ))(+ (d ?t2 )25 ))
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (x ?b1 )3 )
(saved ?t2 )
)
)
(:action go-north-west&go-south-east
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
(decrease (x ?b2 )2 )
(decrease (y ?b2 )2 )
)
)
(:action go-north-west&go-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
(decrease (x ?b2 )3 )
)
)
(:action go-north-west&go-south
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
(decrease (y ?b2 )2 )
)
)
(:action go-south&go-south-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (y ?b1 )2 )
(increase (x ?b2 )2 )
(decrease (y ?b2 )2 )
)
)
(:action go-south-west&save-person
:parameters (?b1 - boat ?b2 - boat ?t2 - person)
:precondition (and
(>= (+ (x ?b2 )(y ?b2 ))(d ?t2 ))
(>= (- (y ?b2 )(x ?b2 ))(d ?t2 ))
(<= (+ (x ?b2 )(y ?b2 ))(+ (d ?t2 )25 ))
(<= (- (y ?b2 )(x ?b2 ))(+ (d ?t2 )25 ))
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )2 )
(decrease (y ?b1 )2 )
(saved ?t2 )
)
)
(:action go-north-west&go-north-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
(decrease (x ?b2 )1.5 )
(increase (y ?b2 )1.5 )
)
)
(:action go-north-east&go-south-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
(increase (x ?b2 )2 )
(decrease (y ?b2 )2 )
)
)
(:action go-south-east&save-person
:parameters (?b1 - boat ?b2 - boat ?t2 - person)
:precondition (and
(>= (+ (x ?b2 )(y ?b2 ))(d ?t2 ))
(>= (- (y ?b2 )(x ?b2 ))(d ?t2 ))
(<= (+ (x ?b2 )(y ?b2 ))(+ (d ?t2 )25 ))
(<= (- (y ?b2 )(x ?b2 ))(+ (d ?t2 )25 ))
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (x ?b1 )2 )
(decrease (y ?b1 )2 )
(saved ?t2 )
)
)
(:action go-north-west&save-person
:parameters (?b1 - boat ?b2 - boat ?t2 - person)
:precondition (and
(>= (+ (x ?b2 )(y ?b2 ))(d ?t2 ))
(>= (- (y ?b2 )(x ?b2 ))(d ?t2 ))
(<= (+ (x ?b2 )(y ?b2 ))(+ (d ?t2 )25 ))
(<= (- (y ?b2 )(x ?b2 ))(+ (d ?t2 )25 ))
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
(saved ?t2 )
)
)
(:action go-east&go-north-east
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )3 )
(increase (x ?b2 )1.5 )
(increase (y ?b2 )1.5 )
)
)
(:action go-east&go-south-east
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )3 )
(decrease (x ?b2 )2 )
(decrease (y ?b2 )2 )
)
)
(:action go-east&go-south
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )3 )
(decrease (y ?b2 )2 )
)
)
(:action save-person&save-person
:parameters (?b1 - boat ?t1 - person ?b2 - boat ?t2 - person)
:precondition (and
(>= (+ (x ?b1 )(y ?b1 ))(d ?t1 ))
(>= (- (y ?b1 )(x ?b1 ))(d ?t1 ))
(<= (+ (x ?b1 )(y ?b1 ))(+ (d ?t1 )25 ))
(<= (- (y ?b1 )(x ?b1 ))(+ (d ?t1 )25 ))
(>= (+ (x ?b2 )(y ?b2 ))(d ?t2 ))
(>= (- (y ?b2 )(x ?b2 ))(d ?t2 ))
(<= (+ (x ?b2 )(y ?b2 ))(+ (d ?t2 )25 ))
(<= (- (y ?b2 )(x ?b2 ))(+ (d ?t2 )25 ))
(dif_boat ?b1 ?b2 )
(dif_person ?t1 ?t2 )
)
:effect (and
(saved ?t1 )
(saved ?t2 )
)
)
(:action go-south-west&go-south-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )2 )
(decrease (y ?b1 )2 )
(increase (x ?b2 )2 )
(decrease (y ?b2 )2 )
)
)
(:action go-east&go-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )3 )
(decrease (x ?b2 )3 )
)
)
(:action go-north-east&go-north-east
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
(increase (x ?b2 )1.5 )
(increase (y ?b2 )1.5 )
)
)
(:action go-south&go-south-east
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (y ?b1 )2 )
(decrease (x ?b2 )2 )
(decrease (y ?b2 )2 )
)
)
(:action go-east&go-north-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )3 )
(decrease (x ?b2 )1.5 )
(increase (y ?b2 )1.5 )
)
)
(:action go-south-east&go-south-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (x ?b1 )2 )
(decrease (y ?b1 )2 )
(increase (x ?b2 )2 )
(decrease (y ?b2 )2 )
)
)
(:action go-south&go-south
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (y ?b1 )2 )
(decrease (y ?b2 )2 )
)
)
(:action go-north-east&go-south-east
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
(decrease (x ?b2 )2 )
(decrease (y ?b2 )2 )
)
)
(:action go-north-west&go-south-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
(increase (x ?b2 )2 )
(decrease (y ?b2 )2 )
)
)
(:action go-south&go-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (y ?b1 )2 )
(decrease (x ?b2 )3 )
)
)
(:action go-north-east&go-south
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
(decrease (y ?b2 )2 )
)
)
(:action go-east&save-person
:parameters (?b1 - boat ?b2 - boat ?t2 - person)
:precondition (and
(>= (+ (x ?b2 )(y ?b2 ))(d ?t2 ))
(>= (- (y ?b2 )(x ?b2 ))(d ?t2 ))
(<= (+ (x ?b2 )(y ?b2 ))(+ (d ?t2 )25 ))
(<= (- (y ?b2 )(x ?b2 ))(+ (d ?t2 )25 ))
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )3 )
(saved ?t2 )
)
)
(:action go-north-east&go-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
(decrease (x ?b2 )3 )
)
)
(:action go-north-east&go-north-west
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )1.5 )
(increase (y ?b1 )1.5 )
(decrease (x ?b2 )1.5 )
(increase (y ?b2 )1.5 )
)
)
(:action go-south&save-person
:parameters (?b1 - boat ?b2 - boat ?t2 - person)
:precondition (and
(>= (+ (x ?b2 )(y ?b2 ))(d ?t2 ))
(>= (- (y ?b2 )(x ?b2 ))(d ?t2 ))
(<= (+ (x ?b2 )(y ?b2 ))(+ (d ?t2 )25 ))
(<= (- (y ?b2 )(x ?b2 ))(+ (d ?t2 )25 ))
(dif_boat ?b1 ?b2 )
)
:effect (and
(decrease (y ?b1 )2 )
(saved ?t2 )
)
)
(:action go-east&go-east
:parameters (?b1 - boat ?b2 - boat)
:precondition (and
(dif_boat ?b1 ?b2 )
)
:effect (and
(increase (x ?b1 )3 )
(increase (x ?b2 )3 )
)
)
)
