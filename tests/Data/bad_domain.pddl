(define (domain bad)
(:predicates (at ?x - location)
(:action move
:parameters (?x - location ?y - location)
:precondition (at ?x)
:effect (at ?y)  //missing precondition
)
(:action move2
