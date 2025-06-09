(define (problem BLOCKS-4-0) (:domain blocks)
(:objects
	a - block
	c - block
	b - block
	d - block
	e - block
    a1 - agent
	a2 - agent
)
(:init
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
)