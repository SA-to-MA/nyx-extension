(define (domain blocks)
	(:requirements :typing)
(:types
	 agent block - object 
 )
(:predicates
    (busy ?object)

	(on ?x - block ?y - block)
	(ontable ?x - block)
	(clear ?x - block)

	(:private
		(holding ?agent - agent ?x - block)
		(handempty ?agent - agent)
	)
)

    (:action stack
        :parameters (?a - agent ?x - block ?y - block)
        :precondition (and
            (holding ?a ?x)
            (clear ?y)
            (not (busy ?a))
            (not (busy ?x))
            (not (busy ?y))
            (= (cur_turn) (turn ?a))
        )
        :effect (and
            (not (holding ?a ?x))
            (not (clear ?y))
            (clear ?x)
            (handempty ?a)
            (on ?x ?y)
            (busy ?a)
            (busy ?x)
            (busy ?y)
            (increase (cur_turn) 1)
        ))


    (:action pick-up
        :parameters (?a - agent ?x - block)
        :precondition (and
            (clear ?x)
            (ontable ?x)
            (handempty ?a)
            (not (busy ?a))
            (not (busy ?x))
            (= (cur_turn) (turn ?a))
        )
        :effect (and
            (not (ontable ?x))
            (not (clear ?x))
            (not (handempty ?a))
            (holding ?a ?x)
            (busy ?a)
            (busy ?x)
            (increase (cur_turn) 1)
        ))



    (:action put-down
        :parameters (?a - agent ?x - block)
        :precondition (and
            (holding ?a ?x)
            (not (busy ?a))
            (not (busy ?x))
            (= (cur_turn) (turn ?a))
        )
        :effect (and
            (not (holding ?a ?x))
            (clear ?x)
            (handempty ?a)
            (ontable ?x)
            (busy ?a)
            (busy ?x)
            (increase (cur_turn) 1)
        ))



    (:action unstack
        :parameters (?a - agent ?x - block ?y - block)
        :precondition (and
            (on ?x ?y)
            (clear ?x)
            (handempty ?a)
            (not (busy ?a))
            (not (busy ?x))
            (not (busy ?y))
            (= (cur_turn) (turn ?a))
        )
        :effect (and
            (holding ?a ?x)
            (clear ?y)
            (not (clear ?x))
            (not (handempty ?a))
            (not (on ?x ?y))
            (busy ?a)
            (busy ?x)
            (busy ?y)
            (increase (cur_turn) 1)
        )

)

    (:action NO_OP
        :parameters ()
        :precondition (and
            (< (cur_turn) 7)
        )
        :effect (and
            (increase (cur_turn) 1)
        )
    )

    (:action PASS_TIME
        :parameters ()
        :precondition (and
            (>= (cur_turn) 7)
            (or (busy a)
(busy a1)
(busy a2)
(busy b)
(busy c)
(busy d)
(busy e))
        )
        :effect (and
            
            (not (busy a))
(not (busy c))
(not (busy b))
(not (busy d))
(not (busy e))
(not (busy private))
(not (busy a1))
(not (busy a2))
            (assign (cur_turn) 1)
            (increase (plan_cost) 1)
        )
    )
)