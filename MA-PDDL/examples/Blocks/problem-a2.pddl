(define (problem BLOCKS-4-0) (:domain blocks)
(:objects
	a - block
	c - block
	b - block
	d - block

	(:private
        a1 - agent
		a2 - agent
	)
)
(:init
	(handempty a2)
	(handempty a1)
	(clear c)
	(clear d)
	(clear a)
	(ontable b)
	(ontable c)
	(ontable d)
	(on a b)
)
(:goal
	(and
		(on b a)
		(on c b)
		(on d c)
	)
)
)