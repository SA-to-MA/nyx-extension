(define (domain blocks)
(:requirements :typing )
(:types agent block - object )
(:predicates (on ?x - block ?y - block )(ontable ?x - block )(clear ?x - block )(holding ?agent - agent ?x - block )(handempty ?agent - agent ))
(:action stack
:parameters (?a1 - agent ?x1 - block ?y1 - block)
:precondition (and
(holding ?a1 ?x1 )
(clear ?y1 )
)
:effect (and
(not (holding ?a1 ?x1 ))
(not (clear ?y1 ))
(clear ?x1 )
(handempty ?a1 )
(on ?x1 ?y1 )
)
)
(:action unstack
:parameters (?a1 - agent ?x1 - block ?y1 - block)
:precondition (and
(on ?x1 ?y1 )
(clear ?x1 )
(handempty ?a1 )
)
:effect (and
(holding ?a1 ?x1 )
(clear ?y1 )
(not (clear ?x1 ))
(not (handempty ?a1 ))
(not (on ?x1 ?y1 ))
)
)
(:action pick-up
:parameters (?a1 - agent ?x1 - block)
:precondition (and
(clear ?x1 )
(ontable ?x1 )
(handempty ?a1 )
)
:effect (and
(not (ontable ?x1 ))
(not (clear ?x1 ))
(not (handempty ?a1 ))
(holding ?a1 ?x1 )
)
)
(:action put-down
:parameters (?a1 - agent ?x1 - block)
:precondition (and
(holding ?a1 ?x1 )
)
:effect (and
(not (holding ?a1 ?x1 ))
(clear ?x1 )
(handempty ?a1 )
(ontable ?x1 )
)
)
)
