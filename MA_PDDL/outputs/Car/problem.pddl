(define (problem multi-car-problem )
(:domain car )
(:requirements :typing :fluents :time )
(:objects car1 - agent
)
(:init (running car1 )(transmission_fine car1 )(= (running_time car1 )0 )(= (d car1 )0 )(= (v car1 )0 )(= (a car1 )0 )(= (up_limit car1 )1 )(= (down_limit car1 )-1 ))
(:goal (and (goal_reached car1 )(not (engineblown car1 ))(<= (running_time car1 )50 )(transmission_fine car1 )))
)