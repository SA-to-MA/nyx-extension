(define (problem BLOCKS-4-0) (:domain blocks)
(:objects
	a - block
	b - block
	c - block
	d - block

    a3 - agent
)
(:init
	(handempty a3)
	(clear a)
	(clear c)
	(clear d)
	(ontable a)
	(ontable b)
	(ontable d)
	(on c b)
)
(:goal
	(and
		(on b a)
		(on c b)
		(on d c)
	)
)
)