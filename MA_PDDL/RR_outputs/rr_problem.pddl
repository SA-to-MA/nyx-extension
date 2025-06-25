(define (problem BLOCKS-4-0) (:domain blocks)
(:objects
	a - block
	c - block
	b - block
	d - block
	e - block

	(:private
        a1 - agent
		a2 - agent
	)
)
(:init
    (= (plan_cost) 0)
    (= (turn e) 7)
    (= (turn d) 6)
    (= (turn c) 5)
    (= (turn b) 4)
    (= (turn a2) 3)
    (= (turn a1) 2)
    (= (turn a) 1)
    (= (cur_turn) 1)
	(handempty a2)
	(handempty a1)
	(clear c)
	(clear d)
	(clear e)
	(ontable b)
	(ontable c)
	(ontable d)
	(on a b)
	(on e a)
)
(:goal
	(and
		(on b a)
		(on c b)
		(on d c)
		(on e d)
	)
)
    (:metric minimize (plan_cost))
)