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
	(handempty a2)
	(handempty a1)
	(clear c)
	(clear d)
	(clear a)
	(clear e)
	(ontable b)
	(ontable c)
	(ontable d)
	(ontable e)
	(on a b)
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