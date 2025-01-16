(define (domain blocks)
(:requirements :typing )
(:types agent block - object )
(:predicates (on ?x - block ?y - block )(ontable ?x - block )(clear ?x - block )(holding ?agent - agent ?x - block )(handempty ?agent - agent )(dif_agent ?ob1 - agent ?ob2 - agent )(dif_block ?ob1 - block ?ob2 - block ))
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
(:action unstack
:parameters (?a1 - agent ?x1 - block ?y1 - block)
:precondition (and
(on ?x1 ?y1 )
(clear ?x1 )
(handempty ?a1 )
(dif_block ?x1 ?y1 )
)
:effect (and
(holding ?a1 ?x1 )
(clear ?y1 )
(not (clear ?x1 ))
(not (handempty ?a1 ))
(not (on ?x1 ?y1 ))
)
)
(:action no-op_agent
:parameters (?a1 - agent)
:precondition (and
)
:effect (and
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
(:action stack
:parameters (?a1 - agent ?x1 - block ?y1 - block)
:precondition (and
(holding ?a1 ?x1 )
(clear ?y1 )
(dif_block ?x1 ?y1 )
)
:effect (and
(not (holding ?a1 ?x1 ))
(not (clear ?y1 ))
(clear ?x1 )
(handempty ?a1 )
(on ?x1 ?y1 )
)
)
)
