; MALFORMED FILE: missing closing parentheses and invalid predicate definition
(define (domain blocks)
(:predicates (at ?x - location)
(:action move
:parameters (?x - location ?y - location)
:precondition (at ?x)
:effect (at ?y)  //missing precondition
)
(:action move2
