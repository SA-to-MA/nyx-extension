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
		a3 - agent
		a4 - agent
	)
)
(:init
	(handempty a2)
	(handempty a1)
	(handempty a3)
	(handempty a4)
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
		(ontable e)
		(ontable b)
		(on c b)
		(on d c)
		(on a e)
	)
)
)