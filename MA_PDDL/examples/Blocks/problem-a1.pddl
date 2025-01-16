(define (problem BLOCKS-4-0) (:domain blocks)
(:objects
	a - block
	c - block
	b - block

	(:private
		a1 - agent
		a2 - agent
	)
)
(:init
	(handempty a1)
	(handempty a2)
	(clear c)
	(clear a)
	(ontable a)
	(ontable b)
	(on c b)
)
(:goal
	(and
		(on c b)
		(on b a)
	)
)
)