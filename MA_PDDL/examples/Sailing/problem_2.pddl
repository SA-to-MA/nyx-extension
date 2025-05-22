(define (problem instance_2_1_1229)

	(:domain Sailing)

	(:objects
	    (:private
		    b0  - boat
		    b1  - boat
		)
		p0  - person
		p1 - person
	)

  (:init
		(= (x b0) 3)
        (= (y b0) 0)
        (= (x b1) 5)
        (= (y b1) 0)
        (= (d p0) 0)
        (= (d p1) 1)
  )

  (:goal
      (and
        (saved p0)
        (saved p1)

      )
  )
)
