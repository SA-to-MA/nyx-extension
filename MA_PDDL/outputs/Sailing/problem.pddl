(define (problem instance_2_1_1229 )
(:domain sailing )
(:objects b0 - boat
b1 - boat
p0 - person
)
(:init (= (plan_cost )0 )(= (turn b1 )2 )(= (turn b0 )1 )(= (cur_turn )1 )(= (x b0 )3 )(= (y b0 )0 )(= (x b1 )7 )(= (y b1 )0 )(= (d p0 )-370 )(dif_boat b0 b1 )(dif_boat b1 b0 ))
(:goal (and (saved p0 )))
(:metric minimize (plan_cost ))
)