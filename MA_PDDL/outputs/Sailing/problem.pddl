(define (problem instance_2_1_1229 )
(:domain sailing )
(:objects b0 - boat
p0 - person
)
(:init (= (plan_cost )0 )(= (turn b0 )1 )(= (cur_turn )1 )(= (x b0 )3 )(= (y b0 )0 )(= (d p0 )0 ))
(:goal (and (saved p0 )))
(:metric minimize (plan_cost ))
)